<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
    <h2 class="text-xl font-semibold text-gray-900 mb-6">Resumen del Pedido</h2>
    <div class="space-y-4 mb-6">
      <div 
        v-for="(item, index) in orderItems" 
        :key="index"
        class="flex items-center space-x-4 pb-4 border-b border-gray-100"
      >
        <img
          :src="item.image"
          :alt="item.name"
          class="w-16 h-16 object-cover rounded-lg"
        >
        <div class="flex-1">
          <h3 class="font-medium text-gray-900">{{ item.name }}</h3>
          <p class="text-sm text-gray-600">Cantidad: {{ item.quantity }}</p>
        </div>
        <span class="font-semibold text-gray-900">${{ formatPrice(item.price) }}</span>
      </div>
    </div>
    <div class="space-y-2 border-t border-gray-200 pt-4">
      <div class="flex justify-between text-sm">
        <span class="text-gray-600">Subtotal:</span>
        <span class="text-gray-900">${{ formatPrice(totals.subtotal) }}</span>
      </div>
      <div class="flex justify-between text-sm">
        <span class="text-gray-600">Envío:</span>
        <span class="text-gray-900">{{ shippingText }}</span>
      </div>
      <div class="flex justify-between text-sm">
        <span class="text-gray-600">IVA (16%):</span>
        <span class="text-gray-900">${{ formatPrice(totals.tax) }}</span>
      </div>
      <div class="flex justify-between text-lg font-bold border-t border-gray-200 pt-2">
        <span class="text-gray-900">Total:</span>
        <span class="text-green-600">${{ formatPrice(totals.total) }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CheckoutOrderSummary',
  props: {
    orderItems: {
      type: Array,
      required: true
    },
    totals: {
      type: Object,
      required: true
    },
    shippingCost: {
      type: Number,
      default: 0
    }
  },
  computed: {
    shippingText() {
      return this.shippingCost === 0 ? 'Gratis' : `$${this.formatPrice(this.shippingCost)}`;
    }
  },
  methods: {
    formatPrice(price) {
      return price.toFixed(2);
    }
  }
}
</script>

<style scoped>
</style>

