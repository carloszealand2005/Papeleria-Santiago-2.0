<template>
  <div class="border-b-2 border-gray-800 p-8">
    <div class="flex justify-between items-start">
      <!-- Logo and Company Info -->
      <div class="flex items-center space-x-4">
        <img 
          src="https://static.readdy.ai/image/a6354382ff0904464d2c460063bc60ba/6f8df39c3ebbe09774d9149fa1ed46ec.png" 
          alt="Santiago Papelería" 
          class="h-16 w-auto"
        >
        <div>
          <h1 class="text-2xl font-bold text-gray-900">PAPELERÍA SANTIAGO</h1>
          <p class="text-gray-600 text-sm">Soluciones completas para oficina y estudio</p>
          <p class="text-gray-500 text-xs">NIT: 900.123.456-7</p>
          <p class="text-gray-500 text-xs">Cra 15 #45-32, Bogotá, Colombia</p>
          <p class="text-gray-500 text-xs">Tel: (601) 234-5678</p>
        </div>
      </div>
      <!-- Invoice Title -->
      <div class="text-right">
        <h2 class="text-3xl font-bold text-gray-800 border-b-2 border-gray-300 pb-2">COMPROBANTE</h2>
        <p class="text-gray-600 text-sm mt-2">Recibo de Compra</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ReceiptHeader'
}
</script>

<style scoped>
</style>

