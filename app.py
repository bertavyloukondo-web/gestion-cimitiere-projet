import flet as ft

def main(page: ft.Page):
    page.title = "Ma première app Flet"
    page.add(ft.Text("🎉 Flet fonctionne !"))

ft.app(target=main)