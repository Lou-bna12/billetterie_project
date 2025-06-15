from django.contrib import admin
from .models import Utilisateur, Offre, Commande, Panier, PanierOffre

admin.site.register(Utilisateur)
admin.site.register(Offre)
admin.site.register(Commande)
admin.site.register(Panier)
admin.site.register(PanierOffre)

