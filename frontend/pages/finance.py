import flet as ft
import httpx
import os


class FinancePage(ft.View):
    def __init__(self, page: ft.Page, user_data: dict):
        super().__init__(route="/finance", padding=0)
        self._pg = page
        self.user = user_data
        self.bgcolor = "#F5F5F5"
        self.factures = []

        self.liste = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        self.message = ft.Text(color="red", size=13)
        self.stats = ft.Row(wrap=True)

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
                                    ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, color="white", size=25),
                                    ft.Text("Gestion Financière", color="white", size=18, weight=ft.FontWeight.BOLD),
                                ]),
                            ]
                        )
                    ),
                    ft.Container(padding=10, content=self.stats),
                    ft.Container(
                        padding=10,
                        bgcolor="#E8EAF6",
                        content=ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    content=ft.Text("Toutes", color="white"),
                                    bgcolor="#1A237E",
                                    on_click=lambda e: self.filtrer(None)
                                ),
                                ft.ElevatedButton(
                                    content=ft.Text("En attente", color="white"),
                                    bgcolor="#FF9800",
                                    on_click=lambda e: self.filtrer("en_attente")
                                ),
                                ft.ElevatedButton(
                                    content=ft.Text("Payées", color="white"),
                                    bgcolor="#4CAF50",
                                    on_click=lambda e: self.filtrer("payee")
                                ),
                                ft.ElevatedButton(
                                    content=ft.Text("Partielles", color="white"),
                                    bgcolor="#2196F3",
                                    on_click=lambda e: self.filtrer("partiellement_payee")
                                ),
                            ]
                        )
                    ),
                    self.message,
                    ft.Container(expand=True, padding=10, content=self.liste)
                ]
            )
        ]
        self.charger_stats()
        self.charger_factures()

    def charger_stats(self):
        try:
            res = httpx.get("http://127.0.0.1:8000/api/finance/stats", timeout=10)
            data = res.json()
            self.stats.controls = [
                self.stat_card("Total factures", str(data.get("total_factures", 0)), ft.Icons.RECEIPT, "#1A237E"),
                self.stat_card("Total payé", f"{data.get('total_paye', 0)} FCFA", ft.Icons.CHECK_CIRCLE, "#4CAF50"),
                self.stat_card("Total attendu", f"{data.get('total_attendu', 0)} FCFA", ft.Icons.HOURGLASS_EMPTY, "#FF9800"),
            ]
            self._pg.update()
        except Exception as ex:
            self.message.value = f"Erreur stats : {ex}"
            self._pg.update()

    def stat_card(self, title, value, icon, color):
        return ft.Container(
            width=180,
            height=90,
            bgcolor="white",
            border_radius=10,
            padding=10,
            margin=5,
            border=ft.Border.all(1, color),
            shadow=ft.BoxShadow(blur_radius=5, color="#CCCCCC"),
            content=ft.Row(controls=[
                ft.Icon(icon, color=color, size=30),
                ft.Column(controls=[
                    ft.Text(title, size=10, color="#555555"),
                    ft.Text(value, size=16, weight=ft.FontWeight.BOLD, color=color),
                ])
            ])
        )

    def formater_date(self, date_str):
        try:
            from datetime import datetime
            d = datetime.strptime(date_str[:10], "%Y-%m-%d")
            return d.strftime("%d/%m/%Y")
        except:
            return date_str

    def charger_factures(self, statut=None):
        try:
            url = "http://127.0.0.1:8000/api/finance/factures"
            if statut:
                url += f"?statut={statut}"
            res = httpx.get(url, timeout=10)
            self.factures = res.json()
            self.afficher_factures()
        except Exception as ex:
            self.message.value = f"Erreur : {ex}"
            self._pg.update()

    def afficher_factures(self):
        self.liste.controls.clear()
        if not self.factures:
            self.liste.controls.append(
                ft.Text("Aucune facture trouvée", color="#555555", size=14)
            )
        for f in self.factures:
            couleur = {
                "en_attente": "#FF9800",
                "payee": "#4CAF50",
                "partiellement_payee": "#2196F3",
                "annulee": "#9E9E9E"
            }.get(f["statut"], "#9E9E9E")

            statut_label = {
                "en_attente": "EN ATTENTE",
                "payee": "PAYÉE",
                "partiellement_payee": "PARTIELLE",
                "annulee": "ANNULÉE"
            }.get(f["statut"], f["statut"].upper())

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
                                ft.Text(f"Facture {f['numero']}", weight=ft.FontWeight.BOLD, size=16, color="#1A237E"),
                                ft.Text(f"Montant : {f['montant_total']} FCFA", color="#333333", size=12),
                                ft.Text(f"Payé : {f['montant_paye']} FCFA", color="#4CAF50", size=12, weight=ft.FontWeight.BOLD),
                                ft.Text(f"Échéance : {self.formater_date(f['date_echeance'])}", color="#333333", size=12),
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
                                    ft.ElevatedButton(
                                        content=ft.Text("Payer", color="white"),
                                        bgcolor="#4CAF50",
                                        on_click=lambda e, fid=f["id"], mt=f["montant_total"]: self.ouvrir_paiement(fid, mt),
                                        visible=f["statut"] != "payee",
                                    ),
                                    ft.ElevatedButton(
                                        content=ft.Row(controls=[
                                            ft.Icon(ft.Icons.PICTURE_AS_PDF, color="white"),
                                            ft.Text("PDF", color="white"),
                                        ]),
                                        bgcolor="#F44336",
                                        on_click=lambda e, fid=f["id"]: self.telecharger_pdf(fid),
                                    ),
                                ]
                            )
                        ]
                    )
                )
            )
        self._pg.update()

    def filtrer(self, statut):
        self.charger_factures(statut)

    def telecharger_pdf(self, facture_id):
        url = f"http://127.0.0.1:8000/api/finance/factures/{facture_id}/pdf"
        os.system(f'start "" "{url}"')

    def ouvrir_paiement(self, facture_id, montant_total):
        def effectuer_paiement(e):
            try:
                httpx.post(
                    "http://127.0.0.1:8000/api/finance/paiements",
                    json={
                        "facture_id": facture_id,
                        "montant": float(montant_field.value),
                        "mode_paiement": mode.value,
                        "reference": reference.value,
                    },
                    timeout=10
                )
                dlg.open = False
                self._pg.update()
                self.charger_stats()
                self.charger_factures()
            except Exception as ex:
                self.message.value = f"Erreur : {ex}"
                self._pg.update()

        montant_field = ft.TextField(label="Montant", value=str(montant_total), width=250)
        mode = ft.Dropdown(
            label="Mode de paiement",
            width=250,
            options=[
                ft.dropdown.Option("mobile_money", "Mobile Money"),
                ft.dropdown.Option("airtel_money", "Airtel Money"),
                ft.dropdown.Option("especes", "Espèces"),
                ft.dropdown.Option("virement", "Virement"),
            ]
        )
        reference = ft.TextField(label="Référence", width=250)

        dlg = ft.AlertDialog(
            title=ft.Text("Enregistrer un paiement"),
            content=ft.Column(controls=[montant_field, mode, reference], tight=True),
            actions=[
                ft.ElevatedButton(
                    content=ft.Text("Annuler", color="white"),
                    bgcolor="#F44336",
                    on_click=lambda e: setattr(dlg, 'open', False) or self._pg.update()
                ),
                ft.ElevatedButton(
                    content=ft.Text("Confirmer", color="white"),
                    bgcolor="#4CAF50",
                    on_click=effectuer_paiement
                ),
            ]
        )
        self._pg.overlay.append(dlg)
        dlg.open = True
        self._pg.update()

    def go_back(self, e):
        self._pg.route = "/dashboard"
        self._pg.on_route_change(None)
        self._pg.update()