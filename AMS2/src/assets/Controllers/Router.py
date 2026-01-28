from urllib.parse import urlparse, parse_qs
import flet as ft
from AMS2.src.assets.Controllers.ProcuctViewController import ProductViewController
from AMS2.src.assets.Views import AGBView
from AMS2.src.assets.Views.ProductView import ProductView
from AMS2.src.assets.Views.StartpageView import StartpageView
from AMS2.src.assets.Views.CatalogView import CatalogView
from AMS2.src.assets.Views.ImpressumView import ImpressumView
from AMS2.src.assets.Views.AGBView import AGBView

def route_change(e):
    page = e.page
    page.views.clear()

    parsed = urlparse(page.route)
    path = parsed.path
    query = parse_qs(parsed.query)

    match path:
        case ("/") :
            page.views.append(
                ft.View(
                    route="/startpage",
                    controls=[StartpageView(page).build()],
                )
            )
        case "/catalog":
            page.views.append(
                ft.View(
                    route="/catalog",
                    controls=[CatalogView(page).build()],
                )
            )

        case "/product":
            product_id = query.get("productid", [None])[0]
            if not product_id:
                page.go("/catalog")
                return

            product = page.session.get("current_product")
            cart = page.session.get("cart")

            controller = ProductViewController(product, cart)

            view = ProductView(
                product=product,
                on_variant_selected=controller.on_variant_selected,
                on_add_to_cart=controller.add_to_cart
            )

            page.views.append(
                ft.View(
                    route="/product",
                    controls=[view(page).build()],
                )
            )

        case "/impressum":
            page.views.append(
                ft.View(
                    route="/impressum",
                    controls=[ImpressumView(page).build()],
                )
            )

        case "/agb":
            page.views.append(AGBView(page).build())

        case _:
            page.go("/")


    page.update()