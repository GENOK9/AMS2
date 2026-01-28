import flet as ft

from AMS2.src.assets.ApiServices.OrderService import OrderService
from AMS2.src.assets.ShopLogic.Variant import Variant
from AMS2.src.assets.ApiServices.ProductService import ProductService
from AMS2.src.assets.ShopLogic.Customer import Customer


class Shoppingcart:
    def __init__(self, page: ft.Page):
        self.page = page
        self.items: dict[Variant, int] = {}
        self.shoppingcart_items = None
        self.papi = ProductService()
        self.order_service = OrderService()

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
                product = await self.papi.get_product_by_id(variant.product_id)

                subtitle_parts = [
                    f"Farbe: {variant.color}",
                    f"Größe: {variant.size}",
                ]
                subtitle = " - ".join(subtitle_parts)

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

        # Hier ist das fehlende Container-Wrapper mit voller Höhe
        return ft.Container(
            content=ft.Column([
                # Header
                ft.Container(
                    content=ft.Row([
                        ft.Text("Warenkorb", size=20, weight=ft.FontWeight.BOLD),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            on_click=lambda _: self.toggle_cart(self.page),
                            tooltip="Schließen"
                        ),
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=ft.padding.all(15),
                    bgcolor=ft.Colors.ORANGE_500,
                ),
                # ListView mit Produkten
                ft.Container(
                    content=cart_listview,
                    expand=True,
                ),
                # Footer mit Summe (optional)
                ft.Container(
                    content=ft.Column([
                        ft.Divider(height=1),
                        ft.Row([
                            ft.Text("Gesamt:", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                f"€{await self.calculate_total():.2f}",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREEN_700
                            ),
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.ElevatedButton(
                            "Zur Kasse",
                            bgcolor=ft.Colors.ORANGE_500,
                            color=ft.Colors.WHITE,
                            width=float('inf'),
                            on_click=lambda _: self.show_checkout_dialog()
                        ),
                    ], spacing=10),
                    padding=ft.padding.all(15),
                ),
            ], spacing=0),
            width=350,  # Feste Breite
            height=float('inf'),  # Volle Höhe
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(blur_radius=10, spread_radius=2, color=ft.Colors.BLACK12),
            visible=False,  # Initial versteckt
        )

    def add_variant(self, variant: Variant, quantity: int = 1):
        if variant.quantity < quantity:
            raise ValueError("Nicht genug Lagerbestand")

        self.items[variant] = self.items.get(variant, 0) + quantity

    def remove_item(self, variant: Variant):
        self.items.pop(variant, None)
        self.page.update()

    def clear_cart(self):
        self.items.clear()
        self.page.update()

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

    async def calculate_total(self):
        total = 0
        for variant, quantity in self.items.items():
            product = await self.papi.get_product_by_id(variant.product_id)
            total += quantity * product.price
        return total


    def show_checkout_dialog(self):
        # Input-Felder für Kundendaten
        firstname_field = ft.TextField(label="Vorname", hint_text="Max")
        lastname_field = ft.TextField(label="Nachname", hint_text="Mustermann")
        email_field = ft.TextField(label="E-Mail", hint_text="max@example.com")
        phone_field = ft.TextField(label="Telefon", hint_text="0123456789")
        street_field = ft.TextField(label="Straße", hint_text="Musterstraße")
        house_number_field = ft.TextField(label="Hausnummer", hint_text="1A")
        postal_code_field = ft.TextField(label="PLZ", hint_text="12345")
        city_field = ft.TextField(label="Stadt", hint_text="Berlin")
        country_field = ft.TextField(label="Land", hint_text="Deutschland", value="Deutschland")

        # RadioGroup für Versand/Abholung
        delivery_option = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="pickup", label="Abholung"),
                ft.Radio(value="shipping", label="Versand"),
            ]),
            value="pickup"
        )

        async def on_place_order(e):
            await self.place_order(
                firstname_field,
                lastname_field,
                email_field,
                phone_field,
                street_field,
                house_number_field,
                postal_code_field,
                city_field,
                country_field,
                delivery_option
            )

        dialog = ft.AlertDialog(
            title=ft.Text("Bestellung abschließen"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Kundendaten:", weight=ft.FontWeight.BOLD, size=16),
                    firstname_field,
                    lastname_field,
                    email_field,
                    phone_field,
                    ft.Divider(),
                    ft.Text("Adresse:", weight=ft.FontWeight.BOLD, size=16),
                    street_field,
                    house_number_field,
                    postal_code_field,
                    city_field,
                    country_field,
                    ft.Divider(),
                    ft.Text("Lieferung:", weight=ft.FontWeight.BOLD, size=16),
                    delivery_option,
                ], spacing=10, scroll=ft.ScrollMode.AUTO),
                width=400,
                height=600,
            ),
            actions=[
                ft.TextButton("Abbrechen", on_click=lambda _: self.close_dialog()),
                ft.ElevatedButton(
                    "Bestellung aufgeben",
                    bgcolor=ft.Colors.ORANGE_500,
                    color=ft.Colors.WHITE,
                    on_click=on_place_order
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = dialog
        dialog.open = True
        self.page.update()

    def close_dialog(self):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    async def place_order(self, firstname_field, lastname_field, email_field, phone_field,
                          street_field, house_number_field, postal_code_field, city_field,
                          country_field, delivery_option):
        # Validierung
        if not all([
            firstname_field.value,
            lastname_field.value,
            email_field.value,
            phone_field.value,
            street_field.value,
            house_number_field.value,
            postal_code_field.value,
            city_field.value,
            country_field.value
        ]):
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Bitte alle Felder ausfüllen!"),
                bgcolor=ft.Colors.RED_500
            )
            self.page.snack_bar.open = True
            self.page.update()
            return

        # Customer-Objekt erstellen
        customer = Customer(
            firstname_field.value,
            lastname_field.value,
            email_field.value,
            phone_field.value,
            street_field.value,
            house_number_field.value,
            postal_code_field.value,
            city_field.value,
            country_field.value,
            delivery_option.value
        )

        # Order-Daten (variant_id: quantity)
        order_data = {
            variant.id: quantity
            for variant, quantity in self.items.items()
        }

        try:
            # Bestellung senden mit Customer-Objekt und Order-Daten
            await self.order_service.create_order(customer, order_data)

            # Dialog schließen
            self.close_dialog()

            # Warenkorb leeren
            self.items.clear()

            # Warenkorb schließen
            self.cart_panel.visible = False
            self.page.update()

            # Erfolgs-Snackbar
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text("Bestellung erfolgreich aufgegeben!"),
                bgcolor=ft.Colors.GREEN_500
            )
            self.page.snack_bar.open = True
            self.page.update()

        except Exception as e:
            # Fehlerbehandlung
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(f"Fehler bei der Bestellung: {str(e)}"),
                bgcolor=ft.Colors.RED_500
            )
            self.page.snack_bar.open = True
            self.page.update()


def add_to_cart(self, cart: Shoppingcart):
    variant = self.variants[self.selectedVariant]
    cart.add_variant(variant)
