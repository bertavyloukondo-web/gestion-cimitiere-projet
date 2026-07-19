from ninja import Router, Schema
from typing import Optional
from users.models import User
import random

router = Router()


class UserSchema(Schema):
    id: int
    username: str
    email: str
    role: str
    statut: str
    phone: Optional[str] = None


class RegisterSchema(Schema):
    username: str
    email: str
    password: str
    role: str = 'client'
    phone: Optional[str] = None


class LoginSchema(Schema):
    username: str
    password: str


class MFASchema(Schema):
    username: str
    mfa_code: str


@router.post("/register", response=UserSchema)
def register(request, data: RegisterSchema):
    from django.core.mail import send_mail
    from django.conf import settings
    from ninja.errors import HttpError

    if User.objects.filter(username=data.username).exists():
        raise HttpError(400, "Ce nom d'utilisateur existe déjà")

    if User.objects.filter(email=data.email).exists():
        raise HttpError(400, "Cet email est déjà utilisé")

    user = User.objects.create_user(
        username=data.username,
        email=data.email,
        password=data.password,
        role=data.role,
        phone=data.phone,
        statut='en_attente' if data.role == 'client' else 'approuve',
    )

    if data.role == 'client':
        try:
            send_mail(
                subject='Nouvelle inscription en attente',
                message=f"Un nouveau client s'est inscrit : {user.username} ({user.email}).\n\nVeuillez approuver ou refuser ce compte dans le tableau de bord.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass

    return user


@router.post("/login")
def login(request, data: LoginSchema):
    from django.core.mail import send_mail
    from django.conf import settings

    try:
        user = User.objects.get(username=data.username)
        if not user.check_password(data.password):
            return {"error": "Identifiants incorrects"}

        if user.statut == 'en_attente':
            return {"error": "Votre compte est en attente d'approbation par l'administrateur"}

        if user.statut == 'refuse':
            return {"error": "Votre compte a été refusé"}

        mfa_code = str(random.randint(100000, 999999))
        user.mfa_code = mfa_code
        user.mfa_verified = False
        user.save()

        try:
            send_mail(
                subject='Votre code de connexion - Gestion de Cimetière',
                message=f"Bonjour {user.username},\n\nVotre code MFA est : {mfa_code}\n\nCe code est valable pour cette session uniquement.\n\nSi vous n'êtes pas à l'origine de cette connexion, ignorez ce message.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
        except Exception as e:
            return {"error": f"Impossible d'envoyer le code MFA : {str(e)}"}

        return {"message": "Code MFA envoyé sur votre email"}

    except User.DoesNotExist:
        return {"error": "Identifiants incorrects"}


@router.post("/verify-mfa")
def verify_mfa(request, data: MFASchema):
    try:
        user = User.objects.get(username=data.username)
        if user.mfa_code == data.mfa_code:
            user.mfa_verified = True
            user.save()
            return {
                "message": "Authentification réussie",
                "user_id": user.id,
                "role": user.role,
                "username": user.username,
            }
        return {"error": "Code MFA incorrect"}
    except User.DoesNotExist:
        return {"error": "Utilisateur introuvable"}


@router.get("/list", response=list[UserSchema])
def list_users(request):
    result = []
    for u in User.objects.all():
        result.append({
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "role": u.role,
            "statut": u.statut,
            "phone": u.phone or "",
        })
    return result


@router.put("/{user_id}/approuver")
def approuver_utilisateur(request, user_id: int):
    try:
        user = User.objects.get(id=user_id)
        user.statut = 'approuve'
        user.save()
        return {"message": "Compte approuvé avec succès"}
    except User.DoesNotExist:
        return {"error": "Utilisateur introuvable"}


@router.put("/{user_id}/refuser")
def refuser_utilisateur(request, user_id: int):
    try:
        user = User.objects.get(id=user_id)
        user.statut = 'refuse'
        user.save()
        return {"message": "Compte refusé"}
    except User.DoesNotExist:
        return {"error": "Utilisateur introuvable"}