from django.urls import path

from . import views

app_name = 'attestations'

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('verifier/', views.verifier, name='verifier'),
    path('qr/<str:numero>/', views.qr_code, name='qr_code'),
    path('a-propos/', views.a_propos, name='a_propos'),
    path('mentions-legales/', views.mentions_legales, name='mentions_legales'),
    path('tableau-de-bord/', views.tableau_de_bord, name='tableau_de_bord'),
]
