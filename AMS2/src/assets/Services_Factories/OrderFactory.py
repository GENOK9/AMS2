from AMS2.src.assets.ShopLogic.Order import Order
from AMS2.src.assets.ShopLogic.Customer import Customer
from AMS2.src.assets.ShopLogic.Shoppingcart import Shoppingcart


class OrderFactory:
    """Factory für Bestellungserstellung"""

    @staticmethod
    def create_from_cart(customer: Customer, cart: Shoppingcart, delivery: bool = True) -> Order:
        """Erstellt Order aus ShoppingCart"""
        order = Order(
            id=0,  # Wird vom OrderService gesetzt
            products=cart.items.copy(),
            date=date.today(),
            customer=customer,
            delivery=delivery
        )
        order.calculate_sum()
        return order