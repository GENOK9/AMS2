class Variant:
    def __init__(self, data: dict):
        self.id: int = data["variantId"]
        self.color: str = data["color"]
        self.size: str = data["uniSize"]
        self.num_size: int = data["numSize"]
        self.gallery: list[str] = data.get("gallery", [])
        self.out_of_stock: bool = data["outOfStock"]
        self.product_id: int = None  # Will be set by Product model
        self.quantity: int = 1 if not data["outOfStock"] else 0

    @property
    def is_available(self) -> bool:
        return not self.out_of_stock

    def get_primary_image(self) -> str | None:
        """Returns the first image from the gallery, or None if no images"""
        return self.gallery[0] if self.gallery else None

    def get_all_images(self) -> list[str]:
        """Returns all images in the gallery"""
        return self.gallery if self.gallery else []