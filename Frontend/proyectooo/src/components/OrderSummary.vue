<template>
  <div class="lg:col-span-1">
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 sticky top-8">
      <h2 class="text-xl font-semibold text-gray-900 mb-6">Resumen de Compra</h2>
      
      <div class="space-y-4 mb-6">
        <div class="flex justify-between">
          <span class="text-gray-600">Subtotal</span>
          <span class="font-medium">${{ subtotal.toFixed(2) }}</span>
        </div>
        <div class="flex justify-between">
          <span class="text-gray-600">Envío</span>
          <span class="font-medium">${{ shipping.toFixed(2) }}</span>
        </div>
        <!-- Campo para Total Descuento - siempre visible -->
        <div class="flex justify-between text-green-600">
          <span>Total Descuento</span>
          <span>-${{ totalDiscount.toFixed(2) }}</span>
        </div>
        <div class="flex justify-between">
          <span class="text-gray-600">Total IVA</span>
          <span class="font-medium">${{ totalIva.toFixed(2) }}</span>
        </div>
        <div class="border-t border-gray-200 pt-4">
          <div class="flex justify-between text-lg font-bold">
            <span>Total</span>
            <span class="text-teal-600">${{ total.toFixed(2) }}</span>
          </div>
        </div>
      </div>
      
      <!-- Shipping Options -->
      <div class="mb-6">
        <h3 class="font-medium text-gray-900 mb-3">Opciones de Envío</h3>
        <div class="space-y-2">
          <label class="flex items-center">
            <input 
              type="radio" 
              name="shipping" 
              value="standard" 
              :checked="localShipping === 'standard'"
              class="mr-3"
              @change="updateShipping('standard')"
            >
            <span class="text-sm">Envío Estándar (5-7 días) - Gratis</span>
          </label>
          <label class="flex items-center">
            <input 
              type="radio" 
              name="shipping" 
              value="express" 
              :checked="localShipping === 'express'"
              class="mr-3"
              @change="updateShipping('express')"
            >
            <span class="text-sm">Envío Express (2-3 días) - $15.00</span>
          </label>
        </div>
      </div>
      
      <!-- Action Buttons -->
      <div class="space-y-3">
        <button 
          @click="$emit('update-cart')" 
          class="w-full py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 font-medium cursor-pointer !rounded-button whitespace-nowrap"
        >
          Actualizar Carrito
        </button>
        <button 
          @click="$emit('proceed-checkout')" 
          class="w-full py-3 bg-teal-600 text-white rounded-lg hover:bg-teal-700 font-medium cursor-pointer !rounded-button whitespace-nowrap"
        >
          <i class="fas fa-lock mr-2"></i>
          Proceder al Pago
        </button>
      </div>
      
      <!-- Security Info -->
      <div class="mt-6 pt-6 border-t border-gray-200">
        <div class="text-center">
          <p class="text-sm text-gray-600 mb-3">Pago 100% Seguro</p>
          <div class="flex justify-center space-x-4 text-2xl text-gray-400">
            <i class="fab fa-cc-visa cursor-pointer"></i>
            <i class="fab fa-cc-mastercard cursor-pointer"></i>
            <i class="fab fa-paypal cursor-pointer"></i>
            <i class="fas fa-shield-alt cursor-pointer"></i>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OrderSummary',
  props: {
    subtotal: {
      type: Number,
      required: true
    },
    shipping: {
      type: Number,
      required: true
    },
    totalIva: { // Nuevo prop para Total IVA
      type: Number,
      required: true
    },
    totalDiscount: { // Nuevo prop para Total Descuento
      type: Number,
      default: 0
    },
    total: {
      type: Number,
      required: true
    },
    selectedShipping: {
      type: String,
      default: 'standard'
    }
  },
  data() {
    return {
      localShipping: this.selectedShipping
    }
  },
  watch: {
    selectedShipping(newVal) {
      this.localShipping = newVal;
    }
  },
  methods: {
    updateShipping(value) {
      this.localShipping = value;
      this.$emit('shipping-changed', value);
    }
  }
}
</script>

<style scoped>
</style>
