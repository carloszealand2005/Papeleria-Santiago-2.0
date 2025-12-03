<template>
  <div class="mt-8 flex justify-center space-x-4">
    <button
      @click="printReceipt"
      class="bg-gray-800 hover:bg-black text-white px-6 py-3 !rounded-button transition-colors whitespace-nowrap"
    >
      <i class="fas fa-print mr-2"></i>Imprimir Comprobante
    </button>
    <button
      @click="downloadPDF"
      class="bg-gray-600 hover:bg-gray-700 text-white px-6 py-3 !rounded-button transition-colors whitespace-nowrap"
    >
      <i class="fas fa-download mr-2"></i>Descargar PDF
    </button>
    <button
      @click="sendEmail"
      class="bg-gray-500 hover:bg-gray-600 text-white px-6 py-3 !rounded-button transition-colors whitespace-nowrap"
    >
      <i class="fas fa-envelope mr-2"></i>Enviar por Email
    </button>
  </div>
</template>

<script>
export default {
  name: 'ReceiptActions',
  methods: {
    printReceipt() {
      window.print();
      this.$emit('print');
    },
    downloadPDF() {
      // En una implementación real, se integraría con una librería como jsPDF
      console.log('Descargando comprobante como PDF...');
      this.$emit('download-pdf');
    },
    sendEmail() {
      // En una implementación real, se enviaría el comprobante por email
      console.log('Enviando comprobante por email...');
      this.$emit('send-email');
    }
  }
}
</script>

<style scoped>
/* Responsive design */
@media (max-width: 768px) {
  .space-x-4 {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .space-x-4 > * {
    margin-right: 0 !important;
    margin-bottom: 0.5rem;
    width: 100%;
  }
}
</style>

