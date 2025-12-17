from rest_framework import generics, permissions

from .models import Cliente
from .auth_serializers import RegistroSerializer
from rest_framework.response import Response
from rest_framework import status

class RegistroView(generics.CreateAPIView):
    queryset = Cliente.objects.all() # El queryset se usa para los permisos, pero la creación es de User y Cliente
    serializer_class = RegistroSerializer
    permission_classes = [permissions.AllowAny] # Permitir que cualquier usuario se registre

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"message": "Usuario registrado exitosamente.", "username": serializer.data['username'], "email": serializer.data['email']},
            status=status.HTTP_201_CREATED,
            headers=headers
        )

