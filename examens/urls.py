from django.urls import path

from . import views

app_name = 'examens'

urlpatterns = [
    path('', views.liste_sujets, name='liste_sujets'),
    path('<int:sujet_id>/traiter/', views.traiter_sujet, name='traiter_sujet'),
    path('copie/<int:copie_id>/resultat/', views.resultat_copie, name='resultat_copie'),
]
