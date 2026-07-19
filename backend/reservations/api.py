from ninja import Router, Schema
from typing import List, Optional
from django.utils import timezone
from reservations.models import Reservation
from terrain.models import Caveau
from users.models import User
import datetime

router = Router()


class ReservationSchema(Schema):
    id: int
    client_id: int
    caveau_id: int
    nom_defunt: str
    prenom_defunt: str
    date_naissance_defunt: datetime.date
    date_deces_defunt: datetime.date
    statut: str
    date_reservation: datetime.datetime
    mode_paiement_prefere: str
    notes: Optional[str] = None


class ReservationCreateSchema(Schema):
    client_id: int
    caveau_id: int
    nom_defunt: str
    prenom_defunt: str
    date_naissance_defunt: datetime.date
    date_deces_defunt: datetime.date
    mode_paiement_prefere: str = 'especes'
    notes: Optional[str] = None


@router.get("/", response=List[ReservationSchema])
def list_reservations(request, statut: Optional[str] = None):
    qs = Reservation.objects.all()
    if statut:
        qs = qs.filter(statut=statut)
    result = []
    for r in qs:
        result.append({
            "id": r.id,
            "client_id": r.client_id,
            "caveau_id": r.caveau_id,
            "nom_defunt": r.nom_defunt,
            "prenom_defunt": r.prenom_defunt,
            "date_naissance_defunt": r.date_naissance_defunt,
            "date_deces_defunt": r.date_deces_defunt,
            "statut": r.statut,
            "date_reservation": r.date_reservation,
            "mode_paiement_prefere": r.mode_paiement_prefere,
            "notes": r.notes or "",
        })
    return result


@router.post("/", response=ReservationSchema)
def create_reservation(request, data: ReservationCreateSchema):
    try:
        caveau = Caveau.objects.get(id=data.caveau_id)
        caveau.etat = 'reserve'
        caveau.save()
        reservation = Reservation.objects.create(
            client_id=data.client_id,
            caveau_id=data.caveau_id,
            nom_defunt=data.nom_defunt,
            prenom_defunt=data.prenom_defunt,
            date_naissance_defunt=data.date_naissance_defunt,
            date_deces_defunt=data.date_deces_defunt,
            mode_paiement_prefere=data.mode_paiement_prefere,
            notes=data.notes or "",
        )
        return reservation
    except Exception as ex:
        return {"error": str(ex)}


@router.put("/{reservation_id}/valider")
def valider_reservation(request, reservation_id: int, admin_id: int):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        admin = User.objects.get(id=admin_id)
        reservation.statut = 'validee'
        reservation.date_validation = timezone.now()
        reservation.valide_par = admin
        reservation.save()
        caveau = reservation.caveau
        caveau.etat = 'occupe'
        caveau.save()
        return {"message": "Reservation validee avec succes"}
    except Reservation.DoesNotExist:
        return {"error": "Reservation introuvable"}


@router.put("/{reservation_id}/refuser")
def refuser_reservation(request, reservation_id: int):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
        reservation.statut = 'refusee'
        reservation.save()
        caveau = reservation.caveau
        caveau.etat = 'disponible'
        caveau.save()
        return {"message": "Reservation refusee"}
    except Reservation.DoesNotExist:
        return {"error": "Reservation introuvable"}