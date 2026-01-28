import flet as ft

class GlobalAppBar:
    def __init__(self, page: ft.Page, cart):
        self.selected_category = None
        self.page = page
        self.cart = cart
        self.search_value = ""

        self.categories = ["Alles", "Oberteile", "Unterteile", "Accessoires"]

    def build(self) -> ft.AppBar:
        return ft.AppBar(
            title=ft.Row(
                controls=[
                    ft.Text("ATIW MERCH SHOP"),
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
                ),
                ft.IconButton(
                    icon=ft.Icons.SHOPPING_CART,
                    on_click=lambda _: self.cart.toggle_cart(self.page),
                    tooltip="Warenkorb öffnen",
                ),
            ],
            bgcolor=ft.Colors.BLUE_700,
        )

    #  Suche
    def on_search_changed(self, e: ft.ControlEvent):
        self.search_value = e.control.value

    #  Kategorie
    def on_category_changed(self, e: ft.ControlEvent):
        self.selected_category = e.control.value
