from AMS2.src.assets.ShopLogic.CatalogProduct import CatalogProduct
from AMS2.src.assets.ApiServices.ProductService import ProductService


class CatalogViewController:
    def __init__(self):
        self.product_service = ProductService()
        self.selected_category = None

    async def load_products(self):
        """loads products from api"""
        try:
            return await self.product_service.get_all_products()

        except Exception as e:
            raise RuntimeError("Produkte konnten nicht geladen werden") from e

    async def load_categories(self, category):
        """ loads products from api by category"""
        try:
            return await self.product_service.get_products_by_category(category)

        except Exception as e:
            raise RuntimeError("Kategorie konnte nicht geladen werden") from e
