<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
    <h2 class="text-xl font-semibold text-gray-900 mb-6">Información de Facturación</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Nombre Completo</label>
        <input
          type="text"
          :value="billingInfo.fullName"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-blue-600 text-sm"
          placeholder="Juan Pérez"
          @input="updateField('fullName', $event.target.value)"
        >
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Teléfono</label>
        <input
          type="tel"
          :value="billingInfo.phone"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-blue-600 text-sm"
          placeholder="(55) 1234-5678"
          @input="updateField('phone', $event.target.value)"
        >
      </div>
      <div class="md:col-span-2">
        <label class="block text-sm font-medium text-gray-700 mb-2">Dirección</label>
        <input
          type="text"
          :value="billingInfo.address"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
          placeholder="Calle Principal 123"
          @input="updateField('address', $event.target.value)"
        >
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Ciudad</label>
        <input
          type="text"
          :value="billingInfo.city"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
          placeholder="Ciudad de México"
          @input="updateField('city', $event.target.value)"
        >
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Código Postal</label>
        <input
          type="text"
          :value="billingInfo.zipCode"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
          placeholder="01000"
          @input="updateField('zipCode', $event.target.value)"
        >
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BillingInfo',
  props: {
    billingInfo: {
      type: Object,
      required: true
    }
  },
  methods: {
    updateField(field, value) {
      const updatedInfo = {
        ...this.billingInfo,
        [field]: value
      };
      this.$emit('update:billing-info', updatedInfo);
    }
  }
}
</script>

<style scoped>
</style>

