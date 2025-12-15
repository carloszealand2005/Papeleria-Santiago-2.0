<template>
  <header class="bg-white shadow-sm border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-6 py-4">
      <div class="flex justify-between items-center">
        <div class="flex items-center">
          <img
            src="https://static.readdy.ai/image/a6354382ff0904464d2c460063bc60ba/d66c997e03357d7855f38b760e34012f.jpeg"
            alt="Santiago Papelería"
            class="h-12 w-auto cursor-pointer"
            @click="goToHome"
          >
        </div>
        <div class="flex items-center space-x-4">
          <div class="flex items-center">
            <div class="flex items-center space-x-2">
              <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                <i class="fas fa-check text-white text-sm"></i>
              </div>
              <span class="text-sm text-gray-600">Carrito</span>
              <i class="fas fa-chevron-right text-gray-400 text-xs"></i>
              <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                <i class="fas fa-check text-white text-sm"></i>
              </div>
              <span class="text-sm text-gray-600">Envío</span>
              <i class="fas fa-chevron-right text-gray-400 text-xs"></i>
              <div class="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center" style="background-color: #2563EB;">
                <i class="fas fa-credit-card text-white text-sm"></i>
              </div>
              <span class="text-sm font-semibold" style="color: #2563EB;">Pago</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'CheckoutHeader',
  methods: {
    goToHome() {
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
</style>

