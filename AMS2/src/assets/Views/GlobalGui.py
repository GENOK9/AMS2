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
        return ft.AppBar(
            title=ft.Row(
                controls=[
                    ft.Image(src="AMS2/src/assets/icon.png", width=250, height=83, fit=ImageFit.CONTAIN),
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
        self.search_value = e.control.value
        # TODO: Implementiere Suchfunktion

    def on_category_changed(self, e: ft.ControlEvent):
        if e.control.value:
            self.selected_category = e.control.value
            self.router.navigate_to_catalog_with_category(self.selected_category)

    def _on_cart_click(self, e: ft.ControlEvent):
        """Handle cart icon click"""
        try:
            self.cart.toggle_cart()
        except Exception as ex:
            print(f"Cart error: {ex}")
