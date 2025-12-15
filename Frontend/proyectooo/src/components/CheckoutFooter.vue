<template>
  <footer class="bg-white border-t border-gray-200 py-6 mt-12">
    <div class="max-w-7xl mx-auto px-6">
      <div class="flex flex-col sm:flex-row items-center justify-between">
        <div class="flex items-center space-x-6 mb-4 sm:mb-0">
          <div class="flex items-center text-sm text-gray-600">
            <i class="fas fa-shield-alt text-green-600 mr-2"></i>
            <span>Pago Seguro SSL</span>
          </div>
          <div class="flex items-center space-x-3">
            <i class="fab fa-cc-visa text-2xl text-blue-600"></i>
            <i class="fab fa-cc-mastercard text-2xl text-red-600"></i>
            <i class="fab fa-cc-paypal text-2xl text-blue-500"></i>
          </div>
        </div>
        <div class="flex items-center space-x-4 text-sm text-gray-600">
          <a 
            href="#" 
            class="hover:text-blue-600 cursor-pointer"
            @click.prevent="goToHome"
          >
            Política de Privacidad
          </a>
          <span>|</span>
          <a 
            href="#" 
            class="hover:text-blue-600 cursor-pointer"
            @click.prevent="goToHome"
          >
            Términos de Servicio
          </a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'CheckoutFooter',
  methods: {
    goToHome() {
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
</style>

