<template>
  <div class="space-y-4 border-t border-gray-200 pt-4">
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">Número de Tarjeta</label>
      <div class="relative">
        <input
          type="text"
          v-model="localCardInfo.number"
          class="w-full px-3 py-2 pr-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
          placeholder="1234 5678 9012 3456"
          @input="updateCardInfo"
        >
        <div class="absolute inset-y-0 right-0 flex items-center pr-3">
          <i class="fas fa-lock text-gray-400 text-sm"></i>
        </div>
      </div>
    </div>
    <div class="grid grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Fecha de Vencimiento</label>
        <input
          type="text"
          v-model="localCardInfo.expiry"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
          placeholder="MM/AA"
          @input="updateCardInfo"
        >
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">CVV</label>
        <input
          type="text"
          v-model="localCardInfo.cvv"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
          placeholder="123"
          @input="updateCardInfo"
        >
      </div>
    </div>
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">Nombre del Titular</label>
      <input
        type="text"
        v-model="localCardInfo.holderName"
        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
        placeholder="Juan Pérez"
        @input="updateCardInfo"
      >
    </div>
  </div>
</template>

<script>
export default {
  name: 'CardDetails',
  props: {
    cardInfo: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      localCardInfo: { ...this.cardInfo }
    }
  },
  watch: {
    cardInfo: {
      deep: true,
      handler(newVal) {
        this.localCardInfo = { ...newVal };
      }
    }
  },
  methods: {
    updateCardInfo() {
      this.$emit('update:card-info', { ...this.localCardInfo });
    }
  }
}
</script>

<style scoped>
</style>

