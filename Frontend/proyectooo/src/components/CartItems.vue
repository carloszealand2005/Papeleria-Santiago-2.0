<template>
  <div class="lg:col-span-2">
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h2 class="text-xl font-semibold text-gray-900 mb-6">Productos</h2>
      <div class="space-y-6">
        <CartItem
          v-for="item in cartItems"
          :key="item.id"
          :item="item"
          @increase-quantity="$emit('increase-quantity', $event)"
          @decrease-quantity="$emit('decrease-quantity', $event)"
          @remove-item="$emit('remove-item', $event)"
        />
      </div>
    </div>
  </div>
</template>

<script>
import CartItem from './CartItem.vue';

export default {
  name: 'CartItems',
  components: {
    CartItem
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

