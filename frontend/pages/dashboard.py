import flet as ft
import httpx


API_URL = "https://gestion-cimitiere-backend.onrender.com/api"


class DashboardPage(ft.View):
    def __init__(self, page: ft.Page, user_data: dict, toggle_theme=None):
        super().__init__(route="/dashboard", padding=0)
        self._pg = page
        self.user = user_data
        self.toggle_theme = toggle_theme
        self.bgcolor = "#F0F2F5"

        self.stat_disponibles = ft.Text("...", size=22, weight=ft.FontWeight.BOLD, color="#4CAF50")
        self.stat_attente = ft.Text("...", size=22, weight=ft.FontWeight.BOLD, color="#FF9800")
        self.stat_occupes = ft.Text("...", size=22, weight=ft.FontWeight.BOLD, color="#F44336")
        self.stat_recettes = ft.Text("...", size=22, weight=ft.FontWeight.BOLD, color="#2196F3")
        self.stat_non_exploitable = ft.Text("...", size=22, weight=ft.FontWeight.BOLD, color="#9E9E9E")

        self.liste_reservations = ft.Column(scroll=ft.ScrollMode.AUTO)

        # ... tout le reste de ton code reste identique ...


    def charger_stats(self, e):
        try:
            res = httpx.get(
                f"{API_URL}/terrain/stats",
                timeout=30
            )

            data = res.json()

            self.stat_disponibles.value = str(data.get("caveaux_disponibles", 0))
            self.stat_attente.value = str(data.get("reservations_en_attente", 0))
            self.stat_occupes.value = str(data.get("caveaux_occupes", 0))
            self.stat_recettes.value = self.formater_recettes(data.get("recettes_totales", 0))
            self.stat_non_exploitable.value = str(data.get("caveaux_non_exploitables", 0))

            self._pg.update()

        except Exception as ex:
            print(f"Erreur stats : {ex}")

        self.charger_dernieres_reservations()



    def charger_dernieres_reservations(self):
        est_dark = self._pg.theme_mode == ft.ThemeMode.DARK

        try:
            res = httpx.get(
                f"{API_URL}/reservations/",
                timeout=30
            )

            reservations = res.json()[:5]

            self.liste_reservations.controls.clear()

            if not reservations:
                self.liste_reservations.controls.append(
                    ft.Text(
                        "Aucune réservation récente",
                        color="#AAAAAA" if est_dark else "#555555",
                        size=13
                    )
                )

            for r in reservations:
                couleur = {
                    "en_attente": "#FF9800",
                    "validee": "#4CAF50",
                    "refusee": "#F44336",
                }.get(r.get("statut", ""), "#9E9E9E")

                statut_label = {
                    "en_attente": "EN ATTENTE",
                    "validee": "VALIDÉE",
                    "refusee": "REFUSÉE",
                }.get(
                    r.get("statut", ""),
                    r.get("statut", "").upper()
                )

                self.liste_reservations.controls.append(
                    ft.Text(
                        f"{r.get('nom_defunt', '')} {r.get('prenom_defunt', '')} - {statut_label}"
                    )
                )

            self._pg.update()

        except Exception as ex:
            print(f"Erreur réservations : {ex}")