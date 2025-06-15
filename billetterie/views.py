from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Offre

def liste_offres(request):
    offres = Offre.objects.all()
    return render(request, 'billetterie/offres.html', {'offres': offres})



# Vue de la page d'accueil
def accueil(request):
    return render(request, 'billetterie/accueil.html')


# Vue de la page d'inscription
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
        return redirect('connexion')

    return render(request, 'billetterie/inscription.html')


# Vue de la connexion
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


# Vue de la déconnexion
def deconnexion(request):
    logout(request)
    return redirect('connexion')
