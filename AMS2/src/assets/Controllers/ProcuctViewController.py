from AMS2.src.assets.ShopLogic.Product import Product
from AMS2.src.assets.ShopLogic.Shoppingcart import Shoppingcart
from AMS2.src.assets.Views.ProductView import ProductView


def show_out_of_stock():
    ProductView.show_out_of_stock()
    pass


class ProductViewController:
    def __init__(self, product: Product, cart: Shoppingcart):
        self.product = product
        self.cart = cart
        self.selected_variant_index = 0

    def on_variant_selected(self, e):
        self.selected_variant_index = int(e.control.value)

    def add_to_cart(self, e):
        variant = self.product.variants[self.selected_variant_index]

        if variant.quantity <= 0:
            show_out_of_stock()
            return

        self.cart.add_variant(variant)
