<template>
  <div class="mt-8">
    <div class="flex justify-end">
      <div class="w-80">
        <div class="space-y-2">
          <div class="flex justify-between py-2 border-b border-gray-200">
            <span class="text-gray-700">Subtotal:</span>
            <span class="text-gray-900 font-semibold">${{ formatNumber(totals.subtotal) }}</span>
          </div>
          <div class="flex justify-between py-2 border-b border-gray-200">
            <span class="text-gray-700">Descuento:</span>
            <span class="text-gray-900">${{ formatNumber(totals.discount) }}</span>
          </div>
          <div class="flex justify-between py-2 border-b border-gray-400">
            <span class="text-gray-700">IVA (19%):</span>
            <span class="text-gray-900">${{ formatNumber(totals.tax) }}</span>
          </div>
          <div class="flex justify-between py-3 border-b-2 border-gray-800 bg-gray-100 px-4">
            <span class="text-lg font-bold text-gray-800">Total a Pagar:</span>
            <span class="text-lg font-bold text-gray-900">${{ formatNumber(totals.total) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ReceiptTotals',
  props: {
    totals: {
      type: Object,
      required: true
    }
  },
  methods: {
    formatNumber(number) {
      return number.toFixed(2).replace(/\d(?=(\d{3})+\.)/g, '$&,');
    }
  }
}
</script>

<style scoped>
</style>

