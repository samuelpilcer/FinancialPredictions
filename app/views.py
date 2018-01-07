# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import ConnexionForm, InscriptionForm, ModeleForm, LayerForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .models import Modele, Layer

# Create your views here.

def home(request):
    try:
        models = Modele.objects.all().filter(admin=request.user)
    except:
        models = []
    # Retourne nombre1, nombre2 et la somme des deux au tpl
    return render(request, 'index.html', locals())

@login_required
def new_model(request):
    if request.method == 'POST':
        form = ModeleForm(request.POST)
        if form.is_valid():
            new_model=Modele()
            new_model.titre=form.cleaned_data.get('titre')
            new_model.sous_titre=form.cleaned_data.get('sous_titre')
            new_model.admin=request.user
            new_model.inputs = form.cleaned_data.get('inputs')
            new_model.outputs = form.cleaned_data.get('outputs')
            new_model.save()
            return redirect('home')
    else:
        form = ModeleForm()
    return render(request, 'new.html', {'form': form})

@login_required
def new_layer(request, id):
    try:
        model = Modele.objects.all().get(id=id)
    except:
        return redirect('home')
    if request.method == 'POST':
        form = LayerForm(request.POST)
        if form.is_valid():
            new_layer=Layer()
            new_layer.model=model
            new_layer.number=form.cleaned_data.get('number')
            new_layer.activation=form.cleaned_data.get('activation')
            new_layer.save()
            return redirect('/model/'+str(id))
    else:
        form = LayerForm()
    return render(request, 'new.html', {'form': form})

@login_required
def model(request, id):
    try:
        model = Modele.objects.all().get(id=id)
    except:
        return redirect('home')
    if model.admin!=request.user:
        return redirect('home')
    models=[model]
    id_model=id
    try:
        layers = Layer.objects.all().filter(model=model)
    except:
        layers = []
    return render(request, 'model.html', locals())

def connexion(request):
    error = False

    if request.method == "POST":
        form = ConnexionForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)  # Nous vérifions si les données sont correctes
            if user:  # Si l'objet renvoyé n'est pas None
                login(request, user)  # nous connectons l'utilisateur
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
            else: # sinon une erreur sera affichée
                error = True
    else:
        form = ConnexionForm()

    return render(request, 'login.html', locals())

def inscription(request):
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            form.save()
            #For next version with email verif: https://farhadurfahim.github.io/post/django-registration-with-confirmation-email/
            #user.is_active = False
            #form.save()
            #current_site = get_current_site(request)
            #message = render_to_string('acc_active_email.html', {
            #    'user':user, 
            #    'domain':current_site.domain,
            #    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #    'token': account_activation_token.make_token(user),
            #})
            #mail_subject = 'Activate your blog account.'
            #to_email = form.cleaned_data.get('email')
            #email = EmailMessage(mail_subject, message, to=[to_email])
            #email.send()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('connexion')
    else:
        form = InscriptionForm()
    return render(request, 'register.html', {'form': form})

def deconnexion(request):
    logout(request)
    return redirect(reverse(connexion))