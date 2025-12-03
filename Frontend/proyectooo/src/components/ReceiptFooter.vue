<template>
  <div class="mt-8 pt-6 border-t border-gray-300">
    <div class="text-center">
      <p class="text-gray-600 text-sm mb-2">Fecha de Emisión: {{ currentDate }}</p>
      <p class="text-gray-500 text-xs">Gracias por su compra en Papelería Santiago</p>
      <p class="text-gray-500 text-xs mt-2">
        Para consultas: info@papeleriasantiago.com | WhatsApp: +57 300 123 4567
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ReceiptFooter',
  computed: {
    currentDate() {
      return this.getCurrentDate();
    }
  },
  methods: {
    getCurrentDate() {
      const now = new Date();
      const day = String(now.getDate()).padStart(2, '0');
      const month = String(now.getMonth() + 1).padStart(2, '0');
      const year = now.getFullYear();
      return `${day}/${month}/${year}`;
    }
  }
}
</script>

<style scoped>
</style>

