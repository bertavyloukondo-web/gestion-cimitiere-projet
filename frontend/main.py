import flet as ft
from pages.login import LoginPage
from pages.dashboard import DashboardPage
from pages.carte import CartePage
from pages.reservations import ReservationsPage
from pages.nouvelle_reservation import NouvelleReservationPage
from pages.finance import FinancePage
from pages.utilisateurs import UtilisateursPage
from pages.concessions import ConcessionsPage
from pages.inscription import InscriptionPage
from pages.comptabilite import ComptabilitePage

user_data_global = {}

def main(page: ft.Page):
    page.title = "Gestion de Cimetière"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = "#F5F5F5"

    def toggle_theme():
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            page.bgcolor = "#121212"
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.bgcolor = "#F5F5F5"
        page.update()
        route_change(None)

    def route_change(e):
        page.views.clear()
        if page.route == "/" or page.route == "/login":
            page.views.append(LoginPage(page, go_to_dashboard))
        elif page.route == "/dashboard":
            page.views.append(DashboardPage(page, user_data_global, toggle_theme))
        elif page.route == "/carte":
            page.views.append(CartePage(page, user_data_global))
        elif page.route == "/reservations":
            page.views.append(ReservationsPage(page, user_data_global))
        elif page.route == "/nouvelle_reservation":
            page.views.append(NouvelleReservationPage(page, user_data_global))
        elif page.route == "/finance":
            page.views.append(FinancePage(page, user_data_global))
        elif page.route == "/utilisateurs":
            page.views.append(UtilisateursPage(page, user_data_global))
        elif page.route == "/concessions":
            page.views.append(ConcessionsPage(page, user_data_global))
        elif page.route == "/inscription":
            page.views.append(InscriptionPage(page))
        elif page.route == "/comptabilite":
            page.views.append(ComptabilitePage(page, user_data_global))
        page.update()

    def go_to_dashboard(user_data):
        user_data_global.update(user_data)
        page.go("/dashboard")

    page.on_route_change = route_change
    page.go("/login")


ft.run(main)