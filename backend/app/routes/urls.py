# backend/app/routes/urls.py
from django.urls import path
from . import queries  # aquí importas los endpoints

urlpatterns = [
    path('test/', queries.test_endpoint),  # ejemplo
]
