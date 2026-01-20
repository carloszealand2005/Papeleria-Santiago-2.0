<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-lg transition-shadow">
    <div class="relative cursor-pointer" @click="viewProduct">
      <img
        :src="product.image"
        :alt="product.name"
        class="w-full h-40 object-cover object-top"
      >
      <div class="absolute top-2 left-2 bg-red-500 text-white px-2 py-1 rounded text-xs font-bold">
        {{ product.discount }}% OFF
      </div>
    </div>
    <div class="p-4">
      <h3 class="font-semibold text-gray-900 mb-2 text-sm cursor-pointer hover:text-blue-600" @click="viewProduct">{{ product.name }}</h3>
      <div class="flex items-center justify-between mb-3">
        <div class="flex flex-col">
          <span class="text-lg font-bold" style="color: #2563EB;">${{ product.salePrice }}</span>
          <span class="text-sm text-gray-600 line-through">${{ product.originalPrice }}</span>
          <span
            v-if="product && product.bulto_minimo_mayorista !== undefined && product.bulto_minimo_mayorista !== null && String(product.bulto_minimo_mayorista) !== ''"
            class="text-xs text-slate-700 mt-1"
          >
            Bulto mínimo: {{ product.bulto_minimo_mayorista }}
          </span>
        </div>
      </div>
      <button 
        @click="addToCart"
        class="w-full text-white py-2 rounded-lg hover:bg-blue-700 transition-colors !rounded-button whitespace-nowrap text-sm" 
        style="background-color: #2563EB;"
      >
        Agregar
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OfferCard',
  props: {
    product: {
      type: Object,
      required: true
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

