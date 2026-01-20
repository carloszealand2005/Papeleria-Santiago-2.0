<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <!-- Botón para volver al home -->
    <div class="max-w-7xl mx-auto px-4 pt-4">
      <button
        @click="goToHome"
        class="text-blue-600 hover:text-blue-700 font-medium transition-colors cursor-pointer"
      >
        <i class="fas fa-arrow-left mr-2"></i>Volver al inicio
      </button>
    </div>

    <RegisterForm
      variant="wholesale"
      @register-success="handleRegisterSuccess"
      @go-to-login="handleGoToLogin"
      @error="handleError"
    />

    <RegisterFooter />
  </div>
</template>

<script>
import RegisterForm from './RegisterForm.vue';
import RegisterFooter from './RegisterFooter.vue';

export default {
  name: 'RegisterWholesalePage',
  components: {
    RegisterForm,
    RegisterFooter
  },
  methods: {
    goToHome() {
      this.$router.push('/');
    },
    handleRegisterSuccess(data) {
      console.log('Registro mayorista exitoso:', data);
      const email = data?.email || '';
      if (email) {
        // Guardamos email temporal para el paso de verificación
        localStorage.setItem('pending-verification-email', email);
      }
      this.$router.push('/verificacion'); // Paso 2: verificación OTP
    },
    handleGoToLogin() {
      this.$router.push('/login');
    },
    handleError(message) {
      console.error('Error en registro mayorista:', message);
      this.$emit('error', message);
    }
  }
};
</script>

<style scoped>
</style>


