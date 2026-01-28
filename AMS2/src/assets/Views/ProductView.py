import flet as ft

class ProductView:
    def __init__(self, product, on_variant_selected, on_add_to_cart):
        self.product = product
        self.on_variant_selected = on_variant_selected
        self.on_add_to_cart = on_add_to_cart

    def build(self):
        variant_options = []

        for idx, variant in enumerate(self.product.variants):
            label = f"{variant.color} • {variant.uniSize}"

            if variant.quantity <= 0:
                label += " (nicht verfügbar)"

            variant_options.append(
                ft.dropdown.Option(
                    key=str(idx),
                    text=label,
                    disabled=variant.quantity <= 0
                )
            )

        return ft.Column(
            controls=[
                ft.Text(self.product.name, size=20, weight=ft.FontWeight.BOLD),

                ft.Dropdown(
                    label="Variante auswählen",
                    options=variant_options,
                    value="0",
                    on_select=self.on_variant_selected,
                ),

                ft.ElevatedButton(
                    text="In den Warenkorb",
                    on_click=self.on_add_to_cart
                )
            ],
            spacing=10
        )

    @classmethod
    def show_out_of_stock(cls):
        out_of_stock_alert = ft.AlertDialog(
            title=ft.Text("Out of Stock"),
            content=ft.Text("This product is out of stock."),
            actions=[ft.TextButton("Dismiss")],
            open=True,
)
