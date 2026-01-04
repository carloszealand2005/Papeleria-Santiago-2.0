<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
    <h2 class="text-xl font-semibold text-gray-900 mb-6">Resumen del Pedido</h2>

    <!-- Items del carrito: mismos datos/lógica que en /carrito, sin IVA por línea -->
    <OrderItemsSummary :items="orderItems" variant="checkout" />

    <!-- Totales: mismos campos que en /carrito -->
    <OrderTotalsSummary
      :subtotal="totals.subtotal"
      :shipping="shippingCost"
      :totalDiscount="totals.totalDiscount"
      :totalIva="totals.totalIva"
      :total="totals.total"
    />
  </div>
</template>

<script>
import OrderItemsSummary from './OrderItemsSummary.vue';
import OrderTotalsSummary from './OrderTotalsSummary.vue';

export default {
  name: 'CheckoutOrderSummary',
  components: {
    OrderItemsSummary,
    OrderTotalsSummary
  },
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
  }
}
</script>

<style scoped>
</style>

