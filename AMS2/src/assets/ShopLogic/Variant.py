
class Variant:
    def __init__(self, data: dict):
        self.id: int = data["id"]
        self.product_id: int = data["product_id"]
        self.size: str = data["uni_size"]
        self.color: str = data["color"]
        self.quantity: int = data["quantity"]

    @property
    def is_available(self) -> bool:
        return self.quantity > 0
