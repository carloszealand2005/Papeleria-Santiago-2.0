<template>
  <div class="mb-12">
    <h2 class="text-2xl font-bold text-gray-900 mb-6">Todos los Productos</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <ProductCard
        v-for="product in filteredProducts"
        :key="product.id"
        :product="product"
        @add-to-cart="handleAddToCart"
      />
    </div>
  </div>
</template>

<script>
import ProductCard from './ProductCard.vue';

export default {
  name: 'AllProducts',
  components: {
    ProductCard
  },
  props: {
    filteredProducts: {
      type: Array,
      required: true
    }
  },
  methods: {
    handleAddToCart(product) {
      this.$emit('add-to-cart', product);
    }
  }
}
</script>

<style scoped>
</style>

