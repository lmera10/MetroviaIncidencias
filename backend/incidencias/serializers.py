from rest_framework import serializers
from .models import Incidencia, Categoria
from django.contrib.auth.models import User

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class IncidenciaSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), source='categoria', write_only=True
    )

    class Meta:
        model = Incidencia
        fields = ['id', 'titulo', 'descripcion', 'categoria', 'categoria_id', 'estado', 'usuario', 'fecha_creacion']
