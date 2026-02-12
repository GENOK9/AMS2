from AMS2.src.assets.ShopLogic.CatalogProduct import CatalogProduct


class CatalogViewController:
    def __init__(self, product_service, category_service):
        self.product_service = product_service
        self.category_service = category_service
        self.selected_category: str = "Alles"

    async def load_products(self) -> list[CatalogProduct]:
        try:
            if self.selected_category and self.selected_category != "Alles":
                return await self.category_service.get_catalogue_products_by_category_name(self.selected_category)

            self.selected_category = None
            return await self.product_service.get_all_products()

        except Exception as e:
            raise RuntimeError("Produkte konnten nicht geladen werden") from e

    def sort_products(self, products: list, mode: str):
        if mode == "price_asc":
            return sorted(products, key=lambda p: p.price)
        if mode == "price_desc":
            return sorted(products, key=lambda p: p.price, reverse=True)
        return products