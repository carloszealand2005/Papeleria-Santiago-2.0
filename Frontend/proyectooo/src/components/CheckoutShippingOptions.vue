<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
    <h2 class="text-xl font-semibold text-gray-900 mb-6">Opciones de Envío</h2>
    <div class="space-y-3">
      <label 
        class="flex items-center p-4 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50"
        :class="{ 'border-blue-600 bg-blue-50': selectedShipping === 'standard' }"
      >
        <input
          type="radio"
          name="shipping"
          value="standard"
          v-model="localShipping"
          class="focus:ring-2"
          style="color: #2563EB; --tw-ring-color: #2563EB;"
          @change="updateShipping"
        >
        <div class="ml-3 flex-1 flex items-center justify-between">
          <div class="flex items-center">
            <i class="fas fa-truck text-gray-500 mr-3"></i>
            <div>
              <div class="font-medium text-gray-900">Envío Estándar</div>
              <div class="text-sm text-gray-600">3-5 días hábiles</div>
            </div>
          </div>
          <span class="font-semibold" style="color: #2563EB;">Gratis</span>
        </div>
      </label>
      <label 
        class="flex items-center p-4 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50"
        :class="{ 'border-blue-600 bg-blue-50': selectedShipping === 'express' }"
      >
        <input
          type="radio"
          name="shipping"
          value="express"
          v-model="localShipping"
          class="text-green-600 focus:ring-green-500"
          @change="updateShipping"
        >
        <div class="ml-3 flex-1 flex items-center justify-between">
          <div class="flex items-center">
            <i class="fas fa-bolt text-gray-500 mr-3"></i>
            <div>
              <div class="font-medium text-gray-900">Envío Express</div>
              <div class="text-sm text-gray-600">1-2 días hábiles</div>
            </div>
          </div>
          <span class="font-semibold text-gray-900">$50.00</span>
        </div>
      </label>
      <label 
        class="flex items-center p-4 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50"
        :class="{ 'border-blue-600 bg-blue-50': selectedShipping === 'pickup' }"
      >
        <input
          type="radio"
          name="shipping"
          value="pickup"
          v-model="localShipping"
          class="text-green-600 focus:ring-green-500"
          @change="updateShipping"
        >
        <div class="ml-3 flex-1 flex items-center justify-between">
          <div class="flex items-center">
            <i class="fas fa-store text-gray-500 mr-3"></i>
            <div>
              <div class="font-medium text-gray-900">Recogida en Tienda</div>
              <div class="text-sm text-gray-600">Disponible hoy</div>
            </div>
          </div>
          <span class="font-semibold" style="color: #2563EB;">Gratis</span>
        </div>
      </label>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CheckoutShippingOptions',
  props: {
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
    updateShipping() {
      this.$emit('shipping-changed', this.localShipping);
    }
  }
}
</script>

<style scoped>
</style>

