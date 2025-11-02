from django.contrib import admin
from .models import Incidencia, Categoria

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

@admin.register(Incidencia)
class IncidenciaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'usuario', 'categoria', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'categoria', 'fecha_creacion')
    search_fields = ('titulo', 'descripcion', 'usuario__username')


