

class CatalogProduct:
    def __init__(self, data: dict):
        self.id: int = data["productId"]
        self.name: str = data["productName"]
        self.price: float = data["productPrice"]
        self.discount: float = data["discountPercentage"]
        self.thumbnail: str = data["thumbnail"]
        self.out_of_stock: bool = data["outOfStock"]

    def get_product_price_with_discount(self) -> float:
        print("discount = " + str(self.discount))
        return self.price - self.price*self.discount
