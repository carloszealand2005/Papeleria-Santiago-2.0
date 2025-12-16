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
          <a href="#" @click.prevent="goToHome" class="text-gray-600 hover:text-indigo-600 px-3 py-2 text-sm font-medium cursor-pointer">Inicio</a>
          <a href="#" @click.prevent="goToProducts" class="text-gray-600 hover:text-indigo-600 px-3 py-2 text-sm font-medium cursor-pointer">Productos</a>
          <a href="#" @click.prevent="goToOffers" class="text-gray-600 hover:text-indigo-600 px-3 py-2 text-sm font-medium cursor-pointer">Ofertas</a>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'RegisterHeader',
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

