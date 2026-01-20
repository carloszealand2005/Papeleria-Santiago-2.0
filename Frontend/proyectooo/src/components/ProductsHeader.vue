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
          <a href="#" @click.prevent="goToHome" class="text-gray-700 hover:text-blue-600 font-medium text-sm transition-colors cursor-pointer">Inicio</a>
          <a href="#" style="color: #1F2937;" class="font-medium text-sm cursor-pointer">Productos</a>
          <a href="#" @click.prevent="goToOffers" class="text-gray-700 hover:text-blue-600 font-medium text-sm transition-colors cursor-pointer">Ofertas</a>
          <a href="#" class="text-gray-700 hover:text-blue-600 font-medium text-sm transition-colors cursor-pointer">Nosotros</a>
          <a href="#" class="text-gray-700 hover:text-blue-600 font-medium text-sm transition-colors cursor-pointer">Contacto</a>
        </nav>
        
        <!-- Search and Cart -->
        <div class="flex items-center space-x-4">
          <div class="relative">
            <label for="products-header-search" class="sr-only">Buscar productos</label>
            <input
              id="products-header-search"
              type="text"
              placeholder="Buscar productos..."
              v-model="searchQuery"
              class="pl-10 pr-4 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:border-blue-600 w-64 focus:outline-none"
              style="--tw-ring-color: #1F2937;"
              @keyup.enter="handleSearch"
            >
            <i class="fas fa-search absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 text-sm" aria-hidden="true"></i>
          </div>
          <button 
            type="button"
            class="relative p-2 text-white rounded-lg transition-colors !rounded-button" 
            style="background-color: #1F2937;"
            @mouseover="hoverCart = true"
            @mouseout="hoverCart = false"
            :style="hoverCart ? 'background-color: #111827;' : 'background-color: #1F2937;'"
            @click="goToCart"
            :aria-label="cartButtonAriaLabel"
            :title="cartButtonAriaLabel"
          >
            <i class="fas fa-shopping-cart" aria-hidden="true"></i>
            <span class="sr-only">{{ cartButtonAriaLabel }}</span>
            <span 
              v-if="cartItemCount > 0"
              class="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center"
              aria-hidden="true"
            >
              {{ cartItemCount }}
            </span>
          </button>
        </div>
      </div>
    </div>
  </header>
</template>

<script>
import { mapGetters } from 'vuex'; // Importar mapGetters

export default {
  name: 'ProductsHeader',
  // Eliminamos la prop cartItemCount
  // props: {
  //   cartItemCount: {
  //     type: Number,
  //     default: 0
  //   }
  // },
  data() {
    return {
      searchQuery: '',
      hoverCart: false
    }
  },
  computed: {
    ...mapGetters(['cartItemCount']), // Mapeamos cartItemCount directamente desde Vuex
    cartButtonAriaLabel() {
      if (this.cartItemCount > 0) return `Ir al carrito (${this.cartItemCount} producto${this.cartItemCount === 1 ? '' : 's'})`;
      return 'Ir al carrito';
    },
  },
  methods: {
    handleSearch() {
      if (this.searchQuery.trim()) {
        this.$emit('search', this.searchQuery);
      }
    },
    goToCart() {
      this.$router.push('/carrito');
    },
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
