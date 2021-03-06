# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import ConnexionForm, InscriptionForm, ModeleForm, LayerForm, TrainingForm, ProcessForm
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
import requests
import json
import csv
import pandas as pd
import os
from django.views.static import serve

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
            new_model.mode = form.cleaned_data.get('mode')
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

    print("Back-end id : "+str(model.back_end_id))
    if model.back_end_id == 0:
        is_trained=False
        accuracy=0
    else:
        try:
            url = 'http://m-learning.fr:50/'+str(model.back_end_id)
            r = requests.get(url, headers={'Token':'test_password_12345'}).json()["model"]
            if r['id_exists']:
                is_trained=r["trained"]
                if 'accuracy' in r:
                    accuracy=r["accuracy"]
                else:
                    accuracy=0
            else:
                is_trained=False
                accuracy=0
        except:
            is_trained=False
            accuracy=0
    #print(requests.get("http://m-learning.fr:50/1", headers={'Token':'test_password_12345'}).json()["model"]["trained"])
    models=[model]
    id_model=id
    try:
        layers = Layer.objects.all().filter(model=model)
    except:
        layers = []
    try:
        training_data=TrainingFiles.objects.all().filter(model=model)[0]
        training_data_url=training_data.url
    except:
        training_data=[]
        training_data_url=''
    return render(request, 'model.html', locals())
#requests.get("http://m-learning.fr:50/1", headers={'Token':'test_password_12345'}).json()["model"]["trained"]

@login_required
def train_model(request, id):
    try:
        model_ML = Modele.objects.all().get(id=id)
    except:
        return redirect('home')
    if model_ML.admin!=request.user:
        return redirect('home')
    if request.method == 'POST':
        file = request.FILES['file']

        if ("epochs" in request.POST):
            epochs=request.POST['epochs']
        else:
            epochs=1
        print(epochs)
        if(file.name[-4:]==".csv"):
            frame=pd.read_csv(file)
        elif(file.name[-5:]==".xlsx"):
            frame=pd.read_excel(file)
        else:
            frame=pd.DataFrame([])
        inputs=frame.shape[1]-1
        url_create = 'http://m-learning.fr:50/create'
        layers=Layer.objects.all().filter(model=model_ML)
        layers_table=[]
        for i in layers:
            layers_table.append({"activation":i.activation,"number":i.number})
        json_data={'mode':model_ML.mode,'layers':layers_table,'inputs':inputs,'outputs':model_ML.outputs,'description':'Test'}
        print(json_data)

        r_create=requests.post(url_create, headers={'Token':'test_password_12345', "Content-Type":"application/json"},data=json.dumps(json_data)).json()["id"]
        model_ML.back_end_id=r_create
        model_ML.save()
        print(os.listdir('../MachineLearningAPI/static/training'))
        frame.to_csv('../MachineLearningAPI/static/training/training_'+str(model_ML.back_end_id)+'.csv', index=False)
        print(os.listdir('../MachineLearningAPI/static/training'))
        url_train = 'http://m-learning.fr:50/train/'+str(model_ML.back_end_id)
        json_training_data={"epochs":epochs,"description":"Test"}
        r_train = requests.post(url_train, headers={'Token':'test_password_12345', "Content-Type":"application/json"},data=json.dumps(json_training_data))
        return model(request, id)
    else:
        form = TrainingForm()
        return render(request, 'form.html', locals())

@login_required
def process_model(request, id):
    try:
        model_ML = Modele.objects.all().get(id=id)
    except:
        return redirect('home')
    if model_ML.admin!=request.user:
        return redirect('home')
    if request.method == 'POST':
        file = request.FILES['file']
        if(file.name[-4:]==".csv"):
            frame=pd.read_csv(file)
        elif(file.name[-5:]==".xlsx"):
            frame=pd.read_excel(file)
        else:
            frame=pd.DataFrame([])
        frame.to_csv('../MachineLearningAPI/static/to_process/file_'+str(model_ML.back_end_id)+'.csv', index=False)
        url_process = 'http://m-learning.fr:50/process_file/'+str(model_ML.back_end_id)
        r_process = requests.get(url_process, headers={'Token':'test_password_12345', "Content-Type":"application/json"})
        url_serve='../MachineLearningAPI/static/processed/file_'+str(model_ML.back_end_id)+'.xlsx'
        return serve(request, os.path.basename(url_serve), os.path.dirname(url_serve))
    else:
        form = ProcessForm()
        return render(request, 'form.html', locals())

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

def upload_file(request):
    requests.get("http://m-learning.fr:50/1", headers={'Token':'test_password_12345'}).json()["model"]["trained"]

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