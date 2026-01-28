import flet as ft
from AMS2.src.assets.ShopLogic.Variant import Variant
from AMS2.src.assets.ApiServices.ProductService import ProductService


class Shoppingcart:
    def __init__(self, page: ft.Page):
        self.page = page
        self.items: dict[Variant, int] = {}
        self.shoppingcart_items = None
        self.papi = ProductService()

    async def cart_panel(self):
        cart_listview = ft.ListView(
            spacing=10,
            padding=10,
            expand=True)

        if not self.items or len(self.items) == 0:
            cart_listview.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.SHOPPING_CART_OUTLINED, size=60, color=ft.Colors.GREY_400),
                        ft.Text("Dein Warenkorb ist leer", color=ft.Colors.GREY_600),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                    alignment=ft.alignment.center,
                    padding=40,
                )
            )
        else:
            for variant, quantity in self.items.items():
                product = await self.papi.get_product_by_id(variant.product_id)  # or lookup by product_id

                subtitle_parts = [
                    f"Farbe: {variant.color}",
                    f"Größe: {variant.size}",
                    f"Passform: {product}",
                ]
                subtitle = " • ".join(subtitle_parts)

                cart_listview.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.CHECKROOM, size=40, color=ft.Colors.BLUE_400),
                        title=ft.Text(product.name, weight=ft.FontWeight.BOLD),
                        subtitle=ft.Column([
                            ft.Text(subtitle, size=12, color=ft.Colors.GREY_600),
                            ft.Text(
                                f"€{product.get_product_price_with_discount():.2f}",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREEN_700,
                            ),
                        ], spacing=4),
                        trailing=ft.Row([
                            ft.Text(f"{quantity}x", size=16, weight=ft.FontWeight.BOLD),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=ft.Colors.RED_400,
                                icon_size=20,
                                on_click=lambda _, v=variant: self.remove_item(v),
                            ),
                        ], width=80, spacing=5),
                    )
                )
                self.page.update()

    def add_variant(self, variant: Variant, quantity: int = 1):
        if variant.quantity < quantity:
            raise ValueError("Nicht genug Lagerbestand")

        self.items[variant] = self.items.get(variant, 0) + quantity

    def remove_item(self, variant: Variant):
        self.items.pop(variant, None)
        self.page.update()

    def clear_cart(self):
        self.items.clear()

    def toggle_cart_button(self, page: ft.Page):
        cart_button = ft.FloatingActionButton(
            icon=ft.Icons.SHOPPING_CART,
            bgcolor=ft.Colors.ORANGE_500,
            on_click=lambda _: (self.toggle_cart(page)),
            tooltip="Warenkorb öffnen",
        )

        return cart_button

    def toggle_cart(self, page: ft.Page):
        self.cart_panel.visible = not self.cart_panel.visible
        page.update()
        self.page.update()

    def close_cart(self):
        self.cart_panel.visible = False
        self.page.update()


def add_to_cart(self, cart: Shoppingcart):
    variant = self.variants[self.selectedVariant]
    cart.add_variant(variant)
