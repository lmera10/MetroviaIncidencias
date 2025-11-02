from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('incidencias.urls')),
    path('', RedirectView.as_view(url='http://localhost:3000')),  # React frontend
]

