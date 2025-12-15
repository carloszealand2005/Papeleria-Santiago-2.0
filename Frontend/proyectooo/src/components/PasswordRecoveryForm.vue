<template>
  <div class="flex items-center justify-center min-h-screen py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Password Recovery Card -->
      <div class="bg-white rounded-xl shadow-lg p-8 border border-gray-100">
        <!-- Header -->
        <div class="text-center mb-8">
          <div class="mx-auto h-12 w-12 bg-indigo-100 rounded-full flex items-center justify-center mb-4">
            <i class="fas fa-key text-indigo-600 text-xl"></i>
          </div>
          <h2 class="text-3xl font-bold text-gray-900">Recuperar Contraseña</h2>
          <p class="mt-2 text-sm text-gray-600">Ingresa tu correo electrónico y te enviaremos un enlace para restablecer tu contraseña</p>
        </div>

        <!-- Password Recovery Form -->
        <form @submit.prevent="handlePasswordReset" class="space-y-6" v-if="!emailSent">
          <!-- Email Field -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              Correo Electrónico
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <i class="fas fa-envelope text-gray-400 text-sm"></i>
              </div>
              <input
                id="email"
                v-model="formData.email"
                type="email"
                required
                class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg text-sm placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                :class="{ 'border-red-300': emailError }"
                placeholder="Ingresa tu correo electrónico"
                @blur="validateEmail"
              />
            </div>
            <p v-if="emailError" class="mt-1 text-xs text-red-600">{{ emailError }}</p>
          </div>

          <!-- Reset Button -->
          <button
            type="submit"
            :disabled="!isEmailValid"
            class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200 cursor-pointer"
          >
            <i v-if="isLoading" class="fas fa-spinner fa-spin mr-2"></i>
            {{ isLoading ? 'Enviando...' : 'Enviar Enlace de Recuperación' }}
          </button>
        </form>

        <!-- Success Message -->
        <div v-if="emailSent" class="text-center space-y-6">
          <div class="mx-auto h-16 w-16 bg-green-100 rounded-full flex items-center justify-center">
            <i class="fas fa-check text-green-600 text-2xl"></i>
          </div>
          <div>
            <h3 class="text-lg font-medium text-gray-900 mb-2">Enlace Enviado</h3>
            <p class="text-sm text-gray-600 mb-4">
              Hemos enviado un enlace de recuperación a <strong>{{ formData.email }}</strong>
            </p>
            <p class="text-xs text-gray-500 mb-6">
              Si no ves el correo en tu bandeja de entrada, revisa tu carpeta de spam.
            </p>
          </div>
          <button
            @click="resetForm"
            class="w-full flex justify-center py-3 px-4 border border-gray-300 rounded-lg shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-200 cursor-pointer"
          >
            Enviar de Nuevo
          </button>
        </div>

        <!-- Additional Information -->
        <div class="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-100" v-if="!emailSent">
          <div class="flex items-start">
            <div class="flex-shrink-0">
              <i class="fas fa-info-circle text-blue-500 text-sm mt-0.5"></i>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-blue-900">Información importante</h3>
              <p class="mt-1 text-xs text-blue-700">
                El enlace de recuperación será válido por 24 horas. Si no tienes acceso a tu correo electrónico, contacta con nuestro equipo de soporte.
              </p>
            </div>
          </div>
        </div>

        <!-- Back to Login -->
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            ¿Recordaste tu contraseña?
            <a href="#" class="font-medium text-indigo-600 hover:text-indigo-500 cursor-pointer" @click.prevent="goToLogin">
              Volver al Inicio de Sesión
            </a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PasswordRecoveryForm',
  data() {
    return {
      formData: {
        email: ''
      },
      isLoading: false,
      emailError: '',
      emailSent: false
    };
  },
  computed: {
    isEmailValid() {
      return (
        this.formData.email.trim() !== '' &&
        !this.emailError
      );
    }
  },
  methods: {
    validateEmail() {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (this.formData.email && !emailRegex.test(this.formData.email)) {
        this.emailError = 'Por favor, ingresa un correo electrónico válido';
      } else {
        this.emailError = '';
      }
    },
    async handlePasswordReset() {
      if (!this.isEmailValid) return;

      this.isLoading = true;
      try {
        // Simulate API call
        await new Promise(resolve => setTimeout(resolve, 2000));
        
        // Handle successful password reset request
        console.log('Solicitud de recuperación enviada para:', this.formData.email);
        this.emailSent = true;
        this.$emit('password-reset-success', this.formData.email);
      } catch (error) {
        console.error('Error al enviar la recuperación:', error);
        this.$emit('error', 'Error al enviar el enlace de recuperación. Por favor, inténtalo de nuevo.');
      } finally {
        this.isLoading = false;
      }
    },
    resetForm() {
      this.emailSent = false;
      this.formData.email = '';
      this.emailError = '';
    },
    goToLogin() {
      this.$emit('go-to-login');
    }
  }
}
</script>

<style scoped>
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type="number"] {
  -moz-appearance: textfield;
}

.transition {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
</style>

