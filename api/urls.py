from django.urls import path
from . import views

urlpatterns = [
    path('notes/', views.notes_api),
    path('ipk/', views.ipk_api),
]