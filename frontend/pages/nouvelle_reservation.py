import flet as ft
import httpx


class NouvelleReservationPage(ft.View):
    def __init__(self, page: ft.Page, user_data: dict):
        super().__init__(route="/nouvelle_reservation", padding=0)
        self._pg = page
        self.user = user_data
        self.bgcolor = "#F0F2F5"
        self.caveaux = []

        self.nom = ft.TextField(label="Nom du défunt", border_color="#1A237E", label_style=ft.TextStyle(color="#1A237E"), width=420)
        self.prenom = ft.TextField(label="Prénom du défunt", border_color="#1A237E", label_style=ft.TextStyle(color="#1A237E"), width=420)
        self.sexe = ft.Dropdown(
            label="Sexe",
            width=420,
            border_color="#1A237E",
            label_style=ft.TextStyle(color="#1A237E"),
            options=[
                ft.dropdown.Option("masculin", "Masculin"),
                ft.dropdown.Option("feminin", "Féminin"),
            ]
        )
        self.date_naissance = ft.TextField(label="Date de naissance (JJ/MM/AAAA)", border_color="#1A237E", label_style=ft.TextStyle(color="#1A237E"), width=420)
        self.date_deces = ft.TextField(label="Date de décès (JJ/MM/AAAA)", border_color="#1A237E", label_style=ft.TextStyle(color="#1A237E"), width=420)
        self.caveau_dropdown = ft.Dropdown(
            label="Choisir un caveau disponible",
            width=420,
            border_color="#1A237E",
            label_style=ft.TextStyle(color="#1A237E"),
        )
        self.mode_paiement_dropdown = ft.Dropdown(
            label="Mode de paiement",
            width=420,
            border_color="#1A237E",
            label_style=ft.TextStyle(color="#1A237E"),
            options=[
                ft.dropdown.Option("mobile_money", "Mobile Money"),
                ft.dropdown.Option("airtel_money", "Airtel Money"),
                ft.dropdown.Option("especes", "Espèces"),
                ft.dropdown.Option("virement", "Virement"),
            ]
        )
        self.message = ft.Text(color="red", size=13)

        self.controls = [
            ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    ft.Container(
                        bgcolor="#1A237E",
                        padding=15,
                        content=ft.Row(controls=[
                            ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=self.go_back),
                            ft.Icon(ft.Icons.ADD_CIRCLE, color="white", size=25),
                            ft.Text("Nouvelle Réservation", color="white", size=18, weight=ft.FontWeight.BOLD),
                        ])
                    ),
                    ft.Container(
                        expand=True,
                        padding=30,
                        alignment=ft.Alignment(0, 0),
                        content=ft.Column(
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=15,
                            controls=[
                                ft.Container(
                                    width=460,
                                    bgcolor="white",
                                    border_radius=12,
                                    padding=25,
                                    shadow=ft.BoxShadow(blur_radius=5, color="#CCCCCC"),
                                    content=ft.Column(
                                        spacing=12,
                                        controls=[
                                            ft.Text("Informations du défunt", size=18, weight=ft.FontWeight.BOLD, color="#1A237E"),
                                            ft.Divider(color="#E0E0E0", height=1),
                                            self.nom,
                                            self.prenom,
                                            self.sexe,
                                            self.date_naissance,
                                            self.date_deces,
                                            ft.Divider(color="#E0E0E0", height=1),
                                            ft.Text("Caveau & Paiement", size=18, weight=ft.FontWeight.BOLD, color="#1A237E"),
                                            self.caveau_dropdown,
                                            self.mode_paiement_dropdown,
                                        ]
                                    )
                                ),
                                self.message,
                                ft.ElevatedButton(
                                    content=ft.Row(
                                        alignment=ft.MainAxisAlignment.CENTER,
                                        controls=[
                                            ft.Icon(ft.Icons.SEND, color="white"),
                                            ft.Text("Soumettre la réservation", color="white", weight=ft.FontWeight.BOLD),
                                        ]
                                    ),
                                    style=ft.ButtonStyle(
                                        bgcolor={
                                            ft.ControlState.HOVERED: "#0D1A6E",
                                            ft.ControlState.DEFAULT: "#1A237E",
                                        },
                                        overlay_color=ft.Colors.TRANSPARENT,
                                        shape=ft.RoundedRectangleBorder(radius=8),
                                    ),
                                    width=460,
                                    on_click=self.soumettre,
                                ),
                            ]
                        )
                    )
                ]
            )
        ]
        self.charger_caveaux()

    def charger_caveaux(self):
        try:
            res = httpx.get("http://127.0.0.1:8000/api/terrain/caveaux?etat=disponible", timeout=10)
            self.caveaux = res.json()
            self.caveau_dropdown.options = [
                ft.dropdown.Option(key=str(c["id"]), text=f"Caveau {c['numero']}")
                for c in self.caveaux
            ]
            self._pg.update()
        except Exception as ex:
            self.message.value = f"Erreur chargement caveaux : {ex}"
            self._pg.update()

    def convertir_date(self, date_str):
        try:
            from datetime import datetime
            d = datetime.strptime(date_str.strip(), "%d/%m/%Y")
            return d.strftime("%Y-%m-%d")
        except:
            return date_str

    def soumettre(self, e):
        if not all([self.nom.value, self.prenom.value, self.sexe.value, self.date_naissance.value, self.date_deces.value, self.caveau_dropdown.value, self.mode_paiement_dropdown.value]):
            self.message.value = "Veuillez remplir tous les champs !"
            self.message.color = "red"
            self._pg.update()
            return
        try:
            res = httpx.post(
                "http://127.0.0.1:8000/api/reservations/",
                json={
                    "client_id": self.user.get("user_id", 1),
                    "caveau_id": int(self.caveau_dropdown.value),
                    "nom_defunt": self.nom.value,
                    "prenom_defunt": self.prenom.value,
                    "sexe_defunt": self.sexe.value,
                    "date_naissance_defunt": self.convertir_date(self.date_naissance.value),
                    "date_deces_defunt": self.convertir_date(self.date_deces.value),
                    "mode_paiement_prefere": self.mode_paiement_dropdown.value,
                },
                timeout=10
            )
            if res.status_code == 200:
                self.message.value = "Réservation soumise avec succès !"
                self.message.color = "green"
                self._pg.update()
                self.go_back(None)
            else:
                self.message.value = f"Erreur : {res.text}"
                self.message.color = "red"
                self._pg.update()
        except Exception as ex:
            self.message.value = f"Erreur : {ex}"
            self.message.color = "red"
            self._pg.update()

    def go_back(self, e):
        self._pg.go("/reservations")