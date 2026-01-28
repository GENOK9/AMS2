"""
Catalog View  - Artikelkatalog mit Kategorien, Suche, filter und sortierfunktion ...
"""
import flet as ft
from AMS2.src.assets.Controllers.CatalogViewController import CatalogViewController
from AMS2.src.assets.ShopLogic.CatalogProduct import CatalogProduct

class CatalogView:
    def __init__(self, page: ft.Page):
        self.page : ft.Page = page
        self.controller = CatalogViewController()
        self.products: list[CatalogProduct] = []
        self.list_view = ft.ListView(expand=True, spacing=10)

    #  public
    async def build(self) -> ft.Container:
        try:
            self.products = await self.controller.load_products()
            self._build_list()

        except Exception as e:
            self._show_error_alert(str(e))

        return ft.Container(
            expand=True,
            padding=20,
            content=ft.Column(
                controls=[
                    self._build_filter_bar(),
                    self.list_view,
                ],
            ),
        )

    #  UI building
    def _build_filter_bar(self) -> ft.Row:
        return ft.Row(
            controls=[
                ft.Dropdown(
                    label="Sortieren",
                    options=[
                        ft.dropdown.Option("price_asc", "Preis ↑"),
                        ft.dropdown.Option("price_desc", "Preis ↓"),
                    ],
                    on_change=self._on_sort_changed,
                ),
                ft.Dropdown(
                    label="Kategorie",
                    options=[
                        ft.dropdown.Option("all", "Alle"),
                        ft.dropdown.Option("shirts", "Shirts"),
                        ft.dropdown.Option("pants", "Hosen"),
                    ],
                    on_change=self._on_category_changed,
                ),
            ]
        )

    def _build_list(self):
        self.list_view.controls.clear()

        for product in self.products:
            self.list_view.controls.append(
                self._product_tile(product)
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

    #  events
    def _on_product_clicked(self, product: CatalogProduct):
        self.page.session.set("current_product", product.id)
        self.page.go(f"/product?productid={product.id}")

    def _on_sort_changed(self, e):
        # TODO: Controller informieren / lokal sortieren
        pass

    def _on_category_changed(self, e):
        # TODO: Controller informieren / neu laden
        pass

    #  error
    def _show_error_alert(self, message: str):
        self.page.dialog = ft.AlertDialog(
            title=ft.Text("Catalog Error"),
            content=ft.Text(message),
            actions=[ft.TextButton("Dismiss")],
            open=True,
        )
        self.page.dialog.open = True
        self.page.update()
