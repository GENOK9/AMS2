from AMS.src.assets.ApiServices.ApiService import ApiService


class OrderService:
    """Order API Service"""

    def __init__(self, api: ApiService):
        self.api = api

    async def create_order(self, order_data: dict) -> dict:
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
                    "product_id": 1,
                    "variant_id": 2,
                    "quantity": 3
                }
            ],
            "delivery": true
        }
        """
        response = await self.api.post("orders", order_data)
        return response