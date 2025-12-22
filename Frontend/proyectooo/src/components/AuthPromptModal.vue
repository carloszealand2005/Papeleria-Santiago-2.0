<template>
  <!-- Login Modal UI -->
  <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center">


    <!-- Fondo oscuro -->
    <div class="absolute inset-0 bg-black bg-opacity-25" @click="closeModal"></div>

    <!-- Ventana -->
    <div class="relative bg-white rounded-2xl shadow-2xl max-w-lg w-full mx-4 p-10">

      <!-- Botón cerrar -->
      <button class="absolute top-4 right-4 text-gray-400 hover:text-gray-600" @click="closeModal">
        <i class="fas fa-times text-lg"></i>
      </button>

      <!-- Ícono -->
      <div class="text-center mb-6">
        <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
          <i class="fas fa-shopping-cart text-blue-600 text-2xl"></i>
        </div>

        <!-- Título -->
        <h3 class="text-xl font-semibold text-gray-900 mb-2">
          ¡Únete a Papelería Santiago!
        </h3>

        <!-- Texto -->
        <p class="text-gray-600 text-sm">
          Necesitas estar registrado o logueado en el sistema para añadir este producto a tu carrito.
          <span class="font-medium text-blue-600">Tomará menos de un minuto.</span>
        </p>
      </div>

      <!-- Botones -->
      <div class="space-y-3">
        <button class="w-full px-6 py-3 bg-blue-600 text-white rounded-lg font-medium" @click="goToRegister">
          <i class="fas fa-user-plus mr-2"></i>
          Registrarse
        </button>

        <button class="w-full px-6 py-3 bg-gray-100 text-gray-700 rounded-lg font-medium" @click="goToLogin">
          <i class="fas fa-sign-in-alt mr-2"></i>
          Ya tengo cuenta
        </button>

        <button class="w-full text-gray-500 text-sm" @click="continueShopping">
          Seguir viendo catálogo
        </button>
      </div>

      <!-- Beneficios -->
      <div class="mt-6 pt-6 border-t border-gray-100">
        <p class="text-xs text-gray-500 text-center mb-3">
          Beneficios de registrarte:
        </p>

        <div class="grid grid-cols-2 gap-3 text-xs text-gray-600">
          <div class="flex items-center">
            <i class="fas fa-check text-green-500 mr-2"></i>
            Carrito guardado
          </div>
          <div class="flex items-center">
            <i class="fas fa-check text-green-500 mr-2"></i>
            Ofertas exclusivas
          </div>
          <div class="flex items-center">
            <i class="fas fa-check text-green-500 mr-2"></i>
            Historial de compras
          </div>
          <div class="flex items-center">
            <i class="fas fa-check text-green-500 mr-2"></i>
            Envío rápido
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: 'AuthPromptModal',
  props: {
    showModal: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    closeModal() {
      this.$emit('close');
    },
    goToRegister() {
      this.$emit('go-to-register');
    },
    goToLogin() {
      this.$emit('go-to-login');
    },
    continueShopping() {
      this.$emit('continue-shopping');
    },
  },
};
</script>

<style scoped>
/* Tailwind CSS clases ya están en el template, no se necesitan estilos adicionales a menos que se desee algo muy específico */
</style>

