from AMS2.src.assets.ShopLogic.Variant import Variant


class Product:
    """Product model"""
    def __init__(self, data: dict, variants: list["Variant"] = None):
        self.id: int = data["productId"]
        self.name: str = data["productName"]
        self.description: str = data["productDescription"]
        self.category = data["categoryName"]
        self.price: float = data["productPrice"]
        self.discount: float = data["productDiscount"]
        self.variants: list[Variant] = variants if variants is not None else []

        # Set product_id on all variants
        for variant in self.variants:
            variant.product_id = self.id

    def get_product_price_with_discount(self) -> float:
        return self.price - self.price*self.discount

    def available_variants(self) -> list[Variant]:
        return [v for v in self.variants if v.is_available]