import flet as ft
import httpx
import base64


GOOGLE_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="28" height="28">
<path fill="#FFC107" d="M43.611,20.083H42V20H24v8h11.303c-1.649,4.657-6.08,8-11.303,8c-6.627,0-12-5.373-12-12
c0-6.627,5.373-12,12-12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24
c0,11.045,8.955,20,20,20c11.045,0,20-8.955,20-20C44,22.659,43.862,21.35,43.611,20.083z"/>
<path fill="#FF3D00" d="M6.306,14.691l6.571,4.819C14.655,15.108,18.961,12,24,12c3.059,0,5.842,1.154,7.961,3.039
l5.657-5.657C34.046,6.053,29.268,4,24,4C16.318,4,9.656,8.337,6.306,14.691z"/>
<path fill="#4CAF50" d="M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.19-5.238C29.211,35.091,26.715,36,24,36
c-5.202,0-9.619-3.317-11.283-7.946l-6.522,5.025C9.505,39.556,16.227,44,24,44z"/>
<path fill="#1976D2" d="M43.611,20.083H42V20H24v8h11.303c-0.792,2.237-2.231,4.166-4.087,5.571
c0.001-0.001,0.002-0.001,0.003-0.002l6.19,5.238C36.971,39.205,44,34,44,24
C44,22.659,43.862,21.35,43.611,20.083z"/>
</svg>"""

FACEBOOK_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="28" height="28">
<path fill="#1877F2" d="M24,12.073c0-6.627-5.373-12-12-12s-12,5.373-12,12c0,5.99,4.388,10.954,10.125,11.854
v-8.385H7.078v-3.47h3.047V9.43c0-3.007,1.792-4.669,4.533-4.669c1.312,0,2.686,0.234,2.686,0.234v2.953H15.83
c-1.491,0-1.956,0.925-1.956,1.875v2.25h3.328l-0.532,3.47h-2.796v8.385
C19.612,23.027,24,18.062,24,12.073z"/>
</svg>"""

TWITTER_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
<rect width="24" height="24" rx="4" fill="#000000"/>
<path fill="#FFFFFF" d="M17.751,6.022h2.117l-4.624,5.286l5.443,7.198h-4.262l-3.338-4.366l-3.821,4.366H5.148
l4.946-5.654L4.86,6.022h4.371l3.016,3.989L17.751,6.022z M16.617,17.146h1.173L8.437,7.166H7.18L16.617,17.146z"/>
</svg>"""


class InscriptionPage(ft.View):
    def __init__(self, page: ft.Page):
        super().__init__(route="/inscription", padding=0)
        self._pg = page
        self.bgcolor = "#1A237E"

        self.username = ft.TextField(
            label="Nom d'utilisateur",
            border_color="white",
            label_style=ft.TextStyle(color="white"),
            color="white",
            cursor_color="white",
            width=320,
        )
        self.email = ft.TextField(
            label="Email",
            border_color="white",
            label_style=ft.TextStyle(color="white"),
            color="white",
            cursor_color="white",
            width=320,
        )
        self.password = ft.TextField(
            label="Mot de passe",
            password=True,
            can_reveal_password=True,
            border_color="white",
            label_style=ft.TextStyle(color="white"),
            color="white",
            cursor_color="white",
            width=320,
        )
        self.phone = ft.TextField(
            label="Téléphone",
            border_color="white",
            label_style=ft.TextStyle(color="white"),
            color="white",
            cursor_color="white",
            width=320,
        )
        self.message = ft.Text(color="red", size=13)

        self.controls = [
            ft.Container(
                expand=True,
                alignment=ft.Alignment(0, 0),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.PERSON_ADD, color="white", size=60),
                        ft.Text("Créer un compte", color="white", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Inscrivez-vous en tant que client", color="white70", size=14),
                        ft.Divider(color="transparent", height=20),
                        self.username,
                        self.email,
                        self.password,
                        self.phone,
                        self.message,
                        ft.ElevatedButton(
                            content=ft.Text("S'inscrire", color="#1A237E", weight=ft.FontWeight.BOLD),
                            width=320,
                            style=ft.ButtonStyle(
                                bgcolor={
                                    ft.ControlState.HOVERED: "#FFD700",
                                    ft.ControlState.DEFAULT: ft.Colors.WHITE,
                                },
                                overlay_color=ft.Colors.TRANSPARENT,
                            ),
                            on_click=self.handle_inscription,
                        ),
                        ft.TextButton(
                            content=ft.Text("Déjà un compte ? Se connecter", color="white"),
                            style=ft.ButtonStyle(
                                overlay_color=ft.Colors.TRANSPARENT,
                            ),
                            on_click=self.go_to_login,
                        ),
                        ft.Divider(color="transparent", height=15),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            controls=[
                                ft.Container(width=100, height=1, bgcolor="white30"),
                                ft.Text("  ou continuer avec  ", color="white70", size=12),
                                ft.Container(width=100, height=1, bgcolor="white30"),
                            ]
                        ),
                        ft.Divider(color="transparent", height=15),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=15,
                            controls=[
                                self.social_button(GOOGLE_SVG, "Google"),
                                self.social_button(FACEBOOK_SVG, "Facebook"),
                                self.social_button(TWITTER_SVG, "Twitter / X"),
                            ]
                        ),
                    ]
                )
            )
        ]

    def social_button(self, svg_content, nom):
        svg_b64 = base64.b64encode(svg_content.encode("utf-8")).decode("utf-8")
        full_src = f"data:image/svg+xml;base64,{svg_b64}"
        
        return ft.Container(
            width=55,
            height=55,
            border_radius=50,
            bgcolor="white",
            tooltip=f"{nom} (bientôt disponible)",
            alignment=ft.Alignment(0, 0),
            content=ft.Image(src=full_src, width=28, height=28),
            ink=True,
            on_click=self.social_login_info,
            shadow=ft.BoxShadow(blur_radius=6, color="#00000040"),
        )

    def social_login_info(self, e):
        self.message.value = "Connexion sociale bientôt disponible !"
        self.message.color = "#FFD700"
        self._pg.update()

    def handle_inscription(self, e):
        if not all([self.username.value, self.email.value, self.password.value]):
            self.message.value = "Veuillez remplir tous les champs obligatoires !"
            self.message.color = "red"
            self._pg.update()
            return
        try:
            res = httpx.post(
                "http://127.0.0.1:8000/api/users/register",
                json={
                    "username": self.username.value,
                    "email": self.email.value,
                    "password": self.password.value,
                    "role": "client",
                    "phone": self.phone.value,
                },
                timeout=10
            )
            if res.status_code == 200:
                self.message.value = "Compte créé avec succès ! En attente d'approbation par l'administrateur."
                self.message.color = "green"
                self._pg.update()
            else:
                try:
                    erreur = res.json().get("detail", "Erreur lors de l'inscription")
                except:
                    erreur = "Erreur lors de l'inscription"
                self.message.value = erreur
                self.message.color = "red"
                self._pg.update()
        except Exception as ex:
            self.message.value = f"Erreur : {ex}"
            self.message.color = "red"
            self._pg.update()

    def go_to_login(self, e):
        # Modification validée : push_route remplacé définitivement par navigate
        self._pg.navigate("/login")