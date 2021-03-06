"""FinancialPredictions URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^new-model$', views.new_model, name='new-model'),
    url(r'^model/(\d+)$', views.model, name='model'),
    url(r'^new-layer/(\d+)$', views.new_layer, name='new-layer'),
    url(r'^train-model/(\d+)$', views.train_model, name='train_model'),
    url(r'^process-model/(\d+)$', views.process_model, name='process_model'),
    url(r'^connexion$', views.connexion, name='connexion'),
    url(r'^inscription$', views.inscription, name='inscription'),
    url(r'^deconnexion$', views.deconnexion, name='deconnexion'),
]
