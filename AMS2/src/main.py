import flet as ft
from flet.core.types import WEB_BROWSER

from AMS2.src.assets.ApiServices.ApiService import ApiService
from AMS2.src.assets.ApiServices.OrderService import OrderService
from AMS2.src.assets.ApiServices.ProductService import ProductService
from AMS2.src.assets.Controllers.Router import Router
from AMS2.src.assets.Controllers.StartpageController import StartpageController
from AMS2.src.assets.Controllers.ProcuctViewController import ProductViewController
from AMS2.src.assets.Controllers.CatalogViewController import CatalogViewController
from AMS2.src.assets.ShopLogic.Shoppingcart import Shoppingcart
from AMS2.src.assets.Views.GlobalGui import GlobalAppBar
from AMS2.src.assets.ApiServices.CategoryService import CategoryService



async def main(page: ft.Page):
    api = ApiService()
    order_service = OrderService(api)
    product_service = ProductService(api)
    cart = Shoppingcart(page, order_service, product_service)
    product_controller = ProductViewController(product_service, cart)
    catalog_controller = CatalogViewController(product_service, CategoryService)
    startpage_controller = StartpageController(product_service, page)

    router = Router(
        page=page,
        cart=cart,
        startpage_controller=startpage_controller,
        product_controller=product_controller,
        catalog_controller=catalog_controller,
    )

    await cart.build_cart_content()
    global_appbar = GlobalAppBar(page, cart, router)
    page.appbar = global_appbar.build()
    page.on_route_change = router.route_change
    page.go("/")

ft.app(main, port= 4200, view=ft.AppView(WEB_BROWSER))
#ft.app(main)