<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow">
    <div class="relative">
      <img
        :src="product.image"
        :alt="product.name"
        class="w-full h-48 object-cover object-top"
      >
      <div class="absolute top-4 left-4 bg-blue-500 text-white px-3 py-1 rounded-full text-sm font-bold">
        NUEVO
      </div>
    </div>
    <div class="p-6">
      <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ product.name }}</h3>
      <p class="text-gray-600 text-sm mb-4">{{ product.description }}</p>
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center space-x-2">
          <span class="text-2xl font-bold" style="color: #1F2937;">${{ product.price }}</span>
        </div>
        <span class="text-sm text-blue-600 font-semibold">Disponible</span>
      </div>
      <button 
        @click="addToCart"
        @mouseover="hoverButton = true"
        @mouseout="hoverButton = false"
        class="w-full text-white py-3 rounded-lg transition-colors !rounded-button whitespace-nowrap" 
        :style="hoverButton ? 'background-color: #111827;' : 'background-color: #1F2937;'"
      >
        <i class="fas fa-shopping-cart mr-2"></i>
        Agregar al Carrito
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FeaturedProduct',
  props: {
    product: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      hoverButton: false
    }
  },
  methods: {
    addToCart() {
      this.$emit('add-to-cart', this.product);
    }
  }
}
</script>

<style scoped>
</style>

