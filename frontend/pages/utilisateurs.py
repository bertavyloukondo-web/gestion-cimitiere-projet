import flet as ft
import httpx


API_URL = "https://gestion-cimitiere-backend.onrender.com/api"


class UtilisateursPage(ft.View):
    def __init__(self, page: ft.Page, user_data: dict):
        super().__init__(route="/utilisateurs", padding=0)
        self._pg = page
        self.user = user_data
        self.bgcolor = "#F0F2F5"
        self.utilisateurs = []

        self.recherche = ft.TextField(
            hint_text="Rechercher par nom ou email...",
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
                                    ft.Icon(ft.Icons.PEOPLE, color="white", size=25),
                                    ft.Text("Gestion des Utilisateurs", color="white", size=18, weight=ft.FontWeight.BOLD),
                                ]),
                                ft.ElevatedButton(
                                    content=ft.Row(controls=[
                                        ft.Icon(ft.Icons.PERSON_ADD, color="white"),
                                        ft.Text("Nouveau", color="white"),
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
                        content=self.recherche,
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
        self.charger_utilisateurs()

    def charger_utilisateurs(self):
        try:
            res = httpx.get(
    f"{API_URL}/users/list",
    timeout=30
)
            self.utilisateurs = res.json()
            self.afficher_utilisateurs()
        except Exception as ex:
            self.message.value = f"Erreur : {ex}"
            self._pg.update()

    def rechercher(self, e):
        terme = self.recherche.value.lower().strip()
        if not terme:
            self.afficher_liste(self.utilisateurs)
            return
        filtres = [
            u for u in self.utilisateurs
            if terme in u.get("username", "").lower() or terme in u.get("email", "").lower()
        ]
        self.afficher_liste(filtres)

    def afficher_utilisateurs(self):
        self.afficher_liste(self.utilisateurs)

    def afficher_liste(self, utilisateurs):
        self.liste.controls.clear()
        if not utilisateurs:
            self.liste.controls.append(
                ft.Text("Aucun utilisateur trouvé", color="#555555", size=14)
            )
        for u in utilisateurs:
            couleur_role = {
                "admin": "#1A237E",
                "agent": "#4CAF50",
                "secretariat": "#FF9800",
                "client": "#9C27B0",
            }.get(u["role"], "#9E9E9E")

            role_label = {
                "admin": "ADMIN",
                "agent": "AGENT",
                "secretariat": "SECRÉTARIAT",
                "client": "CLIENT",
            }.get(u["role"], u["role"].upper())

            statut_couleur = {
                "approuve": "#4CAF50",
                "en_attente": "#FF9800",
                "refuse": "#F44336",
            }.get(u.get("statut", ""), "#9E9E9E")

            statut_label = {
                "approuve": "APPROUVÉ",
                "en_attente": "EN ATTENTE",
                "refuse": "REFUSÉ",
            }.get(u.get("statut", ""), u.get("statut", "").upper())

            self.liste.controls.append(
                ft.Container(
                    bgcolor="white",
                    border_radius=10,
                    padding=15,
                    margin=ft.Margin(0, 0, 0, 10),
                    border=ft.Border(left=ft.BorderSide(4, couleur_role)),
                    shadow=ft.BoxShadow(blur_radius=5, color="#CCCCCC"),
                    content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Row(controls=[
                                ft.CircleAvatar(
                                    content=ft.Text(u["username"][0].upper(), color="white", weight=ft.FontWeight.BOLD),
                                    bgcolor=couleur_role,
                                    radius=25,
                                ),
                                ft.Container(width=10),
                                ft.Column(controls=[
                                    ft.Text(u["username"], weight=ft.FontWeight.BOLD, size=16, color="#1A237E"),
                                    ft.Text(u["email"], color="#555555", size=12),
                                    ft.Text(u.get("phone") or "Pas de téléphone", color="#888888", size=12),
                                ]),
                            ]),
                            ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.END,
                                controls=[
                                    ft.Container(
                                        bgcolor=couleur_role,
                                        border_radius=5,
                                        padding=ft.Padding(10, 5, 10, 5),
                                        content=ft.Text(role_label, color="white", size=11, weight=ft.FontWeight.BOLD),
                                    ),
                                    ft.Container(
                                        bgcolor=statut_couleur,
                                        border_radius=5,
                                        padding=ft.Padding(10, 3, 10, 3),
                                        margin=ft.Margin(0, 5, 0, 0),
                                        content=ft.Text(statut_label, color="white", size=10),
                                    ),
                                    ft.Row(
                                        controls=[
                                            ft.IconButton(
                                                ft.Icons.CHECK_CIRCLE,
                                                icon_color="#4CAF50",
                                                tooltip="Approuver",
                                                visible=u["statut"] == "en_attente",
                                                on_click=lambda e, uid=u["id"]: self.approuver(uid),
                                            ),
                                            ft.IconButton(
                                                ft.Icons.CANCEL,
                                                icon_color="#F44336",
                                                tooltip="Refuser",
                                                visible=u["statut"] == "en_attente",
                                                on_click=lambda e, uid=u["id"]: self.refuser_compte(uid),
                                            ),
                                        ]
                                    )
                                ]
                            ),
                        ]
                    )
                )
            )
        self._pg.update()

    def approuver(self, user_id):
        try:
            httpx.put(
    f"{API_URL}/users/{user_id}/approuver",
    timeout=30
)
            self.charger_utilisateurs()
        except Exception as ex:
            self.message.value = f"Erreur : {ex}"
            self._pg.update()

    def refuser_compte(self, user_id):
        try:
            httpx.put(
    f"{API_URL}/users/{user_id}/refuser",
    timeout=30
)
            self.charger_utilisateurs()
        except Exception as ex:
            self.message.value = f"Erreur : {ex}"
            self._pg.update()

    def ouvrir_formulaire(self, e):
        def creer_utilisateur(e):
            if not all([username.value, email.value, password.value]):
                msg.value = "Remplissez tous les champs !"
                self._pg.update()
                return
            try:
                httpx.post(
    f"{API_URL}/users/register",
    json={
        "username": username.value,
        "email": email.value,
        "password": password.value,
        "role": role.value or "client",
        "phone": phone.value,
    },
    timeout=30
)
                dlg.open = False
                self._pg.update()
                self.charger_utilisateurs()
            except Exception as ex:
                msg.value = f"Erreur : {ex}"
                self._pg.update()

        username = ft.TextField(label="Nom d'utilisateur", width=280)
        email = ft.TextField(label="Email", width=280)
        password = ft.TextField(label="Mot de passe", password=True, width=280)
        phone = ft.TextField(label="Téléphone", width=280)
        role = ft.Dropdown(
            label="Rôle",
            width=280,
            options=[
                ft.dropdown.Option("admin", "Administrateur"),
                ft.dropdown.Option("agent", "Agent de terrain"),
                ft.dropdown.Option("secretariat", "Secrétariat"),
                ft.dropdown.Option("client", "Client"),
            ]
        )
        msg = ft.Text(color="red", size=12)

        dlg = ft.AlertDialog(
            title=ft.Text("Nouvel utilisateur"),
            content=ft.Column(
                controls=[username, email, password, phone, role, msg],
                tight=True,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.ElevatedButton(
                    content=ft.Text("Annuler", color="white"),
                    style=ft.ButtonStyle(bgcolor="#F44336"),
                    on_click=lambda e: setattr(dlg, 'open', False) or self._pg.update()
                ),
                ft.ElevatedButton(
                    content=ft.Text("Créer", color="white"),
                    style=ft.ButtonStyle(bgcolor="#1A237E"),
                    on_click=creer_utilisateur
                ),
            ]
        )
        self._pg.overlay.append(dlg)
        dlg.open = True
        self._pg.update()

    def go_back(self, e):
        self._pg.go("/dashboard")