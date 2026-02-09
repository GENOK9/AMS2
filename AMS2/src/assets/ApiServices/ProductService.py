from AMS2.src.assets.ApiServices.ApiService import ApiService
from AMS2.src.assets.ShopLogic.CatalogProduct import CatalogProduct
from AMS2.src.assets.ShopLogic.Product import Product
from AMS2.src.assets.ShopLogic.Variant import Variant


class ProductService:
    """Product API Service"""

    def __init__(self, api):
        self.api = api

    async def get_all_products(self):
        endpoint = "product/all"
        data = await self.api.get(endpoint)

        print("API PRODUCT SAMPLE:", data[1])
        return [CatalogProduct(item) for item in data]

    async def get_products_by_category(self, category: str) -> list[CatalogProduct]:
        """
        "light mode" by Category: only First Picture, Price & Name
        GET /category/shirts
        """
        data = await self.api.get("category/name", category)

        print("API PRODUCT SAMPLE:", data[1])
        return [CatalogProduct(item) for item in data]

    async def get_product_by_id(self, product_id: int) -> Product:
        """
        Product by ID with all attributes
        GET /product/{id}
        """
        data = await self.api.get(f"product/id/{product_id}")

        variants = [Variant(v) for v in data.get("variants", [])]

        product = Product(data=data, variants=variants)

        return product
