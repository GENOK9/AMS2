import flet as ft


class AGBView:
    def build(self):
        return ft.Container(
            content=ft.Column([
                ft.Text(
                    "Allgemeine Geschäftsbedingungen (AGB)",
                    size=32,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Divider(height=20),

                ft.Text("§ 1 Geltungsbereich", size=20, weight=ft.FontWeight.BOLD),
                ft.Text(
                    "Diese Allgemeinen Geschäftsbedingungen gelten für alle Verträge, die zwischen "
                    "der Musterfirma GmbH nachfolgend und dem Kunden(nachfolgend „Kunde den Online-Shop des Verkäufers geschlossen werden."
        ),

        ft.Container(height=20),

        ft.Text("§ 2 Vertragsschluss", size=20, weight=ft.FontWeight.BOLD),
        ft.Text(
            "(1) Die Darstellung der Produkte im Online-Shop stellt kein rechtlich bindendes "
            "Angebot, sondern eine Aufforderung zur Bestellung dar."
        ),
        ft.Text(
            "(2) Durch Anklicken des Buttons „Bestellung aufgeben\" gibt der Kunde ein "
            "verbindliches Angebot zum Kauf der im Warenkorb befindlichen Waren ab."
        ),
        ft.Text(
            "(3) Der Verkäufer bestätigt den Eingang der Bestellung per E-Mail. Diese "
            "Bestellbestätigung stellt noch keine Annahme des Vertragsangebots dar."
        ),

        ft.Container(height=20),

        ft.Text("§ 3 Preise und Versandkosten", size=20, weight=ft.FontWeight.BOLD),
        ft.Text(
            "(1) Alle Preise sind Endpreise und enthalten die gesetzliche Mehrwertsteuer."
        ),
        ft.Text(
            "(2) Zusätzlich zu den angegebenen Preisen können Versandkosten anfallen. "
            "Die Versandkosten werden im Bestellvorgang deutlich mitgeteilt."
        ),

        ft.Container(height=20),

        ft.Text("§ 4 Lieferung und Verfügbarkeit", size=20, weight=ft.FontWeight.BOLD),
        ft.Text(
            "(1) Die Lieferung erfolgt innerhalb Deutschlands."
        ),
        ft.Text(
            "(2) Die Lieferzeit beträgt, soweit nicht anders angegeben, 3-5 Werktage."
        ),
        ft.Text(
            "(3) Ist die Lieferung der Ware durch Ausverkauf oder aus anderen Gründen nicht "
            "möglich, wird der Verkäufer den Kunden unverzüglich informieren."
        ),

        ft.Container(height=20),

        ft.Text("§ 5 Zahlung", size=20, weight=ft.FontWeight.BOLD),
        ft.Text(
            "(1) Die Zahlung erfolgt wahlweise per Vorkasse, Kreditkarte oder PayPal."
        ),
        ft.Text(
            "(2) Bei Zahlung per Vorkasse ist der Kaufpreis innerhalb von 7 Tagen nach "
            "Vertragsschluss zu zahlen."
        ),

        ft.Container(height=20),

        ft.Text("§ 6 Widerrufsrecht", size=20, weight=ft.FontWeight.BOLD),
        ft.Text(
            "Verbrauchern steht ein gesetzliches Widerrufsrecht zu. Nähere Informationen "
            "zum Widerrufsrecht ergeben sich aus der Widerrufsbelehrung."
        ),

        ft.Container(height=20),

        ft.Text("§ 7 Gewährleistung", size=20, weight=ft.FontWeight.BOLD),
        ft.Text(
            "Es gelten die gesetzlichen Gewährleistungsrechte. Die Gewährleistungsfrist "
            "beträgt 2 Jahre ab Erhalt der Ware."
        ),

        ft.Container(height=20),

        ft.Text("§ 8 Streitbeilegung", size=20, weight=ft.FontWeight.BOLD),
        ft.Text(
            "Die Europäische Kommission stellt eine Plattform zur Online-Streitbeilegung (OS) "
            "bereit: https://ec.europa.eu/consumers/odr"
        ),

        ], spacing = 5, scroll = ft.ScrollMode.AUTO),
        padding = ft.padding.all(40),
        expand = True,
        )