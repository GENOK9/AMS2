import flet as ft


class ImpressumView:
    def build(self):
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "Impressum",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Divider(height=20),

                ft.Text("Angaben gemäß § 5 TMG", size=18, weight=ft.FontWeight.BOLD),
                ft.Text("ATOW GmbH"),
                ft.Text("Riemekestr. 160"),
                ft.Text("33106 Paderborn"),

                ft.Container(height=20),

                ft.Text("Vertreten durch:", size=18, weight=ft.FontWeight.BOLD),
                ft.Text("Adrian Jaeschke, Timothy Schoettl"),

                ft.Container(height=20),

                ft.Text("Kontakt:", size=18, weight=ft.FontWeight.BOLD),
                ft.Text("Telefon: +49 175 1095456"),
                ft.Text("E-Mail: info@atow.de"),

                ft.Container(height=20),

                ft.Text("Registereintrag:", size=18, weight=ft.FontWeight.BOLD),
                ft.Text("Eintragung im Handelsregister"),
                ft.Text("Registergericht: Amtsgericht Musterstadt"),
                ft.Text("Registernummer: HRB 12345"),

                ft.Container(height=20),

                ft.Text("Umsatzsteuer-ID:", size=18, weight=ft.FontWeight.BOLD),
                ft.Text("Umsatzsteuer-Identifikationsnummer gemäß § 27a Umsatzsteuergesetz:"),
                ft.Text("DE123456789"),

                ft.Container(height=20),

                ft.Text("Verantwortlich für den Inhalt nach § 55 Abs. 2 RStV:", size=18, weight=ft.FontWeight.BOLD),
                ft.Text("ATIW Berufskolleg GmbH"),
                ft.Text("Technologiepark neben dem Kreisverkehr"),
                ft.Text("33102 Paderborn"),

            ], spacing=5, scroll=ft.ScrollMode.AUTO),
            padding=ft.padding.all(40),
            expand=True,
        )