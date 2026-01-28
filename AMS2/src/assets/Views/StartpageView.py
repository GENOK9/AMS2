"""
Startpage View - Hauptseite des Shops
"""
import flet as ft
import AMS2.src.assets.Controllers.StartpageController as StartpageController
from AMS2.src.assets.ShopLogic.Shoppingcart import Shoppingcart


class StartpageView:
    """Startseiten-View als instanzierbare Klasse"""

    shoppingcart = Shoppingcart

    def __init__(self, page : ft.Page):
        self.page = page
        self.controller = StartpageController
        self.spacing = 0
        self.expand = True
        self.categories = [     #kommt später von API
            {"name": "Shirts", "icon": ft.Icons.CHECKROOM, "color": ft.Colors.PINK_400},
            {"name": "Hosen", "icon": ft.Icons.DRY_CLEANING, "color": ft.Colors.PURPLE_400},
            {"name": "Schuhe", "icon": ft.Icons.SHOPPING_BAG, "color": ft.Colors.BLUE_400},
            {"name": "Jacken", "icon": ft.Icons.AC_UNIT, "color": ft.Colors.TEAL_400},
            {"name": "Accessoires", "icon": ft.Icons.WATCH, "color": ft.Colors.ORANGE_400},
        ]

    def build(self):
        return ft.Column(
            controls = [
                self.create_header(),
                self.create_category_bar(),
                ft.Container(
                    content=ft.Column([
                        self.create_hero(),
                        self.create_category_bar(),
                        self.create_featured_section(),
                        self.create_footer(),
                    ], spacing=0, scroll=ft.ScrollMode.AUTO),
                    expand=True,
                ),
            ]
        )

    def create_header(self):
        """Erstellt den Header mit Navigation"""
        return ft.Container(
            content=ft.Row([
                ft.Text("🛍️ FASHION STORE", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Row([
                    ft.TextButton("Katalog", on_click=lambda _: self.page.go("/catalog"),
                                  style=ft.ButtonStyle(color=ft.Colors.WHITE)),
                ], spacing=10),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            bgcolor=ft.Colors.BLUE_700,
            padding=15,
        )

    def create_featured_section(self):
        """Featured Products Section"""
        featured_products = self.controller.get_featured_products()
        return ft.Row([
                ft.Text("Featured Products", size=32, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
                ft.Row([
                    self.create_product_card(product) for product in featured_products
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=30, wrap=True),
            ], spacing=40, vertical_alignment=ft.CrossAxisAlignment.CENTER)


    def create_hero(self):
        """Hero Section"""
        return ft.Container(
            content=ft.Column(
                controls=[
                ft.Text("Willkommen bei Fashion Store", size=40, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text("Die neuesten Trends für deinen Style", size=20, color=ft.Colors.WHITE70),
                ft.ElevatedButton(
                    "Jetzt Shoppen",
                    on_click=lambda _: self.page.go("/catalog"),
                    bgcolor=ft.Colors.ORANGE_500,
                    color=ft.Colors.WHITE,
                    height=50,
                    width=200,
                ),self.create_featured_section(),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=20),
            bgcolor=ft.Colors.BLUE_900,
            padding=80,
            alignment=ft.alignment.center,
        )

    def create_product_card(self, product):
        """Create Product Card (for featured products etc.)"""
        discount_badge = None
        if product.has_discount():
            discount_badge = ft.Container(
                content=ft.Text(f"-{int(product.discount)}%", size=14, weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE),
                bgcolor=ft.Colors.RED_500,
                padding=8,
                border_radius=5,
            )

        return ft.Container(
            content=ft.Column([
                ft.Stack([
                    ft.Container(
                        content=ft.Icon(ft.Icons.IMAGE, size=80, color=ft.Colors.GREY_400),
                        bgcolor=ft.Colors.GREY_200,
                        height=200,
                        alignment=ft.alignment.center,
                    ),
                    ft.Container(discount_badge, alignment=ft.alignment.top_right,
                                 padding=10) if discount_badge else ft.Container(),
                ]),
                ft.Column([
                    ft.Text(product.name, size=16, weight=ft.FontWeight.BOLD, max_lines=1),
                    ft.Text(product.description[:50] + "...", size=12, color=ft.Colors.GREY_600, max_lines=2),
                    ft.Row([
                        ft.Text(f"€{product.get_product_price_with_discount():.2f}", size=18, weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREEN_700)],spacing=10),
                    ft.ElevatedButton(
                        "Details ansehen",
                        on_click=lambda _, pid=product.id: self.controller.on_featured_product_clicked(pid),
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE,
                    ),
                ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.START),
            ], spacing=10),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            padding=15,
            shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.BLACK12),
            width=280,
        )

    def create_footer(self):
        """Footer"""
        return ft.Container(
            content=ft.Column([
                ft.Divider(),
                ft.Row([
                    ft.TextButton("Impressum", on_click=lambda _: self.page.go("/impressum")),
                    ft.TextButton("AGB", on_click=lambda _: self.page.go("/agb")),
                    ft.TextButton("Datenschutz", on_click=lambda _: self.page.go("/datenschutz")),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
                ft.Text("© 2025 AMS - ATIW MERCH SHOP - Alle Rechte vorbehalten", size=12, color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER),
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
        )

    def create_category_bar(self):
        """Category Bar"""
        return ft.Container(
            content=ft.Row([
               ft.ElevatedButton(
                   content=ft.Row([
                       ft.Icon(cat["icon"], size=20),
                       ft.Text(cat["name"]),
                   ], spacing=8),
                   on_click=lambda _, c=cat["name"]: self.page.go(f"/catalog?category={c}"),
                   style=ft.ButtonStyle(
                       color=ft.Colors.WHITE,
                       bgcolor=cat["color"],
                   ),
               )
               for cat in self.categories
           ] + [
               # "Alle" Button
               ft.ElevatedButton(
                   "Alle Produkte",
                   on_click=lambda _: self.page.go("/catalog"),
                   style=ft.ButtonStyle(
                       color=ft.Colors.WHITE,
                       bgcolor=ft.Colors.BLUE_700,
                   ),
               )
           ],
            spacing=10, scroll=ft.ScrollMode.AUTO),
            bgcolor=ft.Colors.GREY_100,
            padding=10,
        )