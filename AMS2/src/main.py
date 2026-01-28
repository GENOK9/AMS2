import flet as ft
from AMS2.src.assets.Controllers.Router import route_change
from AMS2.src.assets.ShopLogic.Shoppingcart import Shoppingcart


def main(page: ft.Page):
    cart = Shoppingcart(page)
    page.overlay.append(cart.toggle_cart_button(page))
    page.on_route_change = route_change
    page.go("/")


ft.app(main)