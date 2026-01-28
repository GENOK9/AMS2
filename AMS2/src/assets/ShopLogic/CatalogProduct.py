

class CatalogProduct:
    def __init__(self, data: dict):
        self.id: int = data["productId"]
        self.name: str = data["productName"]
        self.price: float = data["bruttoPrice"]
        self.discount: float = data["discountPercentage"]
        self.thumbnail: str = data["thumbnail"]
        self.out_of_stock: bool = data["outOfStock"]

    def get_product_price_with_discount(self) -> float:
        return self.price * (1 - self.discount / 100)