from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Cliente

class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este correo electrónico ya está en uso.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        Cliente.objects.create(
            user=user,
            nombre=user.username, # Nombre del cliente igual al username
            email=user.email,     # Email del cliente igual al email del user
            tipo_cliente='Persona' # Asignar un tipo de cliente por defecto
        )
        return user

