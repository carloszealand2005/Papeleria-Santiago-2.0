<template>
  <div>
    <!-- Order Details Title -->
    <div class="mb-6">
      <h3 class="font-bold text-gray-800 text-lg border-b-2 border-gray-300 pb-2">Detalles del Pedido:</h3>
    </div>
    <!-- Products Table -->
    <div class="overflow-x-auto">
      <table class="w-full">
        <thead>
          <tr class="bg-gray-800 text-white">
            <th class="text-left py-3 px-4 font-semibold">Producto</th>
            <th class="text-center py-3 px-4 font-semibold">Cantidad</th>
            <th class="text-right py-3 px-4 font-semibold">Precio Unitario</th>
            <th class="text-right py-3 px-4 font-semibold">Total Producto</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="(item, index) in orderItems" 
            :key="index" 
            class="border-b border-gray-200 hover:bg-gray-50"
          >
            <td class="py-4 px-4 text-gray-900">{{ item.name }}</td>
            <td class="py-4 px-4 text-center text-gray-900">{{ item.quantity }}</td>
            <td class="py-4 px-4 text-right text-gray-900">${{ formatNumber(item.price) }}</td>
            <td class="py-4 px-4 text-right text-gray-900 font-semibold">${{ formatNumber(item.total) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ReceiptProducts',
  props: {
    orderItems: {
      type: Array,
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
/* Table styles for better readability */
table {
  border-collapse: collapse;
}

table th,
table td {
  border: 1px solid #e5e5e5;
}

/* Hover effects for better UX */
tr:hover {
  background-color: #f9f9f9;
}

/* Responsive design */
@media (max-width: 768px) {
  .overflow-x-auto {
    overflow-x: scroll;
  }
  
  table {
    min-width: 600px;
  }
}
</style>

