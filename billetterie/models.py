from django.db import models
import uuid


class Utilisateur(models.Model):
    ROLE_CHOICES = [
        ('client', 'Client'),
        ('admin', 'Administrateur'),
    ]

    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    mot_de_passe = models.CharField(max_length=255)  # à hasher à l'inscription
    cle_utilisateur = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.email})"


class Offre(models.Model):
    nom_offre = models.CharField(max_length=100)
    description = models.TextField()
    nombre_places = models.PositiveIntegerField()
    prix = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.nom_offre} – {self.prix}€ ({self.nombre_places} places)"


class Commande(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='commandes')
    cle_commande = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    date_achat = models.DateTimeField(auto_now_add=True)
    cle_finale = models.CharField(max_length=255)
    qrcode = models.TextField(blank=True)  # à générer plus tard (URL/base64)

    def save(self, *args, **kwargs):
        self.cle_finale = f"{self.utilisateur.cle_utilisateur}-{self.cle_commande}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Commande #{self.id} - {self.utilisateur.nom}"


class Panier(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='panier')

    def __str__(self):
        return f"Panier de {self.utilisateur.prenom}"


class PanierOffre(models.Model):
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE, related_name='offres')
    offre = models.ForeignKey(Offre, on_delete=models.CASCADE)
    quantite = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantite} × {self.offre.nom_offre} (Panier de {self.panier.utilisateur.nom})"
