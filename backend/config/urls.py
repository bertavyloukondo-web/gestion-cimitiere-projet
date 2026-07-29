from django.contrib import admin
from django.urls import path
from django.http import HttpResponse
from django.shortcuts import redirect
from ninja import NinjaAPI
import os

from users.api import router as users_router
from terrain.api import router as terrain_router
from reservations.api import router as reservations_router
from concessions.api import router as concessions_router
from finance.api import router as finance_router


api = NinjaAPI(title="API Cimetiere", version="1.0.0")

api.add_router("/users/", users_router)
api.add_router("/terrain/", terrain_router)
api.add_router("/reservations/", reservations_router)
api.add_router("/concessions/", concessions_router)
api.add_router("/finance/", finance_router)


def serve_carte(request):
    html_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "frontend",
        "components",
        "carte_widget.html"
    )

    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as file:
            return HttpResponse(file.read(), content_type="text/html")

    return HttpResponse(
        f"Erreur : fichier carte_widget.html introuvable à {html_path}",
        status=404
    )


urlpatterns = [
    path("", lambda request: redirect("/carte/")),
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path("carte/", serve_carte),
]