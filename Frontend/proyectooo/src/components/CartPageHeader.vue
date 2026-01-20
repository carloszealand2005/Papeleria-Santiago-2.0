<template>
  <div class="mb-8">
    <div class="flex justify-between items-center mb-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900 mb-2">
          Mi Carrito
          <span v-if="isWholesale" class="text-base font-semibold text-gray-600 ml-2">(Cliente mayorista)</span>
        </h1>
        <p class="text-gray-600">{{ itemCount }} productos en tu carrito</p>
        <p v-if="isWholesale" class="text-sm text-slate-600">
          Tus cantidades se manejan por bultos.
        </p>
      </div>
      <button 
        class="text-teal-600 hover:text-teal-700 font-medium cursor-pointer !rounded-button whitespace-nowrap"
        @click="continueShopping"
      >
        <i class="fas fa-arrow-left mr-2"></i>
        Continuar Comprando
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CartPageHeader',
  props: {
    itemCount: {
      type: Number,
      required: true
    },
    isWholesale: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    continueShopping() {
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
</style>

