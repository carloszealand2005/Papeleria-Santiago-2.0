<template>
  <div class="mt-8 grid grid-cols-2 gap-8">
    <div>
      <h4 class="font-semibold text-gray-800 mb-3">Información de Pago:</h4>
      <div class="space-y-2 text-sm">
        <div class="flex">
          <span class="text-gray-600 w-24">Método:</span>
          <span class="text-gray-900">{{ paymentInfo.method }}</span>
        </div>
        <div class="flex">
          <span class="text-gray-600 w-24">Estado:</span>
          <span class="text-green-600 font-semibold">{{ paymentInfo.status }}</span>
        </div>
        <div class="flex">
          <span class="text-gray-600 w-24">Referencia:</span>
          <span class="text-gray-900">{{ paymentInfo.reference }}</span>
        </div>
      </div>
    </div>
    <div>
      <h4 class="font-semibold text-gray-800 mb-3">Información de Entrega:</h4>
      <div class="space-y-2 text-sm">
        <div class="flex">
          <span class="text-gray-600 w-24">Tipo:</span>
          <span class="text-gray-900">{{ deliveryInfo.type }}</span>
        </div>
        <div class="flex">
          <span class="text-gray-600 w-24">Fecha:</span>
          <span class="text-gray-900">{{ deliveryInfo.date }}</span>
        </div>
        <div class="flex">
          <span class="text-gray-600 w-24">Dirección:</span>
          <span class="text-gray-900">{{ deliveryInfo.address }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ReceiptPaymentInfo',
  props: {
    paymentInfo: {
      type: Object,
      required: true
    },
    deliveryInfo: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
/* Responsive design */
@media (max-width: 768px) {
  .grid-cols-2 {
    grid-template-columns: 1fr;
  }
}
</style>

