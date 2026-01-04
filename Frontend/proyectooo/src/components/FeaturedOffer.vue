<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow">
    <div class="relative cursor-pointer" @click="viewProduct">
      <img
        :src="offer.image"
        :alt="offer.name"
        class="w-full h-48 object-cover object-top"
      >
      <div 
        class="absolute top-4 left-4 text-white px-3 py-1 rounded-full text-sm font-bold"
        :style="`background-color: ${offer.badgeColor || '#EF4444'};`"
      >
        {{ offer.discount }}% OFF
      </div>
      <div 
        v-if="offer.isHot"
        class="absolute top-4 right-4 bg-yellow-400 text-black px-2 py-1 rounded text-xs font-bold"
      >
        ¡HOT!
      </div>
    </div>
    <div class="p-6">
      <h3 class="text-lg font-semibold text-gray-900 mb-2 cursor-pointer hover:text-blue-600" @click="viewProduct">{{ offer.name }}</h3>
      <p class="text-gray-600 text-sm mb-4">{{ offer.description }}</p>
      <div class="flex items-center justify-between mb-4">
        <div class="flex items-center space-x-2">
          <template v-if="parseFloat(offer.discount) >= 1.00">
            <span class="text-lg text-gray-500 line-through opacity-75">${{ parseFloat(offer.originalPrice).toFixed(2) }}</span>
          </template>
          <template v-else>
            <span class="text-2xl font-bold" style="color: #1F2937;">${{ parseFloat(offer.originalPrice).toFixed(2) }}</span>
          </template>
        </div>
        <div class="flex items-center space-x-2">
          <template v-if="parseFloat(offer.discount) >= 1.00">
            <span class="text-2xl font-bold text-green-700">${{ parseFloat(offer.salePrice).toFixed(2) }}</span>
            <span class="text-sm font-medium text-green-700">(-{{ parseFloat(offer.discount).toFixed(0) }}%)</span>
          </template>
        </div>
      </div>
      <button 
        @click="addToCart"
        class="w-full text-white py-3 rounded-lg hover:bg-blue-700 transition-colors !rounded-button whitespace-nowrap" 
        style="background-color: #2563EB;"
      >
        <i class="fas fa-shopping-cart mr-2"></i>
        Agregar al Carrito
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'FeaturedOffer',
  props: {
    offer: {
      type: Object,
      required: true
    }
  },
  methods: {
    addToCart() {
      this.$emit('add-to-cart', this.offer);
    },
    viewProduct() {
      this.$emit('select-product', this.offer);
    }
  }
}
</script>

<style scoped>
</style>
