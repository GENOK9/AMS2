import flet as ft


class DataProtectionView:
    def build(self):
        return ft.Container(
            content=ft.Column([
                ft.Text("Datenschutzerklärung", size=32, weight=ft.FontWeight.BOLD),
                ft.Divider(height=20),
                ft.Text("Hier kommt der Datenschutztext"),
            ], spacing=10, scroll=ft.ScrollMode.AUTO),
            padding=ft.padding.all(40),
            expand=True,
        )