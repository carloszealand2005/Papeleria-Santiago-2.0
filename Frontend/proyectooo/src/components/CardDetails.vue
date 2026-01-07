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
          @input="handleInput('number')"
          @blur="handleBlur('number')"
        >
        <div class="absolute inset-y-0 right-0 flex items-center pr-3">
          <span v-if="brandLabel" class="text-xs font-semibold text-gray-500 mr-2">
            {{ brandLabel }}
          </span>
          <i class="fas fa-lock text-gray-400 text-sm"></i>
        </div>
      </div>
      <div v-if="shouldShowError('number')" class="text-red-500 text-xs mt-1">
        {{ errors.number }}
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
          @input="handleInput('expiry')"
          @blur="handleBlur('expiry')"
        >
        <div v-if="shouldShowError('expiry')" class="text-red-500 text-xs mt-1">
          {{ errors.expiry }}
        </div>
      </div>
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-2">CVV</label>
        <input
          type="text"
          v-model="localCardInfo.cvv"
          class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
          :placeholder="cvvPlaceholder"
          @input="handleInput('cvv')"
          @blur="handleBlur('cvv')"
        >
        <div v-if="shouldShowError('cvv')" class="text-red-500 text-xs mt-1">
          {{ errors.cvv }}
        </div>
      </div>
    </div>
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-2">Nombre del Titular</label>
      <input
        type="text"
        v-model="localCardInfo.holderName"
        class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm"
        placeholder="Juan Pérez"
        @input="handleInput('holderName')"
        @blur="handleBlur('holderName')"
      >
      <div v-if="shouldShowError('holderName')" class="text-red-500 text-xs mt-1">
        {{ errors.holderName }}
      </div>
    </div>
  </div>
</template>

<script>
import { formatExpiry, onlyDigits, validateCardInfo } from '@/utils/creditCardValidators';

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
      localCardInfo: { ...this.cardInfo },
      brand: null,
      errors: {},
      touched: {
        number: false,
        expiry: false,
        cvv: false,
        holderName: false
      }
    }
  },
  computed: {
    brandLabel() {
      // Para "unknown" mostramos "Tarjeta" como fallback
      return this.brand?.label || '';
    },
    cvvPlaceholder() {
      return this.brand?.code === 'amex' ? '1234' : '123';
    }
  },
  watch: {
    cardInfo: {
      deep: true,
      handler(newVal) {
        this.localCardInfo = { ...newVal };
        this.runValidation();
      }
    }
  },
  created() {
    this.runValidation();
  },
  methods: {
    updateCardInfo() {
      this.$emit('update:card-info', { ...this.localCardInfo });
    },
    shouldShowError(field) {
      return Boolean(this.touched?.[field] && this.errors?.[field]);
    },
    handleBlur(field) {
      this.$set(this.touched, field, true);
      this.runValidation();
    },
    handleInput(field) {
      // Normalizaciones suaves (mejor UX + evita caracteres inválidos)
      if (field === 'number') {
        const digits = onlyDigits(this.localCardInfo.number).slice(0, 19);
        // Agrupación simple de 4 dígitos (no depende de marca)
        this.localCardInfo.number = digits.replace(/(\d{4})(?=\d)/g, '$1 ');
      }
      if (field === 'expiry') {
        this.localCardInfo.expiry = formatExpiry(this.localCardInfo.expiry);
      }
      if (field === 'cvv') {
        // Amex puede ser 4; otras 3 (dejamos 4 por si la marca cambia mientras escribe)
        this.localCardInfo.cvv = onlyDigits(this.localCardInfo.cvv).slice(0, 4);
      }
      if (field === 'holderName') {
        // Solo limpieza básica de espacios
        this.localCardInfo.holderName = String(this.localCardInfo.holderName ?? '').replace(/\s+/g, ' ');
      }

      this.$set(this.touched, field, true);
      this.updateCardInfo();
      this.runValidation();
    },
    runValidation() {
      const result = validateCardInfo(this.localCardInfo);
      this.brand = result.brand;
      this.errors = result.errors || {};
      this.$emit('validation-changed', {
        isValid: result.isValid,
        brand: result.brand,
        errors: result.errors
      });
    },
  }
}
</script>

<style scoped>
</style>

