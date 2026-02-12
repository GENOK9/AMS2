"""
Catalog View  - Artikelkatalog mit Kategorien, Suche, filter und sortierfunktion ...
"""
import sys

import flet as ft
from AMS2.src.assets.Controllers.CatalogViewController import CatalogViewController
from AMS2.src.assets.ShopLogic.CatalogProduct import CatalogProduct


class CatalogView:
    def __init__(self, page: ft.Page, controller: CatalogViewController):
        self.page: ft.Page = page
        self.controller = controller
        self.products: list[CatalogProduct] = []
        self.list_view = ft.ListView(expand=True, spacing=10)
        self.selected_category: str = "Alles"


        self.sort_dropdown = ft.Dropdown(
            label="Sortieren",
            options=[
                ft.dropdown.Option("price_asc", "Preis ↑"),
                ft.dropdown.Option("price_desc", "Preis ↓"),
            ],
            on_change=self._on_sort_changed,
        )

    # Public
    async def build(self) -> ft.Container:
        try:
            self.products = await self.controller.load_products()
            self._build_items()
        except Exception as e:
            self._show_error_alert(str(e))

        return ft.Container(
            expand=True,
            padding=20,
            content=ft.Column(
                controls=[
                    self._build_filter_bar(),
                    self.list_view,
                    self.create_footer(),
                ],
            ),
        )

    #  when category changes
    async def refresh_products(self):
        """Refreshes the product list (called when category changes)"""
        try:
            self.products = await self.controller.load_products()
            self._build_items()
            self.page.update()
        except Exception as e:
            self._show_error_alert(str(e))

    # UI Building
    def _build_filter_bar(self) -> ft.Row:
        return ft.Row(
            controls=[self.sort_dropdown]
        )

    def _is_mobile(self) -> bool:
        """Check if the current screen is mobile (width < 600)"""
        return sys.platform == "android" or sys.platform == "ios"


    def _build_items(self):
        self.list_view.controls.clear()

        if self._is_mobile():
            # Mobile: ListView with tiles
            self.list_view = ft.ListView(
                expand=True,
                spacing=10,
            )
            for product in self.products:
                self.list_view.controls.append(
                    self._product_tile(product)
                )
        else:
            # Desktop: Grid layout with product cards
            self.list_view = ft.ListView(
                expand=True,
                spacing=0,
            )

            # cards per row
            cards_per_row = 6
            for i in range(0, len(self.products), cards_per_row):
                row_products = self.products[i:i + cards_per_row]
                cards = [self._product_card(product) for product in row_products]

                self.list_view.controls.append(
                    ft.Row(
                        controls=cards,
                        spacing=20,
                        wrap=False,
                    )
                )

    def _product_tile(self, product: CatalogProduct) -> ft.Control:
        return ft.Container(
            padding=12,
            border_radius=8,
            bgcolor=ft.Colors.SURFACE,
            on_click=lambda _: self._on_product_clicked(product),
            content=ft.Row(
                controls=[
                    ft.Image(
                        src=product.thumbnail,
                        width=80,
                        height=80,
                        fit=ft.ImageFit.COVER,
                    ),
                    ft.Column(
                        expand=True,
                        controls=[
                            ft.Text(product.name, weight=ft.FontWeight.BOLD),
                            ft.Text(f"{product.price:.2f} €"),
                            ft.Text(
                                "Ausverkauft" if product.out_of_stock else "Verfügbar",
                                color=ft.Colors.RED if product.out_of_stock else ft.Colors.GREEN,
                            ),
                        ],
                    ),
                ]
            ),
        )

    def _product_card(self, product: CatalogProduct) -> ft.Container:
        print("katalog preis:" + str(product.get_product_price_with_discount()))
        """Grid card for desktop (same style as StartpageView)"""
        discount_badge = None
        if product.discount and product.discount > 0:
            discount_badge = ft.Container(
                content=ft.Text(
                    f"-{int(product.discount*100)}%",
                    size=14,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
                bgcolor=ft.Colors.RED_500,
                padding=8,
                border_radius=5,
            )

        return ft.Container(
            width=280,
            padding=15,
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
            on_click=lambda _: self._on_product_clicked(product),
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.Stack(
                        controls=[
                            ft.Image(
                                src=product.thumbnail,
                                height=200,
                                fit=ft.ImageFit.COVER,
                            ),
                            ft.Container(
                                discount_badge,
                                alignment=ft.alignment.top_right,
                                padding=10,
                            ) if discount_badge else ft.Container(),
                        ]
                    ),
                    ft.Text(
                        product.name,
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        max_lines=1,
                    ),
                    ft.Text(
                        f"€{product.get_product_price_with_discount():.2f}",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREEN_700,
                    ),
                    ft.ElevatedButton(
                        "Details ansehen",
                        on_click=lambda _, pid=product.id: self._on_product_clicked(product),
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE,
                    ),
                ],
            ),
        )


    # Events
    def _on_product_clicked(self, product: CatalogProduct):
        self.page.session.set("current_product", product.id)
        self.page.go(f"/product?productid={product.id}")

    def _on_sort_changed(self, e: ft.ControlEvent):
        mode = e.control.value
        self.products = self.controller.sort_products(self.products, mode)
        self._build_items()
        self.page.update()

    # Error Handling
    def _show_error_alert(self, message: str):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Catalog Error"),
            content=ft.Text(message),
            actions=[ft.TextButton("Dismiss")],
            open=True,
        )
        self.page.dialog.open = True
        self.page.update()

    #  FOOTER
    def create_footer(self) -> ft.Container:
        return ft.Container(
            padding=20,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                controls=[
                    ft.Divider(),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=20,
                        controls=[
                            ft.TextButton("Impressum", on_click=lambda _: self.page.go("/impressum")),
                            ft.TextButton("AGB", on_click=lambda _: self.page.go("/agb")),
                            ft.TextButton("Datenschutz", on_click=lambda _: self.page.go("/datenschutz")),
                        ],
                    ),
                    ft.Text(
                        "© 2025 AMS – ATIW MERCH SHOP – Alle Rechte vorbehalten",
                        size=12,
                        color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
            ),
        )
