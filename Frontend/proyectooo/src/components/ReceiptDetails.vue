<template>
  <div class="p-8">
    <div class="grid grid-cols-2 gap-8 mb-8">
      <!-- Invoice Info -->
      <div class="space-y-3">
        <div class="flex">
          <span class="font-semibold text-gray-700 w-32">Número de Factura:</span>
          <span class="text-gray-900">{{ invoiceData.number }}</span>
        </div>
        <div class="flex">
          <span class="font-semibold text-gray-700 w-32">Fecha de Emisión:</span>
          <span class="text-gray-900">{{ invoiceData.date }}</span>
        </div>
      </div>
      <!-- Customer Info -->
      <div class="space-y-3">
        <h3 class="font-bold text-gray-800 border-b border-gray-300 pb-2">Datos del Cliente:</h3>
        <div class="space-y-2">
          <div class="flex">
            <span class="font-medium text-gray-700 w-20">Nombre:</span>
            <span class="text-gray-900">{{ customerData.name }}</span>
          </div>
          <div class="flex">
            <span class="font-medium text-gray-700 w-20">Cédula:</span>
            <span class="text-gray-900">{{ customerData.id }}</span>
          </div>
          <div class="flex">
            <span class="font-medium text-gray-700 w-20">Email:</span>
            <span class="text-gray-900">{{ customerData.email }}</span>
          </div>
          <div class="flex">
            <span class="font-medium text-gray-700 w-20">Dirección:</span>
            <span class="text-gray-900">{{ customerData.address }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ReceiptDetails',
  props: {
    invoiceData: {
      type: Object,
      required: true
    },
    customerData: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
</style>

