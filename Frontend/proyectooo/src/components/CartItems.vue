<template>
  <div class="lg:col-span-2">
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h2 class="text-xl font-semibold text-gray-900 mb-6">Productos</h2>
       <div v-if="cartItems && cartItems.length">
        <OrderItemsSummary
          :items="cartItems"
          :editable="true"
          variant="cart"
          @increase-quantity="$emit('increase-quantity', $event)"
          @decrease-quantity="$emit('decrease-quantity', $event)"
          @remove-item="$emit('remove-item', $event)"
        />
      </div>

      <div v-else class="py-10 text-center text-gray-500">
        Los productos que añadas al carrito aparecerán aquí
      </div>
    </div>
  </div>
</template>

<script>
import OrderItemsSummary from './OrderItemsSummary.vue';

export default {
  name: 'CartItems',
  components: {
    OrderItemsSummary
  },
  props: {
    cartItems: {
      type: Array,
      required: true
    }
  }
}
</script>

<style scoped>
</style>

