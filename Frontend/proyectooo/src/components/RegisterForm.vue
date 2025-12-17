<template>
  <div class="flex items-center justify-center min-h-screen py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-md w-full space-y-8">
      <!-- Registration Card -->
      <div class="bg-white rounded-xl shadow-lg p-8 border border-gray-100">
        <!-- Header -->
        <div class="text-center mb-8">
          <div class="mx-auto h-12 w-12 bg-indigo-100 rounded-full flex items-center justify-center mb-4">
            <i class="fas fa-user-plus text-indigo-600 text-xl"></i>
          </div>
          <h2 class="text-3xl font-bold text-gray-900">Crear Cuenta</h2>
          <p class="mt-2 text-sm text-gray-600">Únete a nuestra plataforma y comienza tu experiencia</p>
        </div>

        <!-- Registration Form -->
        <form @submit.prevent="handleRegister" class="space-y-6">
          <!-- Full Name Field -->
          <div>
            <label for="fullName" class="block text-sm font-medium text-gray-700 mb-2">
              Nombre Completo
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <i class="fas fa-user text-gray-400 text-sm"></i>
              </div>
              <input
                id="fullName"
                v-model="formData.fullName"
                type="text"
                required
                class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg text-sm placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                placeholder="Ingresa tu nombre completo"
              />
            </div>
          </div>

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
                placeholder="tu@ejemplo.com"
                @blur="validateEmail"
              />
            </div>
            <p v-if="emailError" class="mt-1 text-xs text-red-600">{{ emailError }}</p>
          </div>

          <!-- Password Field -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              Contraseña
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <i class="fas fa-lock text-gray-400 text-sm"></i>
              </div>
              <input
                id="password"
                v-model="formData.password"
                :type="showPassword ? 'text' : 'password'"
                required
                class="block w-full pl-10 pr-10 py-3 border border-gray-300 rounded-lg text-sm placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                placeholder="Crea una contraseña segura"
                @input="checkPasswordStrength"
              />
              <button
                type="button"
                class="absolute inset-y-0 right-0 pr-3 flex items-center cursor-pointer"
                @click="showPassword = !showPassword"
              >
                <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'" class="text-gray-400 text-sm"></i>
              </button>
            </div>
            <!-- Password Strength Indicator -->
            <div v-if="formData.password" class="mt-2">
              <div class="flex items-center space-x-2">
                <div class="flex-1 bg-gray-200 rounded-full h-2">
                  <div
                    class="h-2 rounded-full transition-all duration-300"
                    :class="passwordStrengthColor"
                    :style="{ width: passwordStrengthWidth }"
                  ></div>
                </div>
                <span class="text-xs font-medium" :class="passwordStrengthTextColor">
                  {{ passwordStrengthText }}
                </span>
              </div>
            </div>
          </div>

          <!-- Confirm Password Field -->
          <div>
            <label for="confirmPassword" class="block text-sm font-medium text-gray-700 mb-2">
              Confirmar Contraseña
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <i class="fas fa-lock text-gray-400 text-sm"></i>
              </div>
              <input
                id="confirmPassword"
                v-model="formData.confirmPassword"
                :type="showConfirmPassword ? 'text' : 'password'"
                required
                class="block w-full pl-10 pr-10 py-3 border border-gray-300 rounded-lg text-sm placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                :class="{ 'border-red-300': passwordMismatch }"
                placeholder="Confirma tu contraseña"
                @blur="checkPasswordMatch"
              />
              <button
                type="button"
                class="absolute inset-y-0 right-0 pr-3 flex items-center cursor-pointer"
                @click="showConfirmPassword = !showConfirmPassword"
              >
                <i :class="showConfirmPassword ? 'fas fa-eye-slash' : 'fas fa-eye'" class="text-gray-400 text-sm"></i>
              </button>
            </div>
            <p v-if="passwordMismatch" class="mt-1 text-xs text-red-600">Las contraseñas no coinciden</p>
          </div>

          <!-- Terms and Conditions -->
          <div class="space-y-3">
            <div class="flex items-start">
              <input
                id="acceptTerms"
                v-model="formData.acceptTerms"
                type="checkbox"
                required
                class="mt-1 h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
              />
              <label for="acceptTerms" class="ml-2 text-sm text-gray-600">
                Acepto los
                <a href="#" class="text-indigo-600 hover:text-indigo-500 cursor-pointer">Términos de Servicio</a>
                y la
                <a href="#" class="text-indigo-600 hover:text-indigo-500 cursor-pointer">Política de Privacidad</a>
              </label>
            </div>
            <div class="flex items-start">
              <input
                id="newsletter"
                v-model="formData.newsletter"
                type="checkbox"
                class="mt-1 h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
              />
              <label for="newsletter" class="ml-2 text-sm text-gray-600">
                Deseo recibir noticias y promociones por correo electrónico
              </label>
            </div>
          </div>

          <!-- Register Button -->
          <button
            type="submit"
            :disabled="!isFormValid"
            class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200 cursor-pointer"
          >
            <i v-if="isLoading" class="fas fa-spinner fa-spin mr-2"></i>
            {{ isLoading ? 'Creando cuenta...' : 'Crear Cuenta' }}
          </button>
        </form>

        <!-- Social Registration -->
        <div class="mt-6">
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-2 bg-white text-gray-500">O regístrate con</span>
            </div>
          </div>
          <div class="mt-6 grid grid-cols-2 gap-3">
            <button
              type="button"
              class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-lg shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 transition duration-200 cursor-pointer"
            >
              <i class="fab fa-google text-red-500 mr-2"></i>
              Google
            </button>
            <button
              type="button"
              class="w-full inline-flex justify-center py-2 px-4 border border-gray-300 rounded-lg shadow-sm bg-white text-sm font-medium text-gray-500 hover:bg-gray-50 transition duration-200 cursor-pointer"
            >
              <i class="fab fa-facebook text-blue-600 mr-2"></i>
              Facebook
            </button>
          </div>
        </div>

        <!-- Login Link -->
        <div class="mt-6 text-center">
          <p class="text-sm text-gray-600">
            ¿Ya tienes cuenta?
            <a href="#" class="font-medium text-indigo-600 hover:text-indigo-500 cursor-pointer" @click.prevent="goToLogin">
              Iniciar Sesión
            </a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'; // Importamos mapActions de Vuex

export default {
  name: 'RegisterForm',
  data() {
    return {
      formData: {
        fullName: '',
        email: '',
        password: '',
        confirmPassword: '',
        acceptTerms: false,
        newsletter: false
      },
      showPassword: false,
      showConfirmPassword: false,
      isLoading: false,
      emailError: '',
      passwordMismatch: false,
      passwordStrength: 0
    };
  },
  computed: {
    isFormValid() {
      return (
        this.formData.fullName.trim() !== '' &&
        this.formData.email.trim() !== '' &&
        this.formData.password.length >= 6 &&
        this.formData.confirmPassword === this.formData.password &&
        this.formData.acceptTerms &&
        !this.emailError
      );
    },
    passwordStrengthWidth() {
      return `${(this.passwordStrength / 4) * 100}%`;
    },
    passwordStrengthColor() {
      if (this.passwordStrength <= 1) return 'bg-red-500';
      if (this.passwordStrength <= 2) return 'bg-yellow-500';
      if (this.passwordStrength <= 3) return 'bg-blue-500';
      return 'bg-green-500';
    },
    passwordStrengthText() {
      if (this.passwordStrength <= 1) return 'Débil';
      if (this.passwordStrength <= 2) return 'Regular';
      if (this.passwordStrength <= 3) return 'Buena';
      return 'Fuerte';
    },
    passwordStrengthTextColor() {
      if (this.passwordStrength <= 1) return 'text-red-600';
      if (this.passwordStrength <= 2) return 'text-yellow-600';
      if (this.passwordStrength <= 3) return 'text-blue-600';
      return 'text-green-600';
    }
  },
  methods: {
    ...mapActions(['register']), // Mapeamos la acción 'register' de Vuex
    validateEmail() {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (this.formData.email && !emailRegex.test(this.formData.email)) {
        this.emailError = 'Por favor, ingresa un correo electrónico válido';
      } else {
        this.emailError = '';
      }
    },
    checkPasswordStrength() {
      const password = this.formData.password;
      let strength = 0;
      if (password.length >= 8) strength++;
      if (/[a-z]/.test(password)) strength++;
      if (/[A-Z]/.test(password)) strength++;
      if (/[0-9]/.test(password)) strength++;
      if (/[^A-Za-z0-9]/.test(password)) strength++;
      this.passwordStrength = Math.min(strength, 4);
    },
    checkPasswordMatch() {
      this.passwordMismatch = this.formData.confirmPassword !== '' &&
        this.formData.confirmPassword !== this.formData.password;
    },
    async handleRegister() {
      if (!this.isFormValid) return;

      this.isLoading = true;
      try {
        const response = await this.register({ // Llamamos a la acción 'register' de Vuex
          email: this.formData.email,
          username: this.formData.fullName,
          password: this.formData.password
        });

        console.log('Registro exitoso:', response);
        this.$emit('register-success', response);

      } catch (error) {
        console.error('Error en el registro:', error);
        const errorMessage = error.response && error.response.data && (error.response.data.email || error.response.data.username || error.response.data.password || error.response.data.detail)
                             ? (error.response.data.email || error.response.data.username || error.response.data.password || error.response.data.detail)
                             : 'Error al crear la cuenta. Por favor, inténtalo de nuevo.';
        this.$emit('error', errorMessage);
      } finally {
        this.isLoading = false;
      }
    },
    goToLogin() {
      this.$emit('go-to-login');
    }
  },
  watch: {
    'formData.confirmPassword'() {
      if (this.formData.confirmPassword) {
        this.checkPasswordMatch();
      }
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
