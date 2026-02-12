from AMS2.src.assets.ApiServices.ApiService import ApiService
from AMS2.src.assets.ShopLogic.CatalogProduct import CatalogProduct


class CategoryService:
    """Category API Service (uses /category/* endpoints)"""

    def __init__(self, api: ApiService):
        self.api = api

    async def get_all_category_names(self) -> list[str]:
        """
        Backend: GET /category/name/all
        Returns: List[CategoryNameDto]
        """
        data = await self.api.get("category/name/all")

        # Try common DTO shapes: [{"name": "Oberbekleidung"}, ...] or [{"categoryName": "..."}]
        names: list[str] = []
        for item in data or []:
            if isinstance(item, dict):
                names.append(item.get("name") or item.get("categoryName") or "")
            elif isinstance(item, str):
                names.append(item)

        return [n for n in names if n]

    async def get_catalogue_products_by_category_name(self, name: str) -> list[CatalogProduct]:
        """
        Backend: GET /category/name/{name}
        Returns: CategoryCatalogueDto (must contain a list of catalogue products somewhere)
        """
        dto = await self.api.get(f"category/name/{name}")

        # We don't know your exact JSON shape, so we try common keys.
        # If it fails, raise with the DTO so you can see what key it actually uses.
        candidates = ["products", "catalogueProducts", "catalogProducts", "items"]
        products_payload = None
        if isinstance(dto, dict):
            for key in candidates:
                if key in dto:
                    products_payload = dto[key]
                    break

        if not isinstance(products_payload, list):
            raise RuntimeError(
                f"Unexpected CategoryCatalogueDto shape. Expected one of keys {candidates} to be a list, got: {dto}"
            )

        return [CatalogProduct(item) for item in products_payload]