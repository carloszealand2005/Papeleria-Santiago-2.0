<template>
  <div class="mb-12">
    <h2 class="text-2xl font-bold text-gray-900 mb-6">Todas las Ofertas</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <OfferCard
        v-for="product in filteredProducts"
        :key="product.id"
        :product="product"
        @add-to-cart="handleAddToCart"
        @select-product="handleSelectProduct"
      />
    </div>
  </div>
</template>

<script>
import OfferCard from './OfferCard.vue';

export default {
  name: 'AllOffers',
  components: {
    OfferCard
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
    },
    handleSelectProduct(product) {
      this.$emit('select-product', product);
    }
  }
}
</script>

<style scoped>
</style>

