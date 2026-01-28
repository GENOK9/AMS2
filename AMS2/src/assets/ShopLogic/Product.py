from typing import List

from AMS2.src.assets.ShopLogic.Variant import Variant


class Product:
    """Product model"""
    def __init__(self, data: dict, variants: list["Variant"] = None):
        self.id: int = data["id"]
        self.name: str = data["name"]
        self.description: str = data["description"]
        self.category = data["category"]
        self.price: float = data["price"]
        self.discount: float = data["discount"]
        self.fit: str = data["fit"]
        self.variants: list[Variant] = variants if variants is not None else []


    def get_product_price_with_discount(self) -> float:
        return self.price * (1 - self.discount / 100)

    def available_variants(self) -> list[Variant]:
        return [v for v in self.variants if v.is_available]