import flet as ft
import httpx
import webbrowser


class ComptabilitePage(ft.View):
    def __init__(self, page: ft.Page, user_data: dict):
        super().__init__(route="/comptabilite", padding=0)
        self._pg = page
        self.user = user_data
        self.bgcolor = "#F0F2F5"
        self.paiements = []

        self.recherche = ft.TextField(
            hint_text="Rechercher par référence...",
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
                                    ft.Icon(ft.Icons.ACCOUNT_BALANCE, color="white", size=25),
                                    ft.Text("Comptabilité", color="white", size=18, weight=ft.FontWeight.BOLD),
                                ]),
                                ft.ElevatedButton(
                                    content=ft.Row(controls=[
                                        ft.Icon(ft.Icons.FILE_DOWNLOAD, color="white"),
                                        ft.Text("Exporter vers Excel", color="white"),
                                    ]),
                                    style=ft.ButtonStyle(
                                        bgcolor={
                                            ft.ControlState.HOVERED: "#1B5E20",
                                            ft.ControlState.DEFAULT: "#2E7D32",
                                        },
                                        overlay_color=ft.Colors.TRANSPARENT,
                                    ),
                                    on_click=self.exporter_excel,
                                ),
                            ]
                        )
                    ),
                    ft.Container(
                        padding=10,
                        bgcolor="#E8EAF6",
                        content=ft.Row(controls=[
                            self.recherche,
                            ft.ElevatedButton(
                                content=ft.Text("Toutes", color="white"),
                                style=ft.ButtonStyle(bgcolor="#1A237E"),
                                on_click=lambda e: self.filtrer(None),
                            ),
                            ft.ElevatedButton(
                                content=ft.Text("Mobile Money", color="white"),
                                style=ft.ButtonStyle(bgcolor="#FF9800"),
                                on_click=lambda e: self.filtrer("mobile_money"),
                            ),
                            ft.ElevatedButton(
                                content=ft.Text("Airtel Money", color="white"),
                                style=ft.ButtonStyle(bgcolor="#F44336"),
                                on_click=lambda e: self.filtrer("airtel_money"),
                            ),
                            ft.ElevatedButton(
                                content=ft.Text("Espèces", color="white"),
                                style=ft.ButtonStyle(bgcolor="#4CAF50"),
                                on_click=lambda e: self.filtrer("especes"),
                            ),
                            ft.ElevatedButton(
                                content=ft.Text("Virement", color="white"),
                                style=ft.ButtonStyle(bgcolor="#2196F3"),
                                on_click=lambda e: self.filtrer("virement"),
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
        self.charger_paiements()

    def charger_paiements(self, mode=None):
        try:
            url = "http://127.0.0.1:8000/api/finance/paiements"
            if mode:
                url += f"?mode_paiement={mode}"
            res = httpx.get(url, timeout=10)
            self.paiements = res.json()
            self.afficher_liste(self.paiements)
        except Exception as ex:
            self.message.value = f"Erreur : {ex}"
            self._pg.update()

    def rechercher(self, e):
        terme = self.recherche.value.lower().strip()
        if not terme:
            self.afficher_liste(self.paiements)
            return
        filtres = [
            p for p in self.paiements
            if terme in (p.get("reference") or "").lower()
        ]
        self.afficher_liste(filtres)

    def formater_date(self, date_str):
        try:
            from datetime import datetime
            d = datetime.strptime(date_str[:19], "%Y-%m-%dT%H:%M:%S")
            return d.strftime("%d/%m/%Y %H:%M")
        except:
            return date_str

    def afficher_liste(self, paiements):
        self.liste.controls.clear()
        if not paiements:
            self.liste.controls.append(
                ft.Text("Aucune transaction trouvée", color="#555555", size=14)
            )
        mode_labels = {
            "mobile_money": "Mobile Money",
            "airtel_money": "Airtel Money",
            "especes": "Espèces",
            "virement": "Virement",
        }
        mode_couleurs = {
            "mobile_money": "#FF9800",
            "airtel_money": "#F44336",
            "especes": "#4CAF50",
            "virement": "#2196F3",
        }
        for p in paiements:
            couleur = mode_couleurs.get(p.get("mode_paiement", ""), "#9E9E9E")
            label = mode_labels.get(p.get("mode_paiement", ""), p.get("mode_paiement", ""))

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
                                ft.Text(f"{p.get('montant', 0)} FCFA", weight=ft.FontWeight.BOLD, size=16, color="#1A237E"),
                                ft.Text(f"Référence : {p.get('reference') or '-'}", color="#555555", size=12),
                                ft.Text(f"Date : {self.formater_date(p.get('date_paiement', ''))}", color="#555555", size=12),
                            ]),
                            ft.Container(
                                bgcolor=couleur,
                                border_radius=5,
                                padding=ft.Padding(10, 5, 10, 5),
                                content=ft.Text(label, color="white", size=11, weight=ft.FontWeight.BOLD),
                            ),
                        ]
                    )
                )
            )
        self._pg.update()

    def filtrer(self, mode):
        self.recherche.value = ""
        self.charger_paiements(mode)

    def exporter_excel(self, e):
        try:
            webbrowser.open("http://127.0.0.1:8000/api/finance/export-excel")
        except Exception as ex:
            self.message.value = f"Erreur export : {ex}"
            self._pg.update()

    def go_back(self, e):
        self._pg.go("/dashboard")