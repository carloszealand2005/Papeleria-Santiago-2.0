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
        <label class="block text-sm font-medium text-gray-700 mb-2">Cédula</label>
        <input
          type="text"
          inputmode="numeric"
          pattern="[0-9]*"
          maxlength="10"
          :value="billingInfo.cedula"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-600 focus:border-blue-600 text-sm"
          placeholder="Ej: 1710020030"
          @input="handleCedulaInput($event)"
        >
        <p v-if="cedulaError" class="mt-1 text-xs text-red-600">{{ cedulaError }}</p>
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
        <label class="block text-sm font-medium text-gray-700 mb-2">Número de casa / depto.</label>
        <input
          type="text"
          :value="billingInfo.houseNumber"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
          placeholder="Ej: 123, Dpto 4B"
          @input="updateField('houseNumber', $event.target.value)"
        >
      </div>
      <div class="md:col-span-2">
        <label class="block text-sm font-medium text-gray-700 mb-2">Dirección</label>
        <input
          type="text"
          :value="billingInfo.address"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
          placeholder="Calle Principal y Secundaria"
          @input="updateField('address', $event.target.value)"
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
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">Referencia (opcional)</label>
        <input
          type="text"
          :value="billingInfo.reference"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
          placeholder="Ej: Casa color blanco, frente al parque"
          @input="updateField('reference', $event.target.value)"
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
  computed: {
    cedulaError() {
      const value = String(this.billingInfo?.cedula ?? '').trim();
      if (!value) return '';
      if (!/^\d{10}$/.test(value)) return 'La cédula debe tener 10 dígitos.';
      if (!this.isValidEcuadorCedula(value)) return 'Cédula inválida.';
      return '';
    }
  },
  methods: {
    updateField(field, value) {
      const updatedInfo = {
        ...this.billingInfo,
        [field]: value
      };
      this.$emit('update:billing-info', updatedInfo);
    },
    handleCedulaInput(event) {
      const raw = event?.target?.value ?? '';
      const onlyDigits = String(raw).replace(/\D/g, '').slice(0, 10);
      this.updateField('cedula', onlyDigits);
    },
    // Validación de cédula ecuatoriana (10 dígitos + checksum)
    isValidEcuadorCedula(cedula) {
      if (!/^\d{10}$/.test(cedula)) return false;

      const province = parseInt(cedula.slice(0, 2), 10);
      if (province < 1 || province > 24) return false;

      const third = parseInt(cedula[2], 10);
      if (third < 0 || third > 5) return false;

      const digits = cedula.split('').map((d) => parseInt(d, 10));
      const coeffs = [2, 1, 2, 1, 2, 1, 2, 1, 2];
      let sum = 0;
      for (let i = 0; i < 9; i++) {
        let prod = digits[i] * coeffs[i];
        if (prod >= 10) prod -= 9;
        sum += prod;
      }
      const checkDigit = (10 - (sum % 10)) % 10;
      return checkDigit === digits[9];
    }
  }
}
</script>

<style scoped>
</style>

