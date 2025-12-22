<template>
  <div class="flex items-center justify-center min-h-screen py-12 px-4">
    <div class="max-w-md w-full space-y-8">
      <!-- Login Card -->
      <div class="bg-white rounded-xl shadow-2xl p-8">
        <!-- Header -->
        <div class="text-center mb-8">
          <img 
            src="https://static.readdy.ai/image/a6354382ff0904464d2c460063bc60ba/ea51eb4ba2a53ef142a962fbf9bc4d85.jpeg" 
            alt="Santiago Papelería" 
            class="h-16 w-auto mx-auto mb-4"
          >
          <h2 class="text-3xl font-bold text-gray-900 mb-2">Iniciar Sesión</h2>
          <p class="text-gray-600">Accede a tu cuenta de Papelería Santiago</p>
        </div>

        <!-- User Type Selection -->
        <div class="mb-6">
          <div class="flex bg-gray-100 rounded-lg p-1">
            <button 
              @click="setUserType('individual')" 
              :class="userType === 'individual' ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-600'"
              class="flex-1 py-2 px-4 !rounded-button whitespace-nowrap transition-all cursor-pointer font-medium"
            >
              <i class="fas fa-user mr-2"></i>Cliente Individual
            </button>
            <button 
              @click="setUserType('wholesale')" 
              :class="userType === 'wholesale' ? 'bg-white text-blue-600 shadow-sm' : 'text-gray-600'"
              class="flex-1 py-2 px-4 !rounded-button whitespace-nowrap transition-all cursor-pointer font-medium"
            >
              <i class="fas fa-building mr-2"></i>Mayorista
            </button>
          </div>
        </div>

        <!-- Mensaje de error del servidor -->
        <div v-if="serverError" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
          <strong class="font-bold">¡Error!</strong>
          <span class="block sm:inline"> {{ serverError }}</span>
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleLogin" class="space-y-6">
          <!-- Email Field -->
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700 mb-2">
              {{ userType === 'wholesale' ? 'Email Empresarial' : 'Email' }}
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <i class="fas fa-envelope text-gray-400 text-sm"></i>
              </div>
              <input 
                v-model="loginForm.email"
                type="email" 
                id="email"
                required
                class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors text-sm"
                :placeholder="userType === 'wholesale' ? 'empresa@ejemplo.com' : 'tu@email.com'"
                @input="clearServerError"
              >
            </div>
          </div>

          <!-- Password Field -->
          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">Contraseña</label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <i class="fas fa-lock text-gray-400 text-sm"></i>
              </div>
              <input 
                v-model="loginForm.password"
                :type="showPassword ? 'text' : 'password'"
                id="password"
                required
                class="block w-full pl-10 pr-12 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors text-sm"
                placeholder="Ingresa tu contraseña"
                @input="clearServerError"
              >
              <button 
                type="button"
                @click="togglePassword"
                class="absolute inset-y-0 right-0 pr-3 flex items-center cursor-pointer"
              >
                <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'" class="text-gray-400 text-sm"></i>
              </button>
            </div>
          </div>

          <!-- Additional fields for wholesale users (mantener si es relevante para el futuro) -->
          <div v-if="userType === 'wholesale'" class="space-y-4">
            <div>
              <label for="company" class="block text-sm font-medium text-gray-700 mb-2">Nombre de la Empresa</label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <i class="fas fa-building text-gray-400 text-sm"></i>
                </div>
                <input 
                  v-model="loginForm.company"
                  type="text" 
                  id="company"
                  class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors text-sm"
                  placeholder="Nombre de tu empresa"
                >
              </div>
            </div>
          </div>

          <!-- Remember me & Forgot password -->
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <input 
                v-model="loginForm.rememberMe"
                id="remember-me" 
                type="checkbox" 
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 !rounded-button"
              >
              <label for="remember-me" class="ml-2 block text-sm text-gray-700">
                Recordarme
              </label>
            </div>
            <a 
              href="#" 
              class="text-sm text-blue-600 hover:text-blue-500 cursor-pointer"
              @click.prevent="$emit('forgot-password')"
            >
              ¿Olvidaste tu contraseña?
            </a>
          </div>

          <!-- Submit Button -->
          <button 
            type="submit"
            :disabled="isLoading"
            class="w-full flex justify-center py-3 px-4 border border-transparent !rounded-button shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors whitespace-nowrap"
          >
            <i v-if="isLoading" class="fas fa-spinner fa-spin mr-2"></i>
            {{ isLoading ? 'Iniciando sesión...' : 'Iniciar Sesión' }}
          </button>
        </form>

        <!-- Divider -->
        <div class="mt-6">
          <div class="relative">
            <div class="absolute inset-0 flex items-center">
              <div class="w-full border-t border-gray-300"></div>
            </div>
            <div class="relative flex justify-center text-sm">
              <span class="px-2 bg-white text-gray-500">¿No tienes cuenta?</span>
            </div>
          </div>
        </div>

        <!-- Register Links -->
        <div class="mt-4 space-y-2">
          <button 
            @click="goToRegister('individual')"
            class="w-full text-center py-2 px-4 border border-gray-300 !rounded-button text-sm font-medium text-gray-700 hover:bg-gray-50 transition-colors cursor-pointer whitespace-nowrap"
          >
            Registrarse como Cliente Individual
          </button>
          <button 
            @click="goToRegister('wholesale')"
            class="w-full text-center py-2 px-4 border border-blue-600 !rounded-button text-sm font-medium text-blue-600 hover:bg-blue-50 transition-colors cursor-pointer whitespace-nowrap"
          >
            Registrarse como Mayorista
          </button>
        </div>

        <!-- Wholesale Benefits -->
        <div v-if="userType === 'wholesale'" class="mt-6 p-4 bg-blue-50 rounded-lg">
          <h3 class="text-sm font-semibold text-blue-900 mb-2">
            <i class="fas fa-star mr-2"></i>Beneficios Mayoristas
          </h3>
          <ul class="text-xs text-blue-800 space-y-1">
            <li><i class="fas fa-check mr-2"></i>Descuentos especiales por volumen</li>
            <li><i class="fas fa-check mr-2"></i>Crédito comercial disponible</li>
            <li><i class="fas fa-check mr-2"></i>Atención personalizada</li>
            <li><i class="fas fa-check mr-2"></i>Catálogo exclusivo</li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'; // Importamos mapActions de Vuex

export default {
  name: 'LoginForm',
  data() {
    return {
      userType: 'individual',
      showPassword: false,
      isLoading: false,
      serverError: null, // Nuevo: para errores del servidor
      loginForm: {
        email: '',
        password: '',
        company: '',
        rememberMe: false
      }
    }
  },
  methods: {
    ...mapActions(['login']), // Mapeamos la acción 'login' de Vuex
    setUserType(type) {
      this.userType = type;
      // Limpiar campos específicos al cambiar tipo
      if (type === 'individual') {
        this.loginForm.company = '';
      }
      this.$emit('user-type-changed', type);
    },
    togglePassword() {
      this.showPassword = !this.showPassword;
    },
    clearServerError() {
      this.serverError = null;
    },
    async handleLogin() {
      this.isLoading = true;
      this.serverError = null; // Limpiar errores previos

      try {
        // Validación básica (mantener por si acaso, aunque el backend también validará)
        if (!this.loginForm.email || !this.loginForm.password) {
          this.serverError = 'Por favor, ingresa tu correo y contraseña.';
          return;
        }

        // Llamar a la acción 'login' de Vuex
        const response = await this.login({ 
          email: this.loginForm.email,
          password: this.loginForm.password
        });

        console.log('Inicio de sesión exitoso:', response);
        this.$emit('login-success', response); // Emitir evento de login exitoso
        
        // Redirigir al home después de un login exitoso
        this.$router.push('/');

      } catch (error) {
        console.error('Error en el inicio de sesión:', error);
        if (error.response && error.response.data && error.response.data.non_field_errors) {
          this.serverError = error.response.data.non_field_errors[0];
        } else {
          this.serverError = 'Error al iniciar sesión. Por favor, inténtalo de nuevo.';
        }
      } finally {
        this.isLoading = false;
      }
    },
    goToRegister(type) {
      console.log(`Redirigiendo a registro: ${type}`);
      this.$emit('go-to-register', type);
    }
  }
}
</script>

<style scoped>
/* Las clases de Tailwind CSS ya están en el template */
</style>
