from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Cliente, Carrito # Importar también el modelo Carrito

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
        
        cliente = Cliente.objects.create( # Almacenar la instancia del Cliente creado
            user=user,
            nombre=user.username, # Nombre del cliente igual al username
            email=user.email,     # Email del cliente igual al email del user
            tipo_cliente='Persona' # Asignar un tipo de cliente por defecto
        )

        # Crear un carrito para el cliente recién creado
        # NOTA: El ID del carrito será autogenerado y no será el mismo que el del usuario,
        # pero el carrito estará asociado directamente a este cliente y, por ende, a este usuario.
        Carrito.objects.create(
            cliente=cliente
        )
        
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not (username or email):
            raise serializers.ValidationError("Debe proporcionar un nombre de usuario o un correo electrónico.")

        user = None
        if username:
            user = User.objects.filter(username=username).first()
        elif email:
            user = User.objects.filter(email=email).first()
        
        if user and user.check_password(password):
            # Bloqueo por estado de cuenta (Mayoristas pendientes / cuentas inactivas)
            # Nota: para superusuarios/staff dejamos pasar.
            if not (user.is_superuser or user.is_staff):
                if not user.is_active:
                    raise serializers.ValidationError("Tu cuenta no está activa. Si es una empresa, puede estar en revisión.")

                try:
                    cliente = user.cliente_profile
                except Cliente.DoesNotExist:
                    cliente = None

                if cliente and getattr(cliente, 'estado_cuenta', None) and cliente.estado_cuenta != Cliente.ACTIVO:
                    raise serializers.ValidationError("Tu cuenta no está activa. Si es una empresa, puede estar en revisión.")
            data['user'] = user
        else:
            raise serializers.ValidationError("Credenciales inválidas.")

        return data
