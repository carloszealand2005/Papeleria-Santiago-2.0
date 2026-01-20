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
              {{ fullNameLabel }}
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
                :class="{ 'border-red-300': serverErrors.username }"
                :placeholder="fullNamePlaceholder"
              />
            </div>
            <p v-if="serverErrors.username" class="mt-1 text-xs text-red-600">{{ serverErrors.username[0] }}</p>
          </div>

          <!-- Documento/Archivo Field (solo mayoristas) -->
          <div v-if="isWholesale">
            <label for="documentUrl" class="block text-sm font-medium text-gray-700 mb-2">
              Documento/Archivo (URL)
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <i class="fas fa-link text-gray-400 text-sm"></i>
              </div>
              <input
                id="documentUrl"
                v-model="formData.documentUrl"
                type="url"
                required
                class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg text-sm placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                :class="{ 'border-red-300': !!documentUrlError }"
                placeholder="https://drive.google.com/..."
                @blur="validateDocumentUrl"
              />
            </div>
            <p v-if="documentUrlError" class="mt-1 text-xs text-red-600">{{ documentUrlError }}</p>
            <p v-else class="mt-1 text-xs text-gray-500">
              Sube un documento a la nube y pega aquí el enlace para validar la empresa.
            </p>
          </div>

          <!-- Ciudad y Dirección (solo mayoristas) -->
          <div v-if="isWholesale" class="space-y-6">
            <!-- City Field -->
            <div>
              <label for="city" class="block text-sm font-medium text-gray-700 mb-2">
                Ciudad
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <i class="fas fa-city text-gray-400 text-sm"></i>
                </div>
                <input
                  id="city"
                  v-model="formData.city"
                  type="text"
                  class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg text-sm placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  placeholder="Ingresa tu ciudad"
                />
              </div>
            </div>

            <!-- Address Field -->
            <div>
              <label for="address" class="block text-sm font-medium text-gray-700 mb-2">
                Dirección
              </label>
              <div class="relative">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <i class="fas fa-map-marker-alt text-gray-400 text-sm"></i>
                </div>
                <input
                  id="address"
                  v-model="formData.address"
                  type="text"
                  class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg text-sm placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                  placeholder="Ingresa tu dirección"
                />
              </div>
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
                :class="{ 'border-red-300': emailError || serverErrors.email }"
                placeholder="tu@ejemplo.com"
                @blur="validateEmail"
              />
            </div>
            <p v-if="emailError" class="mt-1 text-xs text-red-600">{{ emailError }}</p>
            <p v-if="serverErrors.email" class="mt-1 text-xs text-red-600">{{ serverErrors.email[0] }}</p>
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
                :class="{ 'border-red-300': serverErrors.password }"
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
            <p v-if="serverErrors.password" class="mt-1 text-xs text-red-600">{{ serverErrors.password[0] }}</p>
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
            :disabled="!isFormValid || isLoading"
            class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200 cursor-pointer"
          >
            <i v-if="isLoading" class="fas fa-spinner fa-spin mr-2"></i>
            {{ isLoading ? 'Creando cuenta...' : 'Crear Cuenta' }}
          </button>
        </form>

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
import { mapActions } from 'vuex';

export default {
  name: 'RegisterForm',
  props: {
    variant: {
      type: String,
      default: 'individual',
      validator: (v) => ['individual', 'wholesale'].includes(v),
    },
  },
  data() {
    return {
      formData: {
        fullName: '',
        documentUrl: '',
        city: '',
        address: '',
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
      documentUrlError: '',
      passwordMismatch: false,
      passwordStrength: 0,
      serverErrors: { // Nuevo objeto para almacenar errores del servidor
        username: null,
        email: null,
        password: null,
      },
    };
  },
  computed: {
    isWholesale() {
      return this.variant === 'wholesale';
    },
    fullNameLabel() {
      return this.isWholesale ? 'Razón Social' : 'Nombre Completo';
    },
    fullNamePlaceholder() {
      return this.isWholesale ? 'Ingresa la razón social' : 'Ingresa tu nombre completo';
    },
    isFormValid() {
      return (
        this.formData.fullName.trim() !== '' &&
        (!this.isWholesale || (this.formData.documentUrl.trim() !== '' && !this.documentUrlError)) &&
        this.formData.email.trim() !== '' &&
        this.formData.password.length >= 6 &&
        this.formData.confirmPassword === this.formData.password &&
        this.formData.acceptTerms &&
        !this.emailError &&
        !this.documentUrlError &&
        !this.serverErrors.username && // Considerar errores del servidor en la validez del formulario
        !this.serverErrors.email &&
        !this.serverErrors.password
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
    ...mapActions(['register']),
    validateDocumentUrl() {
      if (!this.isWholesale) {
        this.documentUrlError = '';
        return;
      }

      const value = String(this.formData.documentUrl || '').trim();
      if (!value) {
        this.documentUrlError = 'El enlace del documento es requerido';
        return;
      }

      try {
        // Validación simple: URL válida (http/https)
        const parsed = new URL(value);
        if (!['http:', 'https:'].includes(parsed.protocol)) {
          this.documentUrlError = 'Por favor, ingresa un enlace válido (http o https)';
          return;
        }
        this.documentUrlError = '';
      } catch (e) {
        this.documentUrlError = 'Por favor, ingresa un enlace válido';
      }
    },
    validateEmail() {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (this.formData.email && !emailRegex.test(this.formData.email)) {
        this.emailError = 'Por favor, ingresa un correo electrónico válido';
      } else {
        this.emailError = '';
      }
      this.serverErrors.email = null; // Limpiar error de servidor al validar cliente
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
      this.serverErrors.password = null; // Limpiar error de servidor al cambiar contraseña
    },
    checkPasswordMatch() {
      this.passwordMismatch = this.formData.confirmPassword !== '' &&
        this.formData.confirmPassword !== this.formData.password;
    },
    async handleRegister() {
      this.isLoading = true;
      // Limpiar errores previos del servidor
      this.serverErrors = { username: null, email: null, password: null };

      // Validaciones específicas (UI)
      if (this.isWholesale) {
        this.validateDocumentUrl();
      }

      if (!this.isFormValid) {
        this.isLoading = false;
        return;
      }

      try {
        const response = await this.register({ 
          email: this.formData.email,
          username: this.formData.fullName,
          password: this.formData.password,
          // Para mayoristas (Empresa) el backend requiere este campo como url_validacion
          url_validacion: this.isWholesale ? this.formData.documentUrl : '',
          tipo_cliente: this.isWholesale ? 'Empresa' : 'Persona',
          ciudad: this.formData.city,
          direccion: this.formData.address,
        });

        console.log('Registro exitoso:', response);
        this.$emit('register-success', response);

      } catch (error) {
        console.error('Error en el registro:', error);
        if (error.response && error.response.data) {
          const errors = error.response.data;
          if (errors.username) {
            this.serverErrors.username = errors.username;
          }
          if (errors.email) {
            this.serverErrors.email = errors.email;
          }
          if (errors.password) {
            this.serverErrors.password = errors.password;
          }
          // Emitir un error general si no hay errores de campo específicos o si hay un error 'detail'
          if (!errors.username && !errors.email && !errors.password && errors.detail) {
            this.$emit('error', errors.detail);
          } else if (!errors.username && !errors.email && !errors.password) {
            this.$emit('error', 'Error desconocido al crear la cuenta. Por favor, inténtalo de nuevo.');
          }
        } else {
          this.$emit('error', 'Error de red o servidor no disponible. Por favor, inténtalo de nuevo.');
        }
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
    },
    'formData.documentUrl'() {
      if (this.isWholesale) {
        this.validateDocumentUrl();
      } else {
        this.documentUrlError = '';
      }
    },
    'formData.email'() {
      this.serverErrors.email = null; // Limpiar error de email del servidor al cambiar el campo
    },
    'formData.fullName'() {
      this.serverErrors.username = null; // Limpiar error de username del servidor al cambiar el campo
    },
    'formData.password'() {
      this.serverErrors.password = null; // Limpiar error de password del servidor al cambiar el campo
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
  appearance: textfield;
  -moz-appearance: textfield;
}

.transition {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
</style>
