import os

import flet as ft
from flet.core.types import ImageFit


class GlobalAppBar:
    def __init__(self, page: ft.Page, cart, router):
        self.selected_category = None
        self.page = page
        self.cart = cart
        self.router = router
        self.search_value = ""

        self.categories = ["Alles", "Oberbekleidung", "Unterbekleidung", "Accessoires", "Sondereditionen"]

    def build(self) -> ft.AppBar:
        logo_w = 155
        logo_h = 51

        return ft.AppBar(
            title=ft.Row(
                controls=[
                    ft.Stack(
                        controls=[
                            ft.Image(
                                src="https://image2url.com/r2/default/images/1770879899496-2cb5c895-e54f-48ea-ac9a-9ab9ae0d568e.png",
                                width=logo_w,
                                height=logo_h,
                                fit=ImageFit.FILL,
                            ),
                            ft.Container(
                                width=logo_w,
                                height=logo_h,
                                bgcolor=ft.Colors.TRANSPARENT,
                                on_click=lambda _: self.page.go("/"),
                            ),
                        ],
                        width=logo_w,
                        height=logo_h,
                    ),
                    ft.TextField(
                        hint_text="Suche...",
                        on_change=self.on_search_changed,
                        width=200,
                    ),
                ],
            ),
            actions=[
                ft.Dropdown(
                    label="Kategorie",
                    options=[ft.dropdown.Option(cat, cat.capitalize()) for cat in self.categories],
                    on_change=self.on_category_changed,
                    width=150,
                ),
                ft.IconButton(
                    icon=ft.Icons.SHOPPING_CART,
                    on_click=self._on_cart_click,
                    tooltip="Warenkorb öffnen",
                ),
            ],
            bgcolor=ft.Colors.WHITE12,
        )

    def on_search_changed(self, e: ft.ControlEvent):
        self.search_value = e.control.value or ""

        # persist (so CatalogView can read it after navigation/rebuild)
        self.page.session.set("catalog_search", self.search_value)

        # ensure we are on catalog if user searches from anywhere
        if self.page.route != "/catalog":
            self.page.go("/catalog")

        # live update for an already open CatalogView
        try:
            self.page.pubsub.send_all({"type": "catalog_search", "value": self.search_value})
        except Exception as ex:
            print(f"pubsub search send failed: {ex}")

    def on_category_changed(self, e: ft.ControlEvent):
        if e.control.value:
            self.selected_category = e.control.value

            # persist
            self.page.session.set("catalog_category", self.selected_category)

            # navigate (CatalogViewController.selected_category will be set in router)
            self.router.navigate_to_catalog_with_category(self.selected_category)

            # live update
            try:
                self.page.pubsub.send_all({"type": "catalog_category", "value": self.selected_category})
            except Exception as ex:
                print(f"pubsub category send failed: {ex}")

    def _on_cart_click(self, e: ft.ControlEvent):
        """Handle cart icon click"""
        try:
            self.cart.toggle_cart()
        except Exception as ex:
            print(f"Cart error: {ex}")
