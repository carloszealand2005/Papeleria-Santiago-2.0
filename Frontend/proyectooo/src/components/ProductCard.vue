<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow">
    <div class="relative">
      <img
        :src="product.image"
        :alt="product.name"
        class="w-full h-40 object-cover object-top"
      >
      <div class="absolute top-2 left-2 bg-blue-500 text-white px-2 py-1 rounded text-xs font-bold">
        NUEVO
      </div>
    </div>
    <div class="p-4">
      <h3 class="font-semibold text-gray-900 mb-2 text-sm">{{ product.name }}</h3>
      <div class="flex items-center justify-between mb-3">
        <div class="flex flex-col">
          <span class="text-lg font-bold" style="color: #1F2937;">${{ product.originalPrice }}</span>
          <span class="text-xs text-blue-600">En stock</span>
        </div>
      </div>
      <button 
        @click="addToCart"
        @mouseover="hoverButton = true"
        @mouseout="hoverButton = false"
        class="w-full text-white py-2 rounded-lg transition-colors !rounded-button whitespace-nowrap text-sm" 
        :style="hoverButton ? 'background-color: #111827;' : 'background-color: #1F2937;'"
      >
        Agregar
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductCard',
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

