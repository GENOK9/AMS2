import flet as ft

from AMS2.src.assets.ApiServices.ApiService import ApiService
from AMS2.src.assets.ApiServices.OrderService import OrderService
from AMS2.src.assets.ApiServices.ProductService import ProductService
from AMS2.src.assets.Controllers.Router import Router
from AMS2.src.assets.Controllers.StartpageController import StartpageController
from AMS2.src.assets.Controllers.ProcuctViewController import ProductViewController
from AMS2.src.assets.Controllers.CatalogViewController import CatalogViewController
from AMS2.src.assets.ShopLogic.Shoppingcart import Shoppingcart
from AMS2.src.assets.Views.GlobalGui import GlobalAppBar


def main(page: ft.Page):
    api = ApiService()
    order_service = OrderService(api)
    product_service = ProductService(api)
    product_controller = ProductViewController(product_service)
    catalog_controller = CatalogViewController(product_service)
    startpage_controller = StartpageController(product_service)
    cart = Shoppingcart(page, order_service)

    # Global Appbar
    global_appbar = GlobalAppBar(page, cart)
    page.appbar = global_appbar.build()

    # Cart Overlay
    cart_panel = ft.Container(
        width=350,
        bgcolor=ft.Colors.BLUE_400,
        visible=False,
        content=ft.Column(),
    )
    cart.cart_panel = cart_panel
    page.overlay.append(cart_panel)

    router = Router(
        page=page,
        cart=cart,
        startpage_controller=startpage_controller,
        product_controller=product_controller,
        catalog_controller=catalog_controller,
    )

    page.on_route_change = router.route_change
    page.go("/")