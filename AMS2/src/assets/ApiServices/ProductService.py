from AMS2.src.assets.ApiServices.ApiService import ApiService
from AMS2.src.assets.ShopLogic.CatalogProduct import CatalogProduct
from AMS2.src.assets.ShopLogic.Product import Product
from AMS2.src.assets.ShopLogic.Variant import Variant


class ProductService:
    """Product API Service"""

    def __init__(self, ):
        self.api = ApiService()

    async def get_all_products(self) -> list[CatalogProduct]:
        """
        "light mode": only First Picture, Price & Name
        GET /products
        """
        data = await self.api.get("products")

        catalog_products = []
        for item in data["products"]:
            catalog_products.append(CatalogProduct(data=item))

        return catalog_products

    async def get_products_by_category(self, category: str) -> list[Product]:
        """
        "light mode" by Category: only First Picture, Price & Name
        GET /products?category=Shirts
        """
        data = await self.api.get("products", params={"category": category})

        products = []
        for item in data["products"]:
            products.append(Product(data=item, variants=[]))

        return products

    async def get_product_by_id(self, product_id: int) -> Product:
        """
        Product by ID with all attributes
        GET /product/{id}
        """
        data = await self.api.get(f"product/{product_id}")

        variants = [Variant(v) for v in data.get("variants", [])]

        product = Product(data=data, variants=variants)

        return product
