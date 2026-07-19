import flet as ft
import httpx


class LoginPage(ft.View):
    def __init__(self, page: ft.Page, on_success):
        super().__init__(route="/login", padding=0)
        self._pg = page
        self.on_success = on_success
        self.bgcolor = "#1A237E"

        self.username = ft.TextField(
            label="Nom d'utilisateur",
            border_color="white",
            label_style=ft.TextStyle(color="white"),
            color="white",
            width=320,
        )
        self.password = ft.TextField(
            label="Mot de passe",
            password=True,
            can_reveal_password=True,
            border_color="white",
            label_style=ft.TextStyle(color="white"),
            color="white",
            width=320,
        )
        self.mfa_code = ft.TextField(
            label="Code MFA (6 chiffres)",
            border_color="white",
            label_style=ft.TextStyle(color="white"),
            color="white",
            width=320,
            visible=False,
        )
        self.message = ft.Text(color="red", size=13)
        self.btn_login = ft.ElevatedButton(
            content=ft.Text("Se connecter", color="#1A237E", weight=ft.FontWeight.BOLD),
            width=320,
            bgcolor="#FFD700",
            on_click=self.handle_login,
        )
        self.btn_mfa = ft.ElevatedButton(
            content=ft.Text("Vérifier le code MFA", color="#1A237E", weight=ft.FontWeight.BOLD),
            width=320,
            bgcolor="#FFD700",
            on_click=self.handle_mfa,
            visible=False,
        )

        self.controls = [
            ft.Container(
                expand=True,
                alignment=ft.Alignment(0, 0),
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Icon(ft.Icons.LOCATION_CITY, color="white", size=60),
                        ft.Text("Gestion de Cimetière", color="white", size=24, weight=ft.FontWeight.BOLD),
                        ft.Text("Connectez-vous à votre compte", color="white70", size=14),
                        ft.Divider(color="transparent", height=20),
                        self.username,
                        self.password,
                        self.mfa_code,
                        self.message,
                        self.btn_login,
                        self.btn_mfa,
                        ft.Divider(height=15, color="transparent"),
                        ft.TextButton(
                            content=ft.Text("Créer un compte", color="white"),
                            on_click=self.go_to_inscription,
                        ),
                    ]
                )
            )
        ]

    def handle_login(self, e):
        self.message.value = ""
        try:
            res = httpx.post(
                "http://127.0.0.1:8000/api/users/login",
                json={
                    "username": self.username.value,
                    "password": self.password.value,
                },
                timeout=10
            )
            if res.status_code == 200:
                data = res.json()
                if "error" in data:
                    self.message.value = data["error"]
                else:
                    self.message.value = f"Code MFA envoyé sur votre email !"
                    self.message.color = "green"
                    self.mfa_code.visible = True
                    self.btn_mfa.visible = True
                    self.btn_login.visible = False
            else:
                self.message.value = f"Erreur serveur : {res.status_code}"
        except Exception as ex:
            self.message.value = f"Erreur : {ex}"
        self._pg.update()

    def handle_mfa(self, e):
        try:
            res = httpx.post(
                "http://127.0.0.1:8000/api/users/verify-mfa",
                json={
                    "username": self.username.value,
                    "mfa_code": self.mfa_code.value,
                },
                timeout=10
            )
            if res.status_code == 200:
                data = res.json()
                if "error" in data:
                    self.message.value = data["error"]
                    self.message.color = "red"
                else:
                    self.on_success(data)
            else:
                self.message.value = f"Erreur serveur : {res.status_code}"
        except Exception as ex:
            self.message.value = f"Erreur : {ex}"
        self._pg.update()

    def go_to_inscription(self, e):
        self._pg.go("/inscription")