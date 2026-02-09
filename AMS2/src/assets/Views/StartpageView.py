"""
Startpage View - Hauptseite des Shops
"""
import flet as ft
from flet.core.types import ImageFit

from AMS2.src.assets.Controllers.StartpageController import StartpageController
from AMS2.src.assets.ShopLogic.CatalogProduct import CatalogProduct
from AMS2.src.assets.ShopLogic.Product import Product


class StartpageView:
    def __init__(self, page: ft.Page, controller: StartpageController):
        self.page = page
        self.controller = controller

    async def build(self) -> ft.Control:
        featured_products: list[CatalogProduct] = await self.controller.get_featured_products()

        return ft.Container(
            expand=True,
            content=ft.Column(
                spacing=0,
                controls=[
                    self.create_hero(),
                    self.create_featured_section(featured_products),
                    self.create_footer(),
                ],
            ),
        )

    # ---------- HERO ----------

    def create_hero(self) -> ft.Container:
        return ft.Container(
            image=ft.DecorationImage("AMS2/src/assets/icon.png", fit=ImageFit.COVER),
            padding=80,
            alignment=ft.alignment.center,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                controls=[
                    ft.Text(
                        "Willkommen beim ATIW MERCH STORE",
                        size=40,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.WHITE,
                    ),
                    ft.Text(
                        "Die neuesten Trends für gute Noten",
                        size=20,
                        color=ft.Colors.WHITE70,
                    ),
                    ft.ElevatedButton(
                        "Zum Katalog",
                        on_click=lambda _: self.page.go("/catalog"),
                        bgcolor=ft.Colors.ORANGE_500,
                        color=ft.Colors.WHITE,
                        height=50,
                        width=200,
                    ),
                ],
            ),
        )

    #  FEATURED

    def create_featured_section(self, products: list[CatalogProduct]) -> ft.Container:
        if not products:
            return ft.Container()

        cards = [
            self.create_product_card(product)
            for product in products
        ]

        return ft.Container(
            padding=40,
            content=ft.Column(
                spacing=20,
                controls=[
                    ft.Text(
                        "Neu & Beliebt",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Row(
                        controls=cards,
                        wrap=True,
                        spacing=20,
                    ),
                ],
            ),
        )

    def create_product_card(self, product: CatalogProduct) -> ft.Container:
        print("startpage preis:" + str(product.get_product_price_with_discount()))
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
                        on_click=lambda _, pid=product.id: self.controller.on_featured_product_clicked(pid),
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE,
                    ),
                ],
            ),
        )

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
