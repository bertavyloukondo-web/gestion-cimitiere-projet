from ninja import Router, Schema
from terrain.models import Zone, Caveau
from typing import List, Optional

router = Router()


class ZoneSchema(Schema):
    id: int
    nom: str
    type_zone: str
    description: str = None


class CaveauSchema(Schema):
    id: int
    numero: str
    latitude: float
    longitude: float
    longueur: float
    largeur: float
    etat: str
    zone_id: int


class ZoneCreateSchema(Schema):
    nom: str
    type_zone: str
    description: str = None


class CaveauCreateSchema(Schema):
    zone_id: int
    numero: str
    latitude: float
    longitude: float
    longueur: float
    largeur: float


@router.get("/zones", response=List[ZoneSchema])
def list_zones(request):
    return Zone.objects.all()


@router.post("/zones", response=ZoneSchema)
def create_zone(request, data: ZoneCreateSchema):
    zone = Zone.objects.create(**data.dict())
    return zone


@router.get("/caveaux", response=List[CaveauSchema])
def list_caveaux(request, etat: Optional[str] = None):
    qs = Caveau.objects.all()
    if etat:
        qs = qs.filter(etat=etat)
    return qs


@router.post("/caveaux", response=CaveauSchema)
def create_caveau(request, data: CaveauCreateSchema):
    caveau = Caveau.objects.create(**data.dict())
    return caveau


@router.put("/caveaux/{caveau_id}/etat")
def update_etat_caveau(request, caveau_id: int, etat: str):
    try:
        caveau = Caveau.objects.get(id=caveau_id)
        caveau.etat = etat
        caveau.save()
        return {"message": "État mis à jour", "etat": etat}
    except Caveau.DoesNotExist:
        return {"error": "Caveau introuvable"}
@router.get("/stats")
def stats_terrain(request):
    from terrain.models import Caveau
    from reservations.models import Reservation
    from finance.models import Facture
    total_disponibles = Caveau.objects.filter(etat='disponible').count()
    total_reserves = Caveau.objects.filter(etat='reserve').count()
    total_occupes = Caveau.objects.filter(etat='occupe').count()
    total_attente = Reservation.objects.filter(statut='en_attente').count()
    total_paye = sum(f.montant_paye for f in Facture.objects.all())
    return {
        "caveaux_disponibles": total_disponibles,
        "caveaux_reserves": total_reserves,
        "caveaux_occupes": total_occupes,
        "reservations_en_attente": total_attente,
        "recettes_totales": float(total_paye),
    }