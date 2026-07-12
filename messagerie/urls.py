from django.urls import path

from . import views

app_name = 'messagerie'

urlpatterns = [
    path('', views.ma_conversation, name='ma_conversation'),
    path('formateur/', views.liste_conversations, name='liste_conversations'),
    path('formateur/<int:conversation_id>/', views.conversation_detail, name='conversation_detail'),
]
