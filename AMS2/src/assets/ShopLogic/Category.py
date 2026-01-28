from AMS2.src.assets.ShopLogic.Product import Product


class Category:
    id: int
    name: str
    description: str
    products: list[Product]