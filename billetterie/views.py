from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import Utilisateur, Offre, Panier, PanierOffre


def accueil(request):
    return render(request, 'billetterie/accueil.html')


def inscription(request):
    if request.method == "POST":
        nom = request.POST.get("nom")
        email = request.POST.get("email")
        mot_de_passe = request.POST.get("mot_de_passe")
        mot_de_passe2 = request.POST.get("mot_de_passe_confirm")

        if mot_de_passe != mot_de_passe2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return redirect('inscription')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Cet utilisateur existe déjà.")
            return redirect('inscription')

        user = User.objects.create_user(username=email, email=email, password=mot_de_passe, first_name=nom)
        user.save()

        utilisateur = Utilisateur.objects.create(
            nom=nom,
            prenom="",
            email=email,
            mot_de_passe=mot_de_passe  # À sécuriser plus tard
        )
        utilisateur.save()

        return redirect('connexion')

    return render(request, 'billetterie/inscription.html')


def connexion(request):
    if request.method == "POST":
        email = request.POST.get("email")
        mot_de_passe = request.POST.get("mot_de_passe")

        user = authenticate(request, username=email, password=mot_de_passe)
        if user is not None:
            login(request, user)
            return redirect('accueil')
        else:
            messages.error(request, "Identifiants invalides.")
            return redirect('connexion')

    return render(request, 'billetterie/connexion.html')


def deconnexion(request):
    logout(request)
    return redirect('connexion')


def liste_offres(request):
    offres = Offre.objects.all()
    return render(request, 'billetterie/offres.html', {'offres': offres})


def ajouter_au_panier(request, offre_id):
    if not request.user.is_authenticated:
        return redirect('connexion')

    utilisateur = Utilisateur.objects.get(email=request.user.username)
    offre = get_object_or_404(Offre, id=offre_id)

    panier, _ = Panier.objects.get_or_create(utilisateur=utilisateur)

    item, created = PanierOffre.objects.get_or_create(
        panier=panier,
        offre=offre,
    )
    if not created:
        item.quantite += 1
        item.save()

    return redirect('offres')
