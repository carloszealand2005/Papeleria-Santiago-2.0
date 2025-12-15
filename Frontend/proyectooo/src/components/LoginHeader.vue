<template>
  <header class="bg-white shadow-sm border-b">
    <div class="max-w-7xl mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <div class="flex items-center">
          <img 
            src="https://static.readdy.ai/image/a6354382ff0904464d2c460063bc60ba/ea51eb4ba2a53ef142a962fbf9bc4d85.jpeg" 
            alt="Santiago Papelería" 
            class="h-10 w-auto mr-3"
          >
        </div>
        
        <!-- Navigation -->
        <nav class="hidden md:flex space-x-8">
          <a 
            href="#" 
            class="text-gray-600 hover:text-blue-600 transition-colors cursor-pointer"
            @click.prevent="goToHome"
          >
            Inicio
          </a>
          <a 
            href="#" 
            class="text-gray-600 hover:text-blue-600 transition-colors cursor-pointer"
            @click.prevent="goToProducts"
          >
            Productos
          </a>
          <a 
            href="#" 
            class="text-gray-600 hover:text-blue-600 transition-colors cursor-pointer"
            @click.prevent="goToOffers"
          >
            Ofertas
          </a>
        </nav>
        
        <!-- Actions -->
        <div class="flex items-center space-x-4">
          <button 
            class="text-gray-600 hover:text-blue-600 transition-colors cursor-pointer"
            @click="$emit('show-account-info')"
          >
            ¿Ya tienes cuenta?
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'LoginHeader',
  methods: {
    goToHome() {
      this.$router.push('/');
    },
    goToProducts() {
      this.$router.push('/productos');
    },
    goToOffers() {
      this.$router.push('/ofertas');
    }
  }
}
</script>

<style scoped>
</style>

