<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-gray-100">
    <LoginHeader 
      @navigate="handleNavigate"
      @show-account-info="handleShowAccountInfo"
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
    
    <LoginForm 
      @login-success="handleLoginSuccess"
      @redirect="handleRedirect"
      @go-to-register="handleGoToRegister"
      @forgot-password="handleForgotPassword"
      @user-type-changed="handleUserTypeChanged"
      @error="handleError"
      @success="handleSuccess"
    />
    
    <LoginFooter />
  </div>
</template>

<script>
import LoginHeader from './LoginHeader.vue';
import LoginForm from './LoginForm.vue';
import LoginFooter from './LoginFooter.vue';

export default {
  name: 'LoginPage',
  components: {
    LoginHeader,
    LoginForm,
    LoginFooter
  },
  methods: {
    goToHome() {
      this.$emit('go-to-home');
    },
    handleNavigate(route) {
      console.log('Navegar a:', route);
      // Si navega a home, emitir evento
      if (route === 'home') {
        this.goToHome();
      }
      // Implementar navegación con Vue Router
      // this.$router.push(`/${route}`);
    },
    handleShowAccountInfo() {
      console.log('Mostrar información de cuenta');
      // Implementar lógica para mostrar información de cuenta
    },
    handleLoginSuccess(data) {
      console.log('Login exitoso:', data);
      // Aquí puedes guardar datos en el store o localStorage
      // y redirigir al usuario
    },
    handleRedirect(destination) {
      console.log('Redirigir a:', destination);
      // Implementar redirección según el destino
      // this.$router.push(`/${destination}`);
    },
    handleGoToRegister(type) {
      console.log('Ir a registro:', type);
      // Implementar navegación a página de registro
      // this.$router.push(`/register?type=${type}`);
    },
    handleForgotPassword() {
      console.log('Olvidé mi contraseña');
      // Implementar navegación a página de recuperación de contraseña
      // this.$router.push('/forgot-password');
    },
    handleUserTypeChanged(type) {
      console.log('Tipo de usuario cambiado:', type);
    },
    handleError(message) {
      console.error('Error en login:', message);
      // Aquí puedes implementar un sistema de notificaciones global
    },
    handleSuccess(message) {
      console.log('Éxito en login:', message);
      // Aquí puedes implementar un sistema de notificaciones global
    }
  }
}
</script>

<style scoped>
</style>

