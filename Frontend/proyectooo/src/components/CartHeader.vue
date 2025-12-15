<template>
  <header class="bg-white border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <div class="flex items-center">
          <div class="flex items-center mr-8">
            <img 
              src="https://static.readdy.ai/image/a6354382ff0904464d2c460063bc60ba/1d728dd92f6f8bab5ded8741c3d0bbae.jpeg" 
              alt="Santiago Papelería" 
              class="h-10 w-auto cursor-pointer"
              @click="goToHome"
            >
          </div>
        </div>
        <nav class="flex items-center space-x-8">
          <a 
            href="#" 
            class="text-gray-700 hover:text-blue-600 text-sm font-medium cursor-pointer"
            @click.prevent="goToHome"
          >
            Inicio
          </a>
          <a 
            href="#" 
            class="text-gray-700 hover:text-blue-600 text-sm font-medium cursor-pointer"
            @click.prevent="goToProducts"
          >
            Productos
          </a>
          <a 
            href="#" 
            class="text-gray-700 hover:text-blue-600 text-sm font-medium cursor-pointer"
            @click.prevent="goToOffers"
          >
            Ofertas
          </a>
          <a 
            href="#" 
            class="text-gray-700 hover:text-blue-600 text-sm font-medium cursor-pointer"
          >
            Nosotros
          </a>
          <a 
            href="#" 
            class="text-gray-700 hover:text-blue-600 text-sm font-medium cursor-pointer"
          >
            Contacto
          </a>
        </nav>
        <div class="flex items-center space-x-4">
          <div class="relative flex items-center">
            <input
              type="text"
              v-model="searchQuery"
              placeholder="Buscar productos..."
              class="w-64 pl-4 pr-10 py-2 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              @keyup.enter="handleSearch"
            >
            <button 
              class="absolute right-2 text-white bg-blue-600 hover:bg-blue-700 px-2 py-1 rounded cursor-pointer !rounded-button whitespace-nowrap"
              @click="handleSearch"
            >
              <i class="fas fa-search text-sm"></i>
            </button>
          </div>
          <div class="relative" @click="goToCart">
            <i class="fas fa-shopping-cart text-xl text-blue-600 cursor-pointer"></i>
            <span 
              v-if="cartCount > 0"
              class="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center"
            >
              {{ cartCount }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  name: 'CartHeader',
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
        this.$emit('search', this.searchQuery);
      }
    },
    goToHome() {
      this.$router.push('/');
    },
    goToProducts() {
      this.$router.push('/productos');
    },
    goToOffers() {
      this.$router.push('/ofertas');
    },
    goToCart() {
      this.$router.push('/carrito');
    }
  }
}
</script>

<style scoped>
</style>

