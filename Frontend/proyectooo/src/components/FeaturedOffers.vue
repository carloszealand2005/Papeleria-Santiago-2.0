<template>
  <div class="mb-12">
    <h2 class="text-2xl font-bold text-gray-900 mb-6">Ofertas Destacadas</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <FeaturedOffer
        v-for="offer in featuredOffers"
        :key="offer.id"
        :offer="offer"
        @add-to-cart="handleAddToCart"
        @select-product="handleSelectProduct"
      />
    </div>
  </div>
</template>

<script>
import FeaturedOffer from './FeaturedOffer.vue';

export default {
  name: 'FeaturedOffers',
  components: {
    FeaturedOffer
  },
  props: {
    featuredOffers: {
      type: Array,
      required: true
    }
  },
  methods: {
    handleAddToCart(offer) {
      this.$emit('add-to-cart', offer);
    },
    handleSelectProduct(offer) {
      this.$emit('select-product', offer);
    }
  }
}
</script>

<style scoped>
</style>

