import flet as ft
import httpx


class ConcessionsPage(ft.View):
    def __init__(self, page: ft.Page, user_data: dict):
        super().__init__(route="/concessions", padding=0)
        self._pg = page
        self.user = user_data
        self.bgcolor = "#F0F2F5"
        self.concessions = []
        self.onglet = "concessions"

        self.liste = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.message = ft.Text(color="red", size=13)
        self.dialog = ft.AlertDialog(modal=True)

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
                                    ft.Icon(ft.Icons.ASSIGNMENT, color="white", size=25),
                                    ft.Text("Concessions & Exhumations", color="white", size=18, weight=ft.FontWeight.BOLD),
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
                        content=ft.Row(controls=[
                            ft.ElevatedButton(
                                content=ft.Text("Concessions", color="white"),
                                style=ft.ButtonStyle(bgcolor="#1A237E"),
                                on_click=lambda e: self.changer_onglet("concessions"),
                            ),
                            ft.ElevatedButton(
                                content=ft.Text("Exhumations", color="white"),
                                style=ft.ButtonStyle(bgcolor="#FF9800"),
                                on_click=lambda e: self.changer_onglet("exhumations"),
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
        self.charger_concessions()

    def changer_onglet(self, onglet):
        self.onglet = onglet
        if onglet == "concessions":
            self.charger_concessions()
        else:
            self.charger_exhumations()

    def formater_date(self, date_str):
        try:
            from datetime import datetime
            d = datetime.strptime(date_str[:10], "%Y-%m-%d")
            return d.strftime("%d/%m/%Y")
        except:
            return date_str if date_str else "—"

    def charger_concessions(self):
        try:
            res = httpx.get("http://127.0.0.1:8000/api/concessions/", timeout=10)
            self.concessions = res.json()
            self.afficher_concessions()
        except Exception as ex:
            self.message.value = f"Erreur : {ex}"
            self._pg.update()

    def charger_exhumations(self):
        try:
            res = httpx.get("http://127.0.0.1:8000/api/concessions/exhumations", timeout=10)
            if res.status_code != 200 or not res.text.strip():
                self.liste.controls.clear()
                self.liste.controls.append(
                    ft.Text("Aucune exhumation trouvée", color="#555555", size=14)
                )
                self._pg.update()
                return
            data = res.json()
            self.liste.controls.clear()
            if not data:
                self.liste.controls.append(
                    ft.Text("Aucune exhumation trouvée", color="#555555", size=14)
                )
            for ex in data:
                self.liste.controls.append(
                    ft.Container(
                        bgcolor="white",
                        border_radius=10,
                        padding=15,
                        margin=ft.Margin(0, 0, 0, 10),
                        border=ft.Border(left=ft.BorderSide(4, "#FF9800")),
                        shadow=ft.BoxShadow(blur_radius=5, color="#CCCCCC"),
                        content=ft.Column(controls=[
                            ft.Text(f"Concession ID : {ex.get('concession_id', '')}", weight=ft.FontWeight.BOLD),
                            ft.Text(f"Motif : {ex.get('motif', '')}", color="#555555", size=12),
                            ft.Text(f"Statut : {ex.get('statut', '')}", color="#555555", size=12),
                        ])
                    )
                )
            self._pg.update()
        except Exception as ex:
            self.liste.controls.clear()
            self.liste.controls.append(
                ft.Text("Aucune exhumation trouvée", color="#555555", size=14)
            )
            self._pg.update()

    def afficher_concessions(self):
        self.liste.controls.clear()
        if not self.concessions:
            self.liste.controls.append(
                ft.Text("Aucune concession trouvée", color="#555555", size=14)
            )
        for c in self.concessions:
            self.liste.controls.append(
                ft.Container(
                    bgcolor="white",
                    border_radius=10,
                    padding=15,
                    margin=ft.Margin(0, 0, 0, 10),
                    border=ft.Border(left=ft.BorderSide(4, "#FF9800")),
                    shadow=ft.BoxShadow(blur_radius=5, color="#CCCCCC"),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Column(controls=[
                                ft.Text(f"Concession #{c['id']}", weight=ft.FontWeight.BOLD, size=16),
                                ft.Text(f"Caveau ID : {c.get('caveau_id', '')}", color="#555555", size=12),
                                ft.Text(f"Type : {c.get('type_concession', '')}", color="#555555", size=12),
                                ft.Text(f"Début : {self.formater_date(c.get('date_debut', ''))}", color="#555555", size=12),
                                ft.Text(f"Fin : {self.formater_date(c.get('date_fin', '')) if c.get('date_fin') else 'Perpétuelle'}", color="#555555", size=12),
                            ]),
                            ft.Container(
                                bgcolor="#FF9800",
                                border_radius=5,
                                padding=ft.Padding(10, 5, 10, 5),
                                content=ft.Text(c.get("type_concession", "").upper(), color="white", size=11),
                            ),
                        ]
                    )
                )
            )
        self._pg.update()

    def ouvrir_formulaire(self, e):
        id_reservation = ft.TextField(label="ID Réservation", border_color="#1A237E", label_style=ft.TextStyle(color="#1A237E"))
        id_caveau = ft.TextField(label="ID Caveau", border_color="#1A237E", label_style=ft.TextStyle(color="#1A237E"))
        type_concession = ft.Dropdown(
            label="Type de concession",
            border_color="#1A237E",
            label_style=ft.TextStyle(color="#1A237E"),
            options=[
                ft.dropdown.Option("temporaire", "Temporaire"),
                ft.dropdown.Option("perpetuelle", "Perpétuelle"),
            ]
        )
        date_debut = ft.TextField(label="Date début (JJ/MM/AAAA)", border_color="#1A237E", label_style=ft.TextStyle(color="#1A237E"))
        date_fin = ft.TextField(label="Date fin (JJ/MM/AAAA, vide si perpétuelle)", border_color="#1A237E", label_style=ft.TextStyle(color="#1A237E"))
        msg = ft.Text(color="red", size=12)

        def convertir_date(date_str):
            try:
                from datetime import datetime
                d = datetime.strptime(date_str.strip(), "%d/%m/%Y")
                return d.strftime("%Y-%m-%d")
            except:
                return date_str

        def creer(e):
            msg.value = ""
            try:
                payload = {
                    "reservation_id": int(id_reservation.value),
                    "caveau_id": int(id_caveau.value),
                    "type_concession": type_concession.value,
                    "date_debut": convertir_date(date_debut.value),
                    "date_fin": convertir_date(date_fin.value) if date_fin.value else None,
                }
                res = httpx.post("http://127.0.0.1:8000/api/concessions/", json=payload, timeout=10)
                if res.status_code in [200, 201]:
                    self.dialog.open = False
                    self._pg.update()
                    self.charger_concessions()
                else:
                    msg.value = str(res.json())
                    self._pg.update()
            except Exception as ex:
                msg.value = f"Erreur : {ex}"
                self._pg.update()

        def annuler(e):
            self.dialog.open = False
            self._pg.update()

        self.dialog.title = ft.Text("Nouvelle concession", weight=ft.FontWeight.BOLD, color="#1A237E")
        self.dialog.content = ft.Column(
            tight=True,
            controls=[id_reservation, id_caveau, type_concession, date_debut, date_fin, msg]
        )
        self.dialog.actions = [
            ft.TextButton(content=ft.Text("Annuler", color="#F44336"), on_click=annuler),
            ft.ElevatedButton(
                content=ft.Text("Créer", color="white"),
                style=ft.ButtonStyle(bgcolor="#1A237E"),
                on_click=creer,
            ),
        ]
        self.dialog.open = True
        self._pg.overlay.append(self.dialog)
        self._pg.update()

    def go_back(self, e):
        self._pg.go("/dashboard")