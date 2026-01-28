import flet as ft
from AMS2.src.assets.Views import AGBView
from AMS2.src.assets.Views.DataProtectionView import DataProtectionView
from AMS2.src.assets.Views.ProductView import ProductView
from AMS2.src.assets.Views.StartpageView import StartpageView
from AMS2.src.assets.Views.CatalogView import CatalogView
from AMS2.src.assets.Views.ImpressumView import ImpressumView
from AMS2.src.assets.Views.AGBView import AGBView


class Router:
    def __init__(
        self,
        startpage_controller,
        page: ft.Page,
        cart,
        catalog_controller,
        product_controller,
    ):
        self.startpage_controller = startpage_controller
        self.page = page
        self.cart = cart
        self.catalog_controller = catalog_controller
        self.product_controller = product_controller

    async def route_change(self, e: ft.RouteChangeEvent):
        self.page.views.clear()

        match True:

            #  STARTPAGE
            case _ if self.page.route == "/":
                view = StartpageView(
                    page=self.page,
                    controller=self.startpage_controller)

                self.page.views.append(
                    ft.View(
                        route="/",
                        controls=[await view.build()],
                    )
                )

            #  CATALOG
            case _ if self.page.route == "/catalog":
                view = CatalogView(
                    page=self.page,
                    controller=self.catalog_controller,
                )

                self.page.views.append(
                    ft.View(
                        route="/",
                        controls=[await view.build()],
                    )
                )

            #  PRODUCT DETAIL
            case _ if self.page.route.startswith("/product"):
                try:
                    product_id = int(self.page.route.split("product?productid=")[-1])
                except  (ValueError, IndexError):
                    self.page.go("/")
                    return

                view = ProductView(
                    page=self.page,
                    controller=self.product_controller,
                    product_id=product_id,
                )

                self.page.views.append(
                    ft.View(
                        route=self.page.route,
                        controls=[await view.build()],
                    )
                )

            #  AGB
            case _ if self.page.route == "/agb":
                self.page.views.append(
                    ft.View(
                        route="/agb",
                        controls=AGBView().build()
                    )
                )

            #  IMPRESSUM
            case _ if self.page.route == "/impressum":
                self.page.views.append(
                    ft.View(
                        route="/impressum",
                        controls=ImpressumView().build()
                    )
                )

            #  DATA PROTECTION
            case _ if self.page.route == "/dataprotection":
                self.page.views.append(
                    ft.View(
                        route="/dataprotection",
                        controls=DataProtectionView().build()
                    )
                )

        self.page.update()