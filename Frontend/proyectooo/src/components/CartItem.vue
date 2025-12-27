<template>
  <div class="flex items-center space-x-4 p-4 border border-gray-200 rounded-lg">
    <!-- Product Image -->
    <div class="w-24 h-24 bg-gray-100 rounded-lg overflow-hidden flex-shrink-0">
      <img 
        :src="item.producto.imagen_url" 
        :alt="item.producto.nombre" 
        class="w-full h-full object-cover object-top"
      >
    </div>
    
    <!-- Product Details -->
    <div class="flex-1">
      <h3 class="font-semibold text-gray-900 mb-1">{{ item.producto.nombre }}</h3>
      <p class="text-sm text-gray-600 mb-2">{{ item.producto.descripcion }}</p>
      <p class="text-sm text-gray-500 line-through opacity-75">${{ parseFloat(item.precio_unitario).toFixed(2) }}</p>
      <p class="text-lg font-bold text-green-600">${{ parseFloat(item.precio_unitario).toFixed(2) }}</p>
    </div>
    
    <!-- Quantity Controls -->
    <div class="flex items-center space-x-3">
      <button 
        @click="decreaseQuantity" 
        class="w-8 h-8 bg-gray-100 hover:bg-gray-200 rounded-full flex items-center justify-center cursor-pointer !rounded-button whitespace-nowrap"
      >
        <i class="fas fa-minus text-xs text-gray-600"></i>
      </button>
      <span class="w-8 text-center font-medium">{{ item.cantidad }}</span>
      <button 
        @click="increaseQuantity" 
        class="w-8 h-8 bg-gray-100 hover:bg-gray-200 rounded-full flex items-center justify-center cursor-pointer !rounded-button whitespace-nowrap"
      >
        <i class="fas fa-plus text-xs text-gray-600"></i>
      </button>
    </div>
    
    <!-- Total Price -->
    <div class="text-right">
      <p class="font-bold text-lg text-gray-900">${{ itemTotal.toFixed(2) }}</p>
    </div>
    
    <!-- Remove Button -->
    <button 
      @click="removeItem" 
      class="text-red-500 hover:text-red-700 cursor-pointer !rounded-button whitespace-nowrap"
    >
      <i class="fas fa-trash text-lg"></i>
    </button>
  </div>
</template>

<script>
export default {
  name: 'CartItem',
  props: {
    item: {
      type: Object,
      required: true
    }
  },
  computed: {
    itemTotal() {
      return parseFloat(this.item.precio_unitario * this.item.cantidad);
    }
  },
  methods: {
    increaseQuantity() {
      this.$emit('increase-quantity', this.item.producto.SKU);
    },
    decreaseQuantity() {
      this.$emit('decrease-quantity', this.item.producto.SKU);
    },
    removeItem() {
      this.$emit('remove-item', this.item.producto.SKU);
    }
  }
}
</script>

<style scoped>
</style>
