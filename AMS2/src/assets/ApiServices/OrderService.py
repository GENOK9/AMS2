import json

from AMS2.src.assets.ApiServices.ApiService import ApiService


class OrderService:
    """Order API Service"""

    def __init__(self, api: ApiService):
        self.api = api

    async def create_order(self, order_data: dict):
        print("order_data (json):", json.dumps(order_data, ensure_ascii=False, indent=2, default=str))
        """
        Erstellt Bestellung
        POST /orders

        Body: {
            "customer": {
                "firstname": "Max",
                "lastname": "Mustermann",
                ...
            },
            "items": [
                {
                    "variant_id": 2,
                    "quantity": 3
                }
            ],
            "delivery": true
        }
        """
        await self.api.post("order/new", order_data)
        print("Bestellung erfolgreich ABGESENDET!")