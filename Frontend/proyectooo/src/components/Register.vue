<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <!-- <RegisterHeader 
      @go-to-home="handleGoToHome"
    /> -->
    
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
      @register-success="handleRegisterSuccess"
      @go-to-login="handleGoToLogin"
      @error="handleError"
    />
    
    <RegisterFooter />
  </div>
</template>

<script>
// import RegisterHeader from './RegisterHeader.vue'; // Eliminado
import RegisterForm from './RegisterForm.vue';
import RegisterFooter from './RegisterFooter.vue';

export default {
  name: 'RegisterPage',
  components: {
    // RegisterHeader, // Eliminado
    RegisterForm,
    RegisterFooter
  },
  methods: {
    goToHome() {
      this.$router.push('/');
    },
    handleGoToHome() {
      this.goToHome();
    },
    handleRegisterSuccess(data) {
      console.log('Registro exitoso:', data);
      this.$router.push('/'); // Redirigimos a la pantalla principal
    },
    handleGoToLogin() {
      this.$router.push('/login');
    },
    handleError(message) {
      console.error('Error en registro:', message);
      this.$emit('error', message);
    }
  }
}
</script>

<style scoped>
</style>
