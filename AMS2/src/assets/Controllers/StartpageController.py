import flet as ft


class StartpageController:
    def __init__(self, product_service, page: ft.Page):
        self.product_service = product_service
        self.page = page

    async def get_featured_products(self):
        products = await self.product_service.get_all_products()
        return products[:3]

    def on_featured_product_clicked(self, product_id: int):
        self.page.go(f"/product?productid={product_id}")
