import flet as ft
import httpx


API_URL = "https://gestion-cimitiere-backend.onrender.com/api"


class ReservationsPage(ft.View):
    def __init__(self, page: ft.Page, user_data: dict):
        super().__init__(route="/reservations", padding=0)
        self._pg = page
        self.user = user_data
        self.bgcolor = "#F0F2F5"
        self.reservations = []
        self.statut_actuel = None

        self.recherche = ft.TextField(
            hint_text="Rechercher par nom du défunt...",
            prefix_icon=ft.Icons.SEARCH,
            border_color="#1A237E",
            width=400,
            on_change=self.rechercher,
        )

        self.liste = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.message = ft.Text(color="red", size=13)

        self.controls = [
            ft.Column(
                expand=True,
                controls=[
                    ft.Container(
                        bgcolor="#1A237E",
                        padding=15,
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Row(controls=[
                                    ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=self.go_back),
                                    ft.Icon(ft.Icons.BOOK_ONLINE, color="white", size=25),
                                    ft.Text("Gestion des Réservations", color="white", size=18, weight=ft.FontWeight.BOLD),
                                ]),
                                ft.ElevatedButton(
                                    content=ft.Row(controls=[
                                        ft.Icon(ft.Icons.ADD, color="white"),
                                        ft.Text("Nouvelle", color="white"),
                                    ]),
                                    style=ft.ButtonStyle(bgcolor="#4CAF50"),
                                    on_click=self.ouvrir_formulaire,
                                ),
                            ]
                        )
                    ),
                    ft.Container(
                        padding=10,
                        bgcolor="#E8EAF6",
                        content=ft.Column(controls=[
                            self.recherche,
                            ft.Row(
                                controls=[
                                    ft.ElevatedButton(
                                        content=ft.Text("Toutes", color="white"),
                                        style=ft.ButtonStyle(bgcolor="#1A237E"),
                                        on_click=lambda e: self.filtrer(None)
                                    ),
                                    ft.ElevatedButton(
                                        content=ft.Text("En attente", color="white"),
                                        style=ft.ButtonStyle(bgcolor="#FF9800"),
                                        on_click=lambda e: self.filtrer("en_attente")
                                    ),
                                    ft.ElevatedButton(
                                        content=ft.Text("Validées", color="white"),
                                        style=ft.ButtonStyle(bgcolor="#4CAF50"),
                                        on_click=lambda e: self.filtrer("validee")
                                    ),
                                    ft.ElevatedButton(
                                        content=ft.Text("Refusées", color="white"),
                                        style=ft.ButtonStyle(bgcolor="#F44336"),
                                        on_click=lambda e: self.filtrer("refusee")
                                    ),
                                ]
                            ),
                        ])
                    ),
                    self.message,
                    ft.Container(
                        expand=True,
                        padding=10,
                        content=self.liste,
                    )
                ]
            )
        ]
        self.charger_reservations()

    def charger_reservations(self, statut=None):
        self.statut_actuel = statut
        try:
            url = f"{API_URL}/reservations/"
            if statut:
                url += f"?statut={statut}"
            res = httpx.get(url, timeout=30)
            self.reservations = res.json()
            self.afficher_reservations()
        except Exception as ex:
            self.message.value = f"Erreur : {ex}"
            self._pg.update()

    def rechercher(self, e):
        terme = self.recherche.value.lower().strip()
        if not terme:
            self.afficher_reservations()
            return
        filtrees = [
            r for r in self.reservations
            if terme in r.get("nom_defunt", "").lower() or terme in r.get("prenom_defunt", "").lower()
        ]
        self.afficher_liste(filtrees)

    def formater_date(self, date_str):
        try:
            from datetime import datetime
            d = datetime.strptime(date_str[:10], "%Y-%m-%d")
            return d.strftime("%d/%m/%Y")
        except:
            return date_str

    def afficher_reservations(self):
        self.afficher_liste(self.reservations)

    def afficher_liste(self, reservations):
        self.liste.controls.clear()
        if not reservations:
            self.liste.controls.append(
                ft.Text("Aucune réservation trouvée", color="#555555", size=14)
            )
        for r in reservations:
            couleur = {
                "en_attente": "#FF9800",
                "validee": "#4CAF50",
                "refusee": "#F44336",
                "annulee": "#9E9E9E"
            }.get(r["statut"], "#9E9E9E")

            statut_label = {
                "en_attente": "EN ATTENTE",
                "validee": "VALIDÉE",
                "refusee": "REFUSÉE",
                "annulee": "ANNULÉE"
            }.get(r["statut"], r["statut"].upper())

            self.liste.controls.append(
                ft.Container(
                    bgcolor="white",
                    border_radius=10,
                    padding=15,
                    margin=ft.Margin(0, 0, 0, 10),
                    border=ft.Border(left=ft.BorderSide(4, couleur)),
                    shadow=ft.BoxShadow(blur_radius=5, color="#CCCCCC"),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(controls=[
                                ft.Text(f"{r['nom_defunt']} {r['prenom_defunt']}", weight=ft.FontWeight.BOLD, size=16),
                                ft.Text(f"Caveau ID : {r['caveau_id']}", color="#555555", size=12),
                                ft.Text(f"Date : {self.formater_date(r['date_reservation'])}", color="#555555", size=12),
                            ]),
                            ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.END,
                                controls=[
                                    ft.Container(
                                        bgcolor=couleur,
                                        border_radius=5,
                                        padding=ft.Padding(10, 5, 10, 5),
                                        content=ft.Text(statut_label, color="white", size=11),
                                    ),
                                    ft.Row(controls=[
                                        ft.IconButton(
                                            ft.Icons.CHECK_CIRCLE,
                                            icon_color="#4CAF50",
                                            tooltip="Valider",
                                            on_click=lambda e, rid=r["id"]: self.valider(rid),
                                            visible=r["statut"] == "en_attente",
                                        ),
                                        ft.IconButton(
                                            ft.Icons.CANCEL,
                                            icon_color="#F44336",
                                            tooltip="Refuser",
                                            on_click=lambda e, rid=r["id"]: self.refuser(rid),
                                            visible=r["statut"] == "en_attente",
                                        ),
                                    ])
                                ]
                            )
                        ]
                    )
                )
            )
        self._pg.update()

    def filtrer(self, statut):
        self.recherche.value = ""
        self.charger_reservations(statut)

    def valider(self, reservation_id):
        try:
            httpx.put(
    f"{API_URL}/reservations/{reservation_id}/valider",
    params={"admin_id": self.user.get("user_id", 1)},
    timeout=30
)
            self.charger_reservations(self.statut_actuel)
        except Exception as ex:
            self.message.value = f"Erreur : {ex}"
            self._pg.update()

    def refuser(self, reservation_id):
        try:
            httpx.put(
    f"{API_URL}/reservations/{reservation_id}/refuser",
    timeout=30
)
            self.charger_reservations(self.statut_actuel)
        except Exception as ex:
            self.message.value = f"Erreur : {ex}"
            self._pg.update()

    def ouvrir_formulaire(self, e):
        self._pg.go("/nouvelle_reservation")

    def go_back(self, e):
        self._pg.go("/dashboard")