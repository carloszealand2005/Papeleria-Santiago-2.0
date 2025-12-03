<template>
  <header class="bg-white shadow-sm border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-6 py-4">
      <div class="flex justify-between items-center">
        <!-- Logo Section -->
        <div class="flex items-center">
          <img 
            src="https://static.readdy.ai/image/a6354382ff0904464d2c460063bc60ba/259e982fdf90414f835fa6591b3078c6.jpeg" 
            alt="Santiago Papelería" 
            class="h-12 w-auto"
          >
        </div>
        
        <!-- Navigation -->
        <nav class="flex items-center space-x-8">
          <a href="#" class="text-gray-700 hover:text-blue-600 font-medium text-sm transition-colors">Inicio</a>
          <a href="#" class="text-gray-700 hover:text-blue-600 font-medium text-sm transition-colors">Productos</a>
          <a href="#" style="color: #2563EB;" class="font-medium text-sm">Ofertas</a>
          <a href="#" class="text-gray-700 hover:text-blue-600 font-medium text-sm transition-colors">Nosotros</a>
          <a href="#" class="text-gray-700 hover:text-blue-600 font-medium text-sm transition-colors">Contacto</a>
        </nav>
        
        <!-- Search and Cart -->
        <div class="flex items-center space-x-4">
          <div class="relative">
            <input
              type="text"
              placeholder="Buscar productos..."
              v-model="searchQuery"
              class="pl-10 pr-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:border-blue-600 w-64 focus:outline-none"
              style="--tw-ring-color: #2563EB;"
              @keyup.enter="handleSearch"
            >
            <i class="fas fa-search absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 text-sm"></i>
          </div>
          <button 
            class="relative p-2 text-white rounded-lg hover:bg-blue-700 transition-colors !rounded-button" 
            style="background-color: #2563EB;"
            @click="goToCart"
          >
            <i class="fas fa-shopping-cart"></i>
            <span 
              v-if="cartCount > 0"
              class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center"
            >
              {{ cartCount }}
            </span>
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'OffersHeader',
  props: {
    cartCount: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      searchQuery: ''
    }
  },
  methods: {
    handleSearch() {
      if (this.searchQuery.trim()) {
        console.log('Buscando:', this.searchQuery);
        this.$emit('search', this.searchQuery);
      }
    },
    goToCart() {
      this.$emit('go-to-cart');
    }
  }
}
</script>

<style scoped>
</style>

