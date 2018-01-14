# coding: utf-8
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Modele, Layer
import sys
sys.path.append("../")


class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30,widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class InscriptionForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(max_length=32, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class ModeleForm(forms.Form):
    MODELE_OPTIONS = (
                ("Classification", "classification"),
                ("Regression", "regression"),
                )
    titre = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    sous_titre = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    inputs = forms.IntegerField(required=True)
    outputs = forms.IntegerField(required=True)
    mode = forms.MultipleChoiceField(widget=forms.MultipleChoiceField,
                                             choices=MODELE_OPTIONS)
    class Meta:
        model = Modele
        fields=('titre','sous_titre','outputs','inputs','mode',)

class LayerForm(forms.Form):
    activation = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    number = forms.IntegerField(required=True)
    class Meta:
        model = Layer
        fields=('activation','number',)

class TrainingForm(forms.Form):
    file = forms.FileField()
    epochs = forms.IntegerField(required=True)

class ProcessForm(forms.Form):
    file = forms.FileField()