from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token # Importar el modelo Token
from django.contrib.auth import authenticate # Importar la función authenticate
from django.contrib.auth.models import User # Necesario para el queryset de LoginView
from .models import Cliente
from .auth_serializers import RegistroSerializer, LoginSerializer # Importar también LoginSerializer
from rest_framework.response import Response
from rest_framework import status

class RegistroView(generics.CreateAPIView):
    queryset = Cliente.objects.all() # El queryset se usa para los permisos, pero la creación es de User y Cliente
    serializer_class = RegistroSerializer
    permission_classes = [permissions.AllowAny] # Permitir que cualquier usuario se registre

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save() # Guarda el usuario y el cliente
        # Crear un token para el usuario recién registrado
        token, created = Token.objects.get_or_create(user=user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Usuario registrado exitosamente.", "username": user.username, "email": user.email, "token": token.key},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny] # Permitir login sin autenticación

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "username": user.username,
            "email": user.email,
            "message": "Inicio de sesión exitoso."
        }, status=status.HTTP_200_OK)