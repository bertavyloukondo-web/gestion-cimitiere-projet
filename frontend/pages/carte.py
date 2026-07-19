import flet as ft
import os


class CartePage(ft.View):
    def __init__(self, page, user_data):
        super().__init__(route="/carte", padding=0)
        self._pg = page
        self.user = user_data
        self.bgcolor = "#F0F2F5"
        self.controls = [
            ft.Column(expand=True, controls=[
                ft.Container(
                    bgcolor="#1A237E",
                    padding=15,
                    content=ft.Row(controls=[
                        ft.IconButton(ft.Icons.ARROW_BACK, icon_color="white", on_click=self.go_back),
                        ft.Icon(ft.Icons.MAP, color="white", size=25),
                        ft.Text("Carte Interactive", color="white", size=18, weight=ft.FontWeight.BOLD),
                    ])
                ),
                ft.Container(
                    expand=True,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Icon(ft.Icons.MAP, size=80, color="#1A237E"),
                            ft.Text("Carte Interactive des Caveaux", size=20, weight=ft.FontWeight.BOLD, color="#1A237E"),
                            ft.Text("Cliquez sur le bouton pour ouvrir la carte", color="#1A237E", size=14, weight=ft.FontWeight.W_500),
                            ft.Divider(height=20, color="transparent"),
                            ft.ElevatedButton(
                                content=ft.Row(controls=[
                                    ft.Icon(ft.Icons.MAP, color="white"),
                                    ft.Text("Ouvrir la carte", color="white"),
                                ]),
                                style=ft.ButtonStyle(
                                    bgcolor={
                                        ft.ControlState.HOVERED: "#0D1A6E",
                                        ft.ControlState.DEFAULT: "#1A237E",
                                    },
                                    overlay_color=ft.Colors.TRANSPARENT,
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                ),
                                on_click=self.open_carte,
                            ),
                            ft.Divider(height=30, color="transparent"),
                            # Légende avec espacement
                            ft.Container(
                                bgcolor="white",
                                border_radius=10,
                                padding=15,
                                shadow=ft.BoxShadow(blur_radius=5, color="#CCCCCC"),
                                content=ft.Row(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    controls=[
                                        ft.Container(width=15, height=15, bgcolor="#4CAF50", border_radius=10),
                                        ft.Text("Disponible", size=12, color="#333333"),
                                        ft.Container(width=30),
                                        ft.Container(width=15, height=15, bgcolor="#FF9800", border_radius=10),
                                        ft.Text("Réservé", size=12, color="#333333"),
                                        ft.Container(width=30),
                                        ft.Container(width=15, height=15, bgcolor="#F44336", border_radius=10),
                                        ft.Text("Occupé", size=12, color="#333333"),
                                        ft.Container(width=30),
                                        ft.Container(width=15, height=15, bgcolor="#9E9E9E", border_radius=10),
                                        ft.Text("Non exploitable", size=12, color="#333333"),
                                    ]
                                )
                            ),
                        ]
                    )
                )
            ])
        ]

    def open_carte(self, e):
        html_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "components", "carte_widget.html"))
        os.system(f'start "" "{html_path}"')

    def go_back(self, e):
        self._pg.go("/dashboard")