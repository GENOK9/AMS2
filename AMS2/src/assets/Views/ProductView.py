import flet as ft
from AMS2.src.assets.Controllers.ProcuctViewController import ProductViewController


class ProductView:
    def __init__(self, page: ft.Page, controller: ProductViewController, product_id: int):
        self.page = page
        self.controller = controller
        self.product_id = product_id

        self.product_image = ft.Image(
            width=300,
            height=300,
            fit=ft.ImageFit.CONTAIN,
        )

        self.variant_dropdown = ft.Dropdown(
            label="Variante auswählen",
            on_change=self._on_variant_changed,
        )

        self.image_counter = ft.Text("", size=12, color=ft.Colors.GREY_600)

    async def build(self) -> ft.Control:
        product = await self.controller.load_product(self.product_id)
        print("detalseiten preis:" + str(product.get_product_price_with_discount()))
        print("detailseiten preis ohne rabatt:" + str(product.price))

        # initiales Bild
        current_image = self.controller.get_current_image()
        if current_image:
            self.product_image.src = current_image
        else:
            self.product_image.src = product.image

        self._update_image_counter()

        # Dropdown Optionen
        self.variant_dropdown.options = []
        for idx, variant in enumerate(product.variants):
            label = f"{variant.color} • {variant.size}"

            if not variant.is_available:
                label += " (nicht verfügbar)"

            self.variant_dropdown.options.append(
                ft.dropdown.Option(
                    key=str(idx),
                    text=label,
                    disabled=not variant.is_available,
                )
            )

        if self.variant_dropdown.options:
            self.variant_dropdown.value = self.variant_dropdown.options[0].key

        return ft.Container(
            expand=True,
            padding=20,
            content=ft.Column(
                spacing=16,
                controls=[
                    # Image gallery with navigation
                    ft.Container(
                        content=ft.Column(
                            spacing=10,
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.IconButton(
                                            icon=ft.Icons.ARROW_BACK_IOS,
                                            on_click=self._on_prev_image,
                                            tooltip="Vorheriges Bild",
                                        ),
                                        ft.Container(
                                            content=self.product_image,
                                            width=300,
                                            height=300,
                                        ),
                                        ft.IconButton(
                                            icon=ft.Icons.ARROW_FORWARD_IOS,
                                            on_click=self._on_next_image,
                                            tooltip="Nächstes Bild",
                                        ),
                                    ],
                                ),
                                self.image_counter,
                            ],
                        ),
                        alignment=ft.alignment.center,
                    ),

                    ft.Text(product.name, size=24, weight=ft.FontWeight.BOLD),

                    ft.Text(
                        f"{product.get_product_price_with_discount():.2f} €",
                        size=20,
                        color=ft.Colors.GREEN_700,
                    ),

                    self.variant_dropdown,

                    ft.ElevatedButton(
                        text="In den Warenkorb",
                        icon=ft.Icons.SHOPPING_CART,
                        on_click=self._on_add_to_cart,
                    ),
                ],
            ),
        )

    #  Events

    def _on_variant_changed(self, e: ft.ControlEvent):
        idx = int(e.control.value)
        new_image = self.controller.on_variant_selected(idx)

        if new_image:
            self.product_image.src = new_image
        self._update_image_counter()
        self.page.update()

    def _on_next_image(self, e: ft.ControlEvent):
        new_image = self.controller.next_image()
        if new_image:
            self.product_image.src = new_image
        self._update_image_counter()
        self.page.update()

    def _on_prev_image(self, e: ft.ControlEvent):
        new_image = self.controller.prev_image()
        if new_image:
            self.product_image.src = new_image
        self._update_image_counter()
        self.page.update()

    def _update_image_counter(self):
        """Update the image counter display"""
        if self.controller.selected_variant:
            images = self.controller.selected_variant.get_all_images()
            if len(images) > 1:
                self.image_counter.value = f"Bild {self.controller.current_image_index + 1} von {len(images)}"
            else:
                self.image_counter.value = ""
        else:
            self.image_counter.value = ""

    async def _on_add_to_cart(self, e: ft.ControlEvent):
        try:
            await self.controller.add_to_cart()

            self.page.snack_bar = ft.SnackBar(
                ft.Text("Zum Warenkorb hinzugefügt ✔")
            )
            self.page.snack_bar.open = True
            self.page.update()

        except Exception as ex:
            self.page.dialog = ft.AlertDialog(
                title=ft.Text("Fehler"),
                content=ft.Text(str(ex)),
                open=True,
            )
            self.page.update()