# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Modele(models.Model):
    titre = models.CharField(max_length=100)
    sous_titre = models.CharField(max_length=400)
    admin = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True, auto_now=False, 
                                verbose_name="Date de parution")
    inputs = models.IntegerField(default=1)
    outputs = models.IntegerField(default=1)
    back_end_id = models.IntegerField(default=0)
    def __str__(self):
        """ 
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que 
        nous traiterons plus tard et dans l'administration
        """
        return self.titre

class Layer(models.Model):
    model = models.ForeignKey(Modele)
    number = models.IntegerField(default=1)
    activation = models.CharField(max_length=400)
    def __str__(self):
        """ 
        Cette méthode que nous définirons dans tous les modèles
        nous permettra de reconnaître facilement les différents objets que 
        nous traiterons plus tard et dans l'administration
        """
        return self.model
