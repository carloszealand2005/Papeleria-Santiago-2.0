<template>
  <!-- variant: cart (replica el diseño anterior del resumen en /carrito) -->
  <div v-if="variant === 'cart'" class="space-y-4 mb-6">
    <div class="flex justify-between">
      <span class="text-gray-600">Subtotal</span>
      <span class="font-medium">${{ formatMoney(subtotal) }}</span>
    </div>
    <div class="flex justify-between">
      <span class="text-gray-600">Envío</span>
      <span class="font-medium">${{ formatMoney(shipping) }}</span>
    </div>
    <!-- Campo para Total Descuento - siempre visible -->
    <div class="flex justify-between text-green-600">
      <span>Total Descuento</span>
      <span>-${{ formatMoney(totalDiscount) }}</span>
    </div>
    <div class="flex justify-between">
      <span class="text-gray-600">Total IVA</span>
      <span class="font-medium">${{ formatMoney(totalIva) }}</span>
    </div>
    <div class="border-t border-gray-200 pt-4">
      <div class="flex justify-between text-lg font-bold">
        <span>Total</span>
        <span class="text-teal-600">${{ formatMoney(total) }}</span>
      </div>
    </div>
  </div>

  <!-- variant: checkout (diseño actual del resumen en /checkout) -->
  <div v-else class="space-y-2 border-t border-gray-200 pt-4">
    <div class="flex justify-between text-sm">
      <span class="text-gray-600">Subtotal:</span>
      <span class="text-gray-900">${{ formatMoney(subtotal) }}</span>
    </div>
    <div class="flex justify-between text-sm text-green-700">
      <span>Total Descuento:</span>
      <span>-${{ formatMoney(totalDiscount) }}</span>
    </div>
    <div class="flex justify-between text-sm">
      <span class="text-gray-600">Envío:</span>
      <span class="text-gray-900">${{ formatMoney(shipping) }}</span>
    </div>
    <div class="flex justify-between text-sm">
      <span class="text-gray-600">Total IVA:</span>
      <span class="text-gray-900">${{ formatMoney(totalIva) }}</span>
    </div>
    <div class="flex justify-between text-lg font-bold border-t border-gray-200 pt-2">
      <span class="text-gray-900">Total:</span>
      <span class="text-green-600">${{ formatMoney(total) }}</span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OrderTotalsSummary',
  props: {
    // Controla el diseño (no la lógica)
    variant: {
      type: String,
      default: 'checkout' // 'checkout' | 'cart'
    },
    subtotal: { type: [Number, String], required: true },
    shipping: { type: [Number, String], default: 0 },
    totalDiscount: { type: [Number, String], default: 0 },
    totalIva: { type: [Number, String], default: 0 },
    total: { type: [Number, String], required: true }
  },
  methods: {
    formatMoney(value) {
      const n = parseFloat(value || '0');
      return Number.isFinite(n) ? n.toFixed(2) : '0.00';
    }
  }
}
</script>

<style scoped>
</style>


