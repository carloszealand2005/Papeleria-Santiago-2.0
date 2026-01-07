<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center px-4 py-12">
    <div class="w-full max-w-md">
      <div class="bg-white rounded-xl shadow-lg p-8 border border-gray-100">
        <div class="text-center mb-6">
          <div class="mx-auto h-12 w-12 bg-indigo-100 rounded-full flex items-center justify-center mb-4">
            <i class="fas fa-shield-alt text-indigo-600 text-xl"></i>
          </div>
          <h2 class="text-2xl font-bold text-gray-900">Verifica tu correo</h2>
          <p class="mt-2 text-sm text-gray-600">
            Ingresa el código de 6 dígitos enviado a
            <span class="font-semibold text-gray-800">{{ email || 'tu correo' }}</span>
          </p>
        </div>

        <div v-if="generalError" class="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
          {{ generalError }}
        </div>

        <form @submit.prevent="handleVerify" novalidate class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Código</label>
            <input
              v-model="otp"
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
            :disabled="isVerifying || !!otpError || otp.length !== 6 || !email"
            class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200"
          >
            <i v-if="isVerifying" class="fas fa-spinner fa-spin mr-2"></i>
            {{ isVerifying ? 'Verificando...' : 'Verificar Cuenta' }}
          </button>

          <button
            type="button"
            :disabled="isResending || resendCooldown > 0 || !email"
            class="w-full flex justify-center py-3 px-4 border border-gray-300 rounded-lg shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition duration-200"
            @click="handleResend"
          >
            <i v-if="isResending" class="fas fa-spinner fa-spin mr-2"></i>
            <span v-if="resendCooldown > 0">Reenviar Código ({{ resendCooldown }}s)</span>
            <span v-else>{{ isResending ? 'Reenviando...' : 'Reenviar Código' }}</span>
          </button>
        </form>

        <div class="mt-6 text-center text-xs text-gray-500">
          ¿Ingresaste un correo equivocado?
          <button class="text-indigo-600 hover:text-indigo-700 font-medium" @click="goToRegister">
            Volver al registro
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions, mapGetters } from 'vuex';

export default {
  name: 'VerificationCode',
  data() {
    return {
      otp: '',
      otpError: '',
      generalError: '',
      isVerifying: false,
      isResending: false,
      resendCooldown: 0,
      cooldownTimer: null,
    };
  },
  computed: {
    ...mapGetters(['pendingVerificationEmail']),
    email() {
      return this.pendingVerificationEmail || localStorage.getItem('pending-verification-email') || '';
    },
  },
  beforeDestroy() {
    if (this.cooldownTimer) clearInterval(this.cooldownTimer);
  },
  methods: {
    ...mapActions(['verifyOtp', 'resendOtp']),
    sanitizeOtp() {
      this.otp = String(this.otp || '').replace(/[^0-9]/g, '').slice(0, 6);
      this.otpError = this.otp.length === 0 ? 'El código es requerido.' : (this.otp.length < 6 ? 'El código debe tener 6 dígitos.' : '');
      this.generalError = '';
    },
    startCooldown(seconds = 30) {
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
    async handleVerify() {
      this.generalError = '';
      this.sanitizeOtp();
      if (this.otpError || !this.email) return;

      this.isVerifying = true;
      try {
        await this.verifyOtp({ email: this.email, otp: this.otp });
        // Login automático (token ya guardado en Vuex + localStorage por la acción)
        this.$router.push('/');
      } catch (error) {
        const message = error?.response?.data?.error || error?.response?.data?.detail || 'No se pudo verificar el código.';
        this.generalError = message;
      } finally {
        this.isVerifying = false;
      }
    },
    async handleResend() {
      this.generalError = '';
      if (!this.email) return;

      this.isResending = true;
      try {
        await this.resendOtp({ email: this.email });
        this.startCooldown(30);
      } catch (error) {
        const message = error?.response?.data?.error || error?.response?.data?.detail || 'No se pudo reenviar el código.';
        this.generalError = message;
      } finally {
        this.isResending = false;
      }
    },
    goToRegister() {
      localStorage.removeItem('pending-verification-email');
      this.$router.push('/registro');
    },
  },
  created() {
    // UX: si ya hay email, iniciamos cooldown corto si venimos de un envío reciente
    // (si quieres persistir el tiempo exacto, podemos guardarlo en localStorage).
    if (this.email) {
      this.sanitizeOtp();
    }
  },
};
</script>

<style scoped>
</style>


