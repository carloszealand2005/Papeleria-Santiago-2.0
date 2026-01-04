<template>
  <div class="mb-12" v-if="featuredProducts.length > 0">
    <h2 class="text-2xl font-bold text-gray-900 mb-6">{{ title }}</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <FeaturedProduct
        v-for="product in featuredProducts"
        :key="product.id"
        :product="product"
        @add-to-cart="handleAddToCart"
        @select-product="handleSelectProduct"
        :badgeText="badgeText"
        :badgeColor="badgeColor"
      />
    </div>
  </div>
</template>

<script>
import FeaturedProduct from './FeaturedProduct.vue';

export default {
  name: 'FeaturedProducts',
  components: {
    FeaturedProduct
  },
  props: {
    featuredProducts: {
      type: Array,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    badgeText: {
      type: String,
      default: ''
    },
    badgeColor: {
      type: String,
      default: '#2563EB'
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
