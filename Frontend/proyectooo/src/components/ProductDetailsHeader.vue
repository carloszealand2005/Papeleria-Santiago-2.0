<template>
  <nav class="bg-white shadow-sm border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <div class="flex items-center">
          <div class="flex-shrink-0 flex items-center">
            <img
              src="https://static.readdy.ai/image/a6354382ff0904464d2c460063bc60ba/4b239160cf881d842d720a25a307d075.jpeg"
              alt="Santiago Papelería"
              class="h-8 w-auto cursor-pointer"
              @click="goToHome"
            />
          </div>
        </div>
        <div class="flex items-center space-x-4">
          <a href="#" class="text-gray-600 hover:text-indigo-600 px-3 py-2 text-sm font-medium cursor-pointer" @click.prevent="goToHome">Inicio</a>
          <a href="#" class="text-gray-600 hover:text-indigo-600 px-3 py-2 text-sm font-medium cursor-pointer" @click.prevent="goToProducts">Productos</a>
          <a href="#" class="text-gray-600 hover:text-indigo-600 px-3 py-2 text-sm font-medium cursor-pointer" @click.prevent="goToOffers">Ofertas</a>
          <a href="#" class="text-gray-600 hover:text-indigo-600 px-3 py-2 text-sm font-medium cursor-pointer">Nosotros</a>
          <a href="#" class="text-gray-600 hover:text-indigo-600 px-3 py-2 text-sm font-medium cursor-pointer">Contacto</a>
          <div class="flex items-center ml-6">
            <div class="relative">
              <input
                type="text"
                placeholder="Buscar..."
                v-model="searchQuery"
                @keyup.enter="handleSearch"
                class="pl-8 pr-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              />
              <i class="fas fa-search absolute left-2.5 top-1/2 transform -translate-y-1/2 text-gray-400 text-sm"></i>
            </div>
            <button class="ml-3 bg-indigo-600 text-white p-2 rounded-lg hover:bg-indigo-700 cursor-pointer" @click="handleSearch">
              <i class="fas fa-search"></i>
            </button>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'ProductDetailsHeader',
  data() {
    return {
      searchQuery: ''
    };
  },
  methods: {
    goToHome() {
      this.$router.push('/');
    },
    goToProducts() {
      this.$router.push('/productos');
    },
    goToOffers() {
      this.$router.push('/ofertas');
    },
    handleSearch() {
      if (this.searchQuery.trim()) {
        this.$emit('search', this.searchQuery);
      }
    }
  }
}
</script>

<style scoped>
</style>

