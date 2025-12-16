<template>
  <nav class="bg-white shadow-lg">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-20">
        <!-- Logo -->
        <div class="flex items-center">
          <img 
            src="https://static.readdy.ai/image/a6354382ff0904464d2c460063bc60ba/a517923db6583f4c953e5c11089dec01.jpeg" 
            alt="Santiago Papelería" 
            class="h-12 w-auto"
          >
        </div>

        <!-- Navigation Menu -->
        <div class="hidden md:flex items-center space-x-8">
          <a href="#" @click.prevent="goToHome" class="text-slate-700 hover:text-blue-600 font-medium transition-colors">Inicio</a>
          <a href="#" @click.prevent="goToProducts" class="text-slate-700 hover:text-blue-600 font-medium transition-colors">Productos</a>
          <a href="#" @click.prevent="goToOffers" class="text-slate-700 hover:text-blue-600 font-medium transition-colors">Ofertas</a>
          <a href="#" class="text-slate-700 hover:text-blue-600 font-medium transition-colors">Nosotros</a>
          <a href="#" class="text-slate-700 hover:text-blue-600 font-medium transition-colors">Contacto</a>
        </div>

        <!-- Search and Cart -->
        <div class="flex items-center space-x-4">
          <div class="relative">
            <input
              type="text"
              placeholder="Buscar..."
              v-model="searchQuery"
              class="w-64 pl-10 pr-4 py-2 border border-gray-300 !rounded-button focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
              @keyup.enter="handleSearch"
            >
            <i class="fas fa-search absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 text-sm"></i>
          </div>
          <button 
            class="text-slate-700 hover:text-blue-600 font-medium transition-colors px-4 py-2"
            @click="goToLogin"
          >
            <i class="fas fa-user mr-2"></i>Iniciar Sesión
          </button>
          <button 
            class="relative bg-blue-600 hover:bg-blue-700 text-white p-2 !rounded-button transition-colors"
            @click="goToCart"
          >
            <i class="fas fa-shopping-cart text-lg"></i>
            <span 
              v-if="cartCount > 0"
              class="absolute -top-2 -right-2 bg-yellow-400 text-slate-900 text-xs rounded-full w-5 h-5 flex items-center justify-center font-bold"
            >
              {{ cartCount }}
            </span>
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'HeaderComponent',
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
        // Emitir evento o navegar a resultados de búsqueda
        this.$emit('search', this.searchQuery);
      }
    },
    goToCart() {
      this.$router.push('/carrito');
    },
    goToLogin() {
      this.$router.push('/login');
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