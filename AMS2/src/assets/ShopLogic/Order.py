from datetime import date

from dataclasses import dataclass
from AMS2.src.assets.ShopLogic.Product import Product
from AMS2.src.assets.ShopLogic.Customer import Customer


@dataclass
class Order:
    """Bestellungsmodell"""
    id: int
    products: dict[Product, int]  # Produkt, Menge
    date: date
    customer: Customer
    delivery: bool
    sum: float = 0.0

    def calculate_sum(self) -> float:
        """Berechnet Gesamtsumme der Bestellung"""
        total = sum(
            product.get_product_price_with_discount() * quantity
            for product, quantity in self.products.items()
        )
        self.sum = total
        return total

