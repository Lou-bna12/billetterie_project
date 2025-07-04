from django.urls import path
from . import views

urlpatterns = [
    path('accueil/', views.accueil, name='accueil'),
    path('register/', views.inscription, name='inscription'),
    path('login/', views.connexion, name='connexion'),
    path('logout/', views.deconnexion, name='deconnexion'),
    path('offres/', views.liste_offres, name='offres'),
    path('ajouter-au-panier/<int:offre_id>/', views.ajouter_au_panier, name='ajouter_au_panier'),
]
