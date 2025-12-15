<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <RegisterHeader 
      @go-to-home="handleGoToHome"
    />
    
    <!-- Botón para volver al home -->
    <div class="max-w-7xl mx-auto px-4 pt-4">
      <button 
        @click="goToHome"
        class="text-blue-600 hover:text-blue-700 font-medium transition-colors cursor-pointer"
      >
        <i class="fas fa-arrow-left mr-2"></i>Volver al inicio
      </button>
    </div>
    
    <PasswordRecoveryForm 
      @password-reset-success="handlePasswordResetSuccess"
      @go-to-login="handleGoToLogin"
      @error="handleError"
    />
    
    <RegisterFooter />
  </div>
</template>

<script>
import RegisterHeader from './RegisterHeader.vue';
import PasswordRecoveryForm from './PasswordRecoveryForm.vue';
import RegisterFooter from './RegisterFooter.vue';

export default {
  name: 'PasswordRecoveryPage',
  components: {
    RegisterHeader,
    PasswordRecoveryForm,
    RegisterFooter
  },
  methods: {
    goToHome() {
      this.$router.push('/');
    },
    handleGoToHome() {
      this.goToHome();
    },
    handlePasswordResetSuccess(email) {
      console.log('Solicitud de recuperación enviada para:', email);
    },
    handleGoToLogin() {
      this.$router.push('/login');
    },
    handleError(message) {
      console.error('Error en recuperación:', message);
      this.$emit('error', message);
    }
  }
}
</script>

<style scoped>
</style>

