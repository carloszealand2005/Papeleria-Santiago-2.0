<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow">
    <div class="relative cursor-pointer" @click="viewProduct">
      <img
        :src="product.image"
        :alt="product.name"
        class="w-full h-48 object-cover object-top"
      >
      <div 
        v-if="badgeText"
        class="absolute top-4 left-4 text-white px-3 py-1 rounded-full text-sm font-bold"
        :style="`background-color: ${badgeColor};`"
      >
        {{ badgeText }}
      </div>
    </div>
    <div class="p-6">
      <h3 class="text-lg font-semibold text-gray-900 mb-1 cursor-pointer hover:text-blue-600" @click="viewProduct">{{ product.name }}</h3>
      <p v-if="product.brand" class="text-sm text-gray-500 mb-2">{{ product.brand }}</p>
      <p class="text-gray-600 text-sm mb-4">{{ product.description }}</p>
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center space-x-2">
          <template v-if="parseFloat(product.discount) >= 1.00">
            <span class="text-lg text-gray-500 line-through opacity-75">${{ parseFloat(product.originalPrice).toFixed(2) }}</span>
            <span class="text-2xl font-bold text-green-700">${{ parseFloat(product.salePrice).toFixed(2) }}</span>
            <span class="text-sm font-medium text-green-700">(-{{ parseFloat(product.discount).toFixed(0) }}%)</span>
          </template>
          <template v-else>
            <span class="text-2xl font-bold" style="color: #1F2937;">${{ parseFloat(product.originalPrice).toFixed(2) }}</span>
          </template>
        </div>
        <span class="text-sm text-blue-600 font-semibold">Disponible</span>
      </div>
      <button 
        @click="addToCart"
        @mouseover="hoverButton = true"
        @mouseout="hoverButton = false"
        class="w-full text-white py-3 rounded-lg transition-colors !rounded-button whitespace-nowrap" 
        :style="hoverButton ? 'background-color: #111827;' : 'background-color: #1F2937;'
"
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
    },
    badgeText: {
      type: String,
      default: ''
    },
    badgeColor: {
      type: String,
      default: '#2563EB' // Un azul por defecto
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
    },
    viewProduct() {
      this.$emit('select-product', this.product);
    }
  }
}
</script>

<style scoped>
</style>
