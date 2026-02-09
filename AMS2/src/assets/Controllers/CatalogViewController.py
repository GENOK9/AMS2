from AMS2.src.assets.ShopLogic.CatalogProduct import CatalogProduct
from AMS2.src.assets.ApiServices.ProductService import ProductService


class CatalogViewController:
    def __init__(self, product_service):
        self.product_service = product_service
        self.selected_category: str = "Alles"

    async def load_products(self):
        try:
            if self.selected_category and self.selected_category != "Alles":
                products = await self.product_service.get_products_by_category(self.selected_category)
                return products
            else:
                self.selected_category = None
                products = await self.product_service.get_all_products()
                return products
        except Exception as e:
            raise RuntimeError("Produkte konnten nicht geladen werden") from e

    def sort_products(self, products: list, mode: str):
        if mode == "price_asc":
            return sorted(products, key=lambda p: p.price)
        if mode == "price_desc":
            return sorted(products, key=lambda p: p.price, reverse=True)
        return products