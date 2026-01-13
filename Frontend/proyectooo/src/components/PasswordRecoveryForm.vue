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
          <p class="mt-2 text-sm text-gray-600" v-if="step === 'request'">
            Ingresa tu correo electrónico y te enviaremos un código de verificación
          </p>
          <p class="mt-2 text-sm text-gray-600" v-else>
            Ingresa el código de 6 dígitos enviado a <span class="font-semibold text-gray-800">{{ formData.email || 'tu correo' }}</span>
            junto con tu nueva contraseña
          </p>
        </div>

        <div v-if="generalError" class="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
          {{ generalError }}
        </div>
        <div v-if="generalMessage" class="mb-4 p-3 bg-green-50 border border-green-200 text-green-700 rounded-lg text-sm">
          {{ generalMessage }}
        </div>

        <!-- ESTADO A: Solicitar Código -->
        <form @submit.prevent="handleRequestOtp" class="space-y-6" v-if="step === 'request'">
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

          <!-- Send OTP Button -->
          <button
            type="submit"
            :disabled="!isEmailValid || isLoadingRequest"
            class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200 cursor-pointer"
          >
            <i v-if="isLoadingRequest" class="fas fa-spinner fa-spin mr-2"></i>
            {{ isLoadingRequest ? 'Enviando...' : 'Enviar código de verificación' }}
          </button>
        </form>

        <!-- ESTADO B: Validar y Cambiar Contraseña -->
        <form @submit.prevent="handleConfirmReset" class="space-y-4" v-else novalidate>
          <div>
            <label for="new_password" class="block text-sm font-medium text-gray-700 mb-2">
              Nueva Contraseña
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <i class="fas fa-lock text-gray-400 text-sm"></i>
              </div>
              <input
                id="new_password"
                v-model="formData.new_password"
                type="password"
                required
                class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg text-sm placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                placeholder="Ingresa tu nueva contraseña"
                @input="clearMessages"
              />
            </div>
          </div>

          <div>
            <label for="confirm_password" class="block text-sm font-medium text-gray-700 mb-2">
              Confirmar Nueva Contraseña
            </label>
            <div class="relative">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <i class="fas fa-lock text-gray-400 text-sm"></i>
              </div>
              <input
                id="confirm_password"
                v-model="formData.confirm_password"
                type="password"
                required
                class="block w-full pl-10 pr-3 py-3 border border-gray-300 rounded-lg text-sm placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
                placeholder="Confirma tu nueva contraseña"
                @input="clearMessages"
              />
            </div>
            <p v-if="passwordError" class="mt-1 text-xs text-red-600">{{ passwordError }}</p>
          </div>

          <div>
            <label for="otp_code" class="block text-sm font-medium text-gray-700 mb-2">
              Código de Verificación
            </label>
            <input
              id="otp_code"
              v-model="formData.otp_code"
              type="text"
              inputmode="numeric"
              pattern="[0-9]{6}"
              maxlength="6"
              class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 text-sm tracking-widest text-center"
              placeholder="123456"
              @input="sanitizeOtp"
            />
            <p v-if="otpError" class="mt-1 text-xs text-red-600">{{ otpError }}</p>
          </div>

          <button
            type="submit"
            :disabled="isLoadingConfirm || !!otpError || !!passwordError || formData.otp_code.length !== 6"
            class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200 cursor-pointer"
          >
            <i v-if="isLoadingConfirm" class="fas fa-spinner fa-spin mr-2"></i>
            {{ isLoadingConfirm ? 'Cambiando...' : 'Cambiar Contraseña' }}
          </button>

          <button
            type="button"
            :disabled="isResending || resendCooldown > 0 || resendCountLocal >= maxResends"
            class="w-full flex justify-center py-3 px-4 border border-gray-300 rounded-lg shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200 cursor-pointer"
            @click="handleResend"
          >
            <i v-if="isResending" class="fas fa-spinner fa-spin mr-2"></i>
            <span v-if="resendCountLocal >= maxResends">Límite de reenvíos alcanzado</span>
            <span v-else-if="resendCooldown > 0">Reenviar código ({{ resendCooldown }}s)</span>
            <span v-else>{{ isResending ? 'Reenviando...' : 'Reenviar código' }}</span>
          </button>

          <button
            type="button"
            class="w-full flex justify-center py-3 px-4 border border-gray-300 rounded-lg shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-200 cursor-pointer"
            @click="resetAll"
          >
            Volver
          </button>
        </form>

        <!-- Additional Information -->
        <div class="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-100" v-if="step === 'request'">
          <div class="flex items-start">
            <div class="flex-shrink-0">
              <i class="fas fa-info-circle text-blue-500 text-sm mt-0.5"></i>
            </div>
            <div class="ml-3">
              <h3 class="text-sm font-medium text-blue-900">Información importante</h3>
              <p class="mt-1 text-xs text-blue-700">
                El código de verificación tiene expiración. Si no ves el correo en tu bandeja de entrada, revisa tu carpeta de spam.
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
import api from '../utils/api';

export default {
  name: 'PasswordRecoveryForm',
  data() {
    return {
      formData: {
        email: '',
        new_password: '',
        confirm_password: '',
        otp_code: ''
      },
      step: 'request', // 'request' | 'confirm'
      isLoadingRequest: false,
      isLoadingConfirm: false,
      isResending: false,
      emailError: '',
      otpError: '',
      passwordError: '',
      generalError: '',
      generalMessage: '',
      resendCooldown: 90,
      cooldownTimer: null,
      resendCountLocal: 0,
      maxResends: 3,
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
  beforeDestroy() {
    if (this.cooldownTimer) clearInterval(this.cooldownTimer);
  },
  methods: {
    clearMessages() {
      this.generalError = '';
      this.generalMessage = '';
    },
    validateEmail() {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (this.formData.email && !emailRegex.test(this.formData.email)) {
        this.emailError = 'Por favor, ingresa un correo electrónico válido';
      } else {
        this.emailError = '';
      }
    },
    sanitizeOtp() {
      this.formData.otp_code = String(this.formData.otp_code || '').replace(/[^0-9]/g, '').slice(0, 6);
      this.otpError = this.formData.otp_code.length === 0 ? 'El código es requerido.' : (this.formData.otp_code.length < 6 ? 'El código debe tener 6 dígitos.' : '');
      this.generalError = '';
    },
    validatePasswords() {
      if (!this.formData.new_password || !this.formData.confirm_password) {
        this.passwordError = '';
        return;
      }
      this.passwordError = this.formData.new_password === this.formData.confirm_password ? '' : 'Las contraseñas no coinciden.';
    },
    startCooldown(seconds = 90) {
      this.resendCooldown = seconds;
      if (this.cooldownTimer) clearInterval(this.cooldownTimer);
      this.cooldownTimer = setInterval(() => {
        this.resendCooldown -= 1;
        if (this.resendCooldown <= 0) {
          this.resendCooldown = 0;
          clearInterval(this.cooldownTimer);
          this.cooldownTimer = null;
        }
      }, 1000);
    },
    async handleRequestOtp() {
      this.clearMessages();
      this.validateEmail();
      if (!this.isEmailValid) return;

      this.isLoadingRequest = true;
      try {
        const res = await api.post('/solicitar-recuperacion/', { email: this.formData.email });
        this.generalMessage = res?.data?.message || 'Si el correo existe, se ha enviado un código de verificación.';
        this.step = 'confirm';
        this.resendCountLocal = 0;
        this.startCooldown(90); // botón "Reenviar código" deshabilitado inicialmente 90s
        this.$emit('password-reset-success', this.formData.email);
      } catch (error) {
        const message = error?.response?.data?.error || error?.response?.data?.detail || 'Error al enviar el código. Por favor, inténtalo de nuevo.';
        this.generalError = message;
        this.$emit('error', message);
      } finally {
        this.isLoadingRequest = false;
      }
    },
    async handleConfirmReset() {
      this.clearMessages();
      this.sanitizeOtp();
      this.validatePasswords();

      if (this.passwordError) return;
      if (this.formData.new_password !== this.formData.confirm_password) {
        this.passwordError = 'Las contraseñas no coinciden.';
        return;
      }
      if (this.otpError || this.formData.otp_code.length !== 6) return;

      this.isLoadingConfirm = true;
      try {
        const payload = {
          email: this.formData.email,
          otp_code: this.formData.otp_code,
          new_password: this.formData.new_password,
          confirm_password: this.formData.confirm_password,
        };
        const res = await api.post('/confirmar-recuperacion/', payload);
        this.generalMessage = res?.data?.message || 'Contraseña actualizada exitosamente.';
        // UX: podemos redirigir al login tras éxito
        setTimeout(() => this.goToLogin(), 800);
      } catch (error) {
        const message = error?.response?.data?.error || error?.response?.data?.detail || 'No se pudo cambiar la contraseña.';
        this.generalError = message;
        this.$emit('error', message);
      } finally {
        this.isLoadingConfirm = false;
      }
    },
    async handleResend() {
      this.clearMessages();
      if (!this.formData.email) return;
      if (this.resendCountLocal >= this.maxResends) return;
      if (this.resendCooldown > 0) return;

      this.isResending = true;
      try {
        const res = await api.post('/solicitar-recuperacion/', { email: this.formData.email });
        this.generalMessage = res?.data?.message || 'Si el correo existe, se ha enviado un código de verificación.';
        this.resendCountLocal += 1;
        this.startCooldown(90);
      } catch (error) {
        const message = error?.response?.data?.error || error?.response?.data?.detail || 'No se pudo reenviar el código.';
        this.generalError = message;
        this.$emit('error', message);
      } finally {
        this.isResending = false;
      }
    },
    resetAll() {
      this.clearMessages();
      this.step = 'request';
      this.formData.new_password = '';
      this.formData.confirm_password = '';
      this.formData.otp_code = '';
      this.otpError = '';
      this.passwordError = '';
      this.resendCountLocal = 0;
      this.resendCooldown = 90;
      if (this.cooldownTimer) {
        clearInterval(this.cooldownTimer);
        this.cooldownTimer = null;
      }
    },
    goToLogin() {
      this.$emit('go-to-login');
    }
  },
  watch: {
    'formData.confirm_password'() {
      this.validatePasswords();
    },
    'formData.new_password'() {
      this.validatePasswords();
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

