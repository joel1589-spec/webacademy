from django.urls import path

from . import views

app_name = 'comptes'

urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.ConnexionView.as_view(), name='connexion'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('mon-espace/', views.mon_espace, name='mon_espace'),
    path('mon-espace/modifier/', views.modifier_profil, name='modifier_profil'),
    path('mes-attestations/', views.mes_attestations, name='mes_attestations'),
]
