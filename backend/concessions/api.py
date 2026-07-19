from ninja import Router, Schema
from typing import List, Optional
from django.utils import timezone
from concessions.models import Concession, Exhumation
from users.models import User
import datetime

router = Router()


class ConcessionSchema(Schema):
    id: int
    reservation_id: int
    client_id: int
    caveau_id: int
    type_concession: str
    statut: str
    date_debut: datetime.date
    date_fin: datetime.date = None


class ConcessionCreateSchema(Schema):
    reservation_id: int
    client_id: int
    caveau_id: int
    type_concession: str
    date_debut: datetime.date
    date_fin: datetime.date = None


class ExhumationSchema(Schema):
    id: int
    concession_id: int
    demandeur_id: int
    motif: str
    statut: str
    date_demande: datetime.datetime


class ExhumationCreateSchema(Schema):
    concession_id: int
    demandeur_id: int
    motif: str


@router.get("/", response=List[ConcessionSchema])
def list_concessions(request, statut: Optional[str] = None):
    qs = Concession.objects.all()
    if statut:
        qs = qs.filter(statut=statut)
    return qs


@router.post("/", response=ConcessionSchema)
def create_concession(request, data: ConcessionCreateSchema):
    concession = Concession.objects.create(**data.dict())
    return concession


@router.get("/exhumations", response=List[ExhumationSchema])
def list_exhumations(request):
    return Exhumation.objects.all()


@router.post("/exhumations", response=ExhumationSchema)
def create_exhumation(request, data: ExhumationCreateSchema):
    exhumation = Exhumation.objects.create(**data.dict())
    return exhumation


@router.put("/exhumations/{exhumation_id}/valider")
def valider_exhumation(request, exhumation_id: int, admin_id: int):
    try:
        exhumation = Exhumation.objects.get(id=exhumation_id)
        admin = User.objects.get(id=admin_id)
        exhumation.statut = 'validee'
        exhumation.date_validation = timezone.now()
        exhumation.valide_par = admin
        exhumation.save()
        return {"message": "Exhumation validée avec succès"}
    except Exhumation.DoesNotExist:
        return {"error": "Exhumation introuvable"}