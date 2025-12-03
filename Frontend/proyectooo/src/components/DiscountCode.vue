<template>
  <div class="mt-8 p-4 bg-gray-50 rounded-lg">
    <h3 class="font-semibold text-gray-900 mb-4">Código de Descuento</h3>
    <div class="flex space-x-3">
      <input
        v-model="discountCode"
        type="text"
        placeholder="Ingresa tu código promocional"
        class="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-sm"
        @keyup.enter="applyDiscount"
      >
      <button 
        @click="applyDiscount" 
        class="px-6 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 font-medium cursor-pointer !rounded-button whitespace-nowrap"
      >
        Aplicar
      </button>
    </div>
    <div v-if="appliedDiscount > 0" class="mt-3 text-green-600 text-sm">
      <i class="fas fa-check-circle mr-2"></i>
      Descuento aplicado: {{ appliedDiscount }}% OFF
    </div>
  </div>
</template>

<script>
export default {
  name: 'DiscountCode',
  props: {
    appliedDiscount: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      discountCode: ''
    }
  },
  methods: {
    applyDiscount() {
      if (this.discountCode.trim()) {
        this.$emit('apply-discount', this.discountCode);
        this.discountCode = '';
      }
    }
  }
}
</script>

<style scoped>
</style>

