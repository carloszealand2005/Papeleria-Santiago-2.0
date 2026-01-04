<template>
  <nav class="bg-white shadow-lg">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-20">
        <!-- Logo -->
        <div class="flex items-center">
          <router-link to="/" class="flex items-center">
            <img 
              src="@/assets/papeleria_santiago_logo.png" 
              alt="Santiago Papelería" 
              class="h-12 w-auto"
            >
          </router-link>
        </div>

        <!-- Navigation Menu -->
        <div class="hidden md:flex items-center space-x-8">
          <a href="#" @click.prevent="goToHome" class="text-slate-700 hover:text-blue-600 font-medium transition-colors">Inicio</a>
          <a href="#" @click.prevent="goToProducts" class="text-slate-700 hover:text-blue-600 font-medium transition-colors">Productos</a>
          <a href="#" @click.prevent="goToOffers" class="text-slate-700 hover:text-blue-600 font-medium transition-colors">Ofertas</a>
          <a href="#" @click.prevent="goToFavorites" class="text-slate-700 hover:text-blue-600 font-medium transition-colors">Favoritos</a>
          <a href="#" @click.prevent="goToContact" class="text-slate-700 hover:text-blue-600 font-medium transition-colors">Contacto</a>
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
            <i class="fas fa-user mr-2"></i>{{ isAuthenticated ? 'Mi cuenta' : 'Iniciar Sesión' }}
          </button>
          <button 
            class="relative p-2 transition-colors"
            @click="goToCart"
          >
            <img src="@/assets/img_cart.png" alt="Carrito" class="h-6 w-6">
            <span 
              v-if="cartItemCount > 0"
              class="absolute -top-2 -right-2 bg-yellow-400 text-slate-900 text-xs rounded-full w-5 h-5 flex items-center justify-center font-bold"
            >
              {{ cartItemCount }}
            </span>
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapGetters } from 'vuex'; // Importar mapGetters

export default {
  name: 'GlobalHeader',
  components: {},
  data() {
    return {
      searchQuery: '',
    }
  },
  computed: {
    ...mapGetters(['cartItemCount', 'isAuthenticated']),
  },
  inject: ['showAuthModal'],
  methods: {
    handleSearch() {
      if (this.searchQuery.trim()) {
        this.$router.push({ path: '/productos', query: { search: this.searchQuery } });
      }
    },
    goToCart() {
      if (!this.isAuthenticated) {
        this.showAuthModal(); // Llamar a la función inyectada para mostrar el modal
        return;
      }
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
    },
    goToFavorites() {
      this.$router.push('/favoritos');
    },
    goToContact() {
      // Asume que también hay una página de contacto o se dejará como un placeholder
    }
  }
}
</script>

<style scoped>
</style>
