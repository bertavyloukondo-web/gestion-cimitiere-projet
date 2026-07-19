import flet as ft
import httpx


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

        est_dark = self._pg.theme_mode == ft.ThemeMode.DARK
        icone_theme = ft.Icons.DARK_MODE if not est_dark else ft.Icons.LIGHT_MODE

        self.controls = [
            ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Container(
                        bgcolor="#1A237E",
                        padding=20,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Row(controls=[
                                    ft.Icon(ft.Icons.LOCATION_CITY, color="white", size=35),
                                    ft.Text("Gestion de Cimetière", color="white", size=22, weight=ft.FontWeight.BOLD),
                                ]),
                                ft.Row(controls=[
                                    ft.Icon(ft.Icons.PERSON, color="white", size=25),
                                    ft.Text(f"Rôle : {self.user.get('role', '')}", color="white", size=14),
                                    ft.IconButton(
                                        icone_theme,
                                        icon_color="white",
                                        tooltip="Mode clair/sombre",
                                        on_click=lambda e: self.toggle_theme() if self.toggle_theme else None,
                                    ),
                                    ft.IconButton(ft.Icons.LOGOUT, icon_color="white", on_click=self.logout, tooltip="Déconnexion"),
                                ])
                            ]
                        )
                    ),
                    ft.Container(
                        padding=20,
                        bgcolor="#F0F2F5" if not est_dark else "#1E1E1E",
                        content=ft.Column(controls=[
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text("Tableau de bord", size=24, weight=ft.FontWeight.BOLD, color="#1A237E" if not est_dark else "white"),
                                    ft.IconButton(ft.Icons.REFRESH, icon_color="#1A237E" if not est_dark else "white", on_click=self.charger_stats, tooltip="Actualiser"),
                                ]
                            ),
                            ft.Row(
                                wrap=True,
                                controls=self.get_stat_cards()
                            ),
                            ft.Divider(height=10, color="#C5CAE9" if not est_dark else "#333333"),
                            ft.Text("Navigation", size=18, weight=ft.FontWeight.BOLD, color="#1A237E" if not est_dark else "white"),
                            ft.Container(
                                bgcolor="white" if not est_dark else "#2C2C2C",
                                border_radius=12,
                                padding=15,
                                content=ft.Row(
                                    wrap=True,
                                    controls=self.get_menu_cards()
                                )
                            ),
                            ft.Divider(height=10, color="#C5CAE9" if not est_dark else "#333333"),
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Text("Dernières réservations", size=18, weight=ft.FontWeight.BOLD, color="#1A237E" if not est_dark else "white"),
                                    ft.TextButton(
                                        content=ft.Text("Voir tout", color="#1A237E" if not est_dark else "#90CAF9"),
                                        on_click=lambda e: self.navigate("/reservations"),
                                    ),
                                ]
                            ),
                            ft.Container(
                                bgcolor="white" if not est_dark else "#2C2C2C",
                                border_radius=12,
                                padding=15,
                                content=self.liste_reservations,
                            ),
                        ])
                    )
                ]
            )
        ]
        self.charger_stats(None)

    def get_stat_cards(self):
        cards = [
            self.stat_card("Caveaux disponibles", self.stat_disponibles, ft.Icons.GRASS, "#4CAF50"),
            self.stat_card("Réservations en attente", self.stat_attente, ft.Icons.HOURGLASS_EMPTY, "#FF9800"),
            self.stat_card("Caveaux occupés", self.stat_occupes, ft.Icons.BLOCK, "#F44336"),
            self.stat_card("Non exploitables", self.stat_non_exploitable, ft.Icons.NOT_INTERESTED, "#9E9E9E"),
        ]
        if self.user.get("role") in ["admin", "secretariat"]:
            cards.append(
                self.stat_card("Recettes totales", self.stat_recettes, ft.Icons.ATTACH_MONEY, "#2196F3")
            )
        return cards

    def get_menu_cards(self):
        cards = [
            self.menu_card("Carte interactive", ft.Icons.MAP, "#1A237E", "/carte"),
            self.menu_card("Réservations", ft.Icons.BOOK_ONLINE, "#2E7D32", "/reservations"),
            self.menu_card("Concessions", ft.Icons.ASSIGNMENT, "#E65100", "/concessions"),
        ]
        if self.user.get("role") in ["admin", "secretariat"]:
            cards.append(self.menu_card("Finance", ft.Icons.ACCOUNT_BALANCE_WALLET, "#1565C0", "/finance"))
            cards.append(self.menu_card("Comptabilité", ft.Icons.ACCOUNT_BALANCE, "#00897B", "/comptabilite"))
        if self.user.get("role") == "admin":
            cards.append(self.menu_card("Utilisateurs", ft.Icons.PEOPLE, "#6A1B9A", "/utilisateurs"))
        return cards

    def formater_recettes(self, valeur):
        try:
            v = int(float(valeur))
            return f"{v:,} FCFA".replace(",", " ")
        except:
            return f"{valeur} FCFA"

    def charger_stats(self, e):
        try:
            res = httpx.get("http://127.0.0.1:8000/api/terrain/stats", timeout=10)
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
            res = httpx.get("http://127.0.0.1:8000/api/reservations/", timeout=10)
            reservations = res.json()[:5]
            self.liste_reservations.controls.clear()
            if not reservations:
                self.liste_reservations.controls.append(
                    ft.Text("Aucune réservation récente", color="#AAAAAA" if est_dark else "#555555", size=13)
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
                }.get(r.get("statut", ""), r.get("statut", "").upper())

                self.liste_reservations.controls.append(
                    ft.Container(
                        bgcolor="#3A3A3A" if est_dark else "#F5F5F5",
                        border_radius=8,
                        padding=12,
                        margin=ft.Margin(0, 0, 0, 8),
                        border=ft.Border(left=ft.BorderSide(4, couleur)),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(controls=[
                                    ft.Text(f"{r.get('nom_defunt', '')} {r.get('prenom_defunt', '')}", weight=ft.FontWeight.BOLD, size=14, color="white" if est_dark else "#000000"),
                                    ft.Text(f"Caveau ID : {r.get('caveau_id', '')}", color="#AAAAAA" if est_dark else "#555555", size=12),
                                ]),
                                ft.Container(
                                    bgcolor=couleur,
                                    border_radius=5,
                                    padding=ft.Padding(8, 4, 8, 4),
                                    content=ft.Text(statut_label, color="white", size=11),
                                ),
                            ]
                        )
                    )
                )
            self._pg.update()
        except Exception as ex:
            print(f"Erreur réservations : {ex}")

    def stat_card(self, title, value_widget, icon, color):
        est_dark = self._pg.theme_mode == ft.ThemeMode.DARK
        return ft.Container(
            width=210,
            height=105,
            bgcolor="#2C2C2C" if est_dark else "#EDEDEB",
            border_radius=12,
            padding=15,
            margin=5,
            border=ft.Border.all(1, color),
            shadow=ft.BoxShadow(
                blur_radius=8,
                color="#000000" if est_dark else "#BBBBBB",
                spread_radius=0,
            ),
            content=ft.Row(controls=[
                ft.Icon(icon, color=color, size=40),
                ft.Column(controls=[
                    ft.Text(title, size=11, color="#AAAAAA" if est_dark else "#555555", weight=ft.FontWeight.W_500),
                    value_widget,
                ])
            ])
        )

    def menu_card(self, title, icon, color, route=None):
        est_dark = self._pg.theme_mode == ft.ThemeMode.DARK
        return ft.Container(
            width=155,
            height=125,
            bgcolor=color,
            border_radius=12,
            padding=15,
            margin=5,
            shadow=ft.BoxShadow(
                blur_radius=8,
                color="#000000" if est_dark else "#BBBBBB",
                spread_radius=0,
            ),
            ink=True,
            on_click=lambda e, r=route: self.navigate(r) if r else None,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Icon(icon, color="white", size=45),
                    ft.Text(title, size=12, color="white", text_align=ft.TextAlign.CENTER, weight=ft.FontWeight.W_500),
                ]
            )
        )

    def navigate(self, route):
        self._pg.go(route)

    def logout(self, e):
        self._pg.go("/login")