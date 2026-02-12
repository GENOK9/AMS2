from traceback import print_tb

import httpx


class ApiService:
    """Base API Service für HTTP Requests"""

    def __init__(self, base_url: str = "http://localhost:8080/api"):
        self.base_url = base_url
        self.client = httpx.Client(timeout=30.0)
        self.AsyncClient = httpx.AsyncClient(timeout=30.0)

    async def get(self, endpoint: str, params: dict = None):
        """GET Request"""
        response = self.client.get(f"{self.base_url}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()

    async def post(self, endpoint: str, data: dict):
        """POST Request"""
        await self.AsyncClient.post(f"{self.base_url}/{endpoint}", json=data)
        print("halloooo")
