from AMS2.src.assets.ApiServices.ProductService import ProductService
from AMS2.src.assets.ShopLogic.Product import Product
from AMS2.src.assets.ShopLogic.Shoppingcart import Shoppingcart
from AMS2.src.assets.ShopLogic.Variant import Variant


class ProductViewController:
    def __init__(self, pserv: ProductService, cart: Shoppingcart):
        self.selected_variant: Variant | None = None
        self.pserv = pserv
        self.cart = cart

        self.product: Product | None = None
        self.selected_variant_id: int | None = None
        self.current_image_index: int = 0

    async def load_product(self, product_id: int) -> Product:
        self.product = await self.pserv.get_product_by_id(product_id)
        self.current_image_index = 0

        for v in self.product.variants:
            if v.is_available:
                self.selected_variant = v
                self.selected_variant_id = v.id
                break

        return self.product

    def on_variant_selected(self, variant_index: int) -> str | None:
        """Select a variant and return its primary image"""
        if not self.product or variant_index >= len(self.product.variants):
            return None

        try:
            self.selected_variant = self.product.variants[variant_index]
            self.selected_variant_id = self.selected_variant.id
            self.current_image_index = 0

            # Return the primary image from variant gallery, or fallback to product image
            return self.selected_variant.get_primary_image() or self.product.variants[0].gallery[0]

        except IndexError:
            self.selected_variant = None
            return self.product.variants[0].gallery[0]

    def get_current_image(self) -> str | None:
        """Get the currently displayed image"""
        if self.selected_variant:
            images = self.selected_variant.get_all_images()
            if images and self.current_image_index < len(images):
                return images[self.current_image_index]
            return self.selected_variant.get_primary_image() or self.product.variants[0].gallery[0]
        return self.product.variants[0].gallery[0]

    def next_image(self) -> str | None:
        """Go to next image in the gallery"""
        if self.selected_variant:
            images = self.selected_variant.get_all_images()
            if len(images) > 1:
                self.current_image_index = (self.current_image_index + 1) % len(images)
                return images[self.current_image_index]
        return self.get_current_image()

    def prev_image(self) -> str | None:
        """Go to previous image in the gallery"""
        if self.selected_variant:
            images = self.selected_variant.get_all_images()
            if len(images) > 1:
                self.current_image_index = (self.current_image_index - 1) % len(images)
                return images[self.current_image_index]
        return self.get_current_image()

    async def add_to_cart(self, quantity: int = 1):
        if not self.selected_variant:
            raise ValueError("Keine Variante ausgewählt")

        print(str(self.selected_variant.size))
        await self.cart.add_to_cart(
            variant=self.selected_variant,
            quantity=quantity
        )