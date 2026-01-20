<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
    <h2 class="text-xl font-semibold text-gray-900 mb-6">Método de Pago</h2>
    <div class="space-y-4 mb-6">
      <label 
        class="flex items-center p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50"
        :class="{ 'border-blue-600 bg-blue-50': selectedPayment === 'card' }"
      >
        <input
          type="radio"
          name="payment"
          value="card"
          v-model="localPayment"
          class="text-green-600 focus:ring-green-500"
          @change="updatePayment"
        >
        <div class="ml-3 flex items-center">
          <i class="fas fa-credit-card text-gray-500 mr-3"></i>
          <span class="font-medium text-gray-900">Tarjeta de Crédito/Débito</span>
        </div>
      </label>
      <label 
        class="flex items-center p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50"
        :class="{ 'border-blue-600 bg-blue-50': selectedPayment === 'transfer' }"
      >
        <input
          type="radio"
          name="payment"
          value="transfer"
          v-model="localPayment"
          class="text-green-600 focus:ring-green-500"
          @change="updatePayment"
        >
        <div class="ml-3 flex items-center">
          <i class="fas fa-university text-gray-500 mr-3"></i>
          <span class="font-medium text-gray-900">Transferencia Bancaria</span>
        </div>
      </label>
    </div>
    
    <!-- Card Details -->
    <CardDetails 
      v-if="selectedPayment === 'card'"
      :cardInfo="cardInfo"
      @update:card-info="$emit('update:card-info', $event)"
      @validation-changed="$emit('card-validation-changed', $event)"
    />
  </div>
</template>

<script>
import CardDetails from './CardDetails.vue';

export default {
  name: 'PaymentMethod',
  components: {
    CardDetails
  },
  props: {
    selectedPayment: {
      type: String,
      default: 'card'
    },
    cardInfo: {
      type: Object,
      default: () => ({
        number: '',
        expiry: '',
        cvv: '',
        holderName: ''
      })
    }
  },
  data() {
    return {
      localPayment: this.selectedPayment
    }
  },
  watch: {
    selectedPayment(newVal) {
      this.localPayment = newVal;
    }
  },
  methods: {
    updatePayment() {
      this.$emit('payment-changed', this.localPayment);
    }
  }
}
</script>

<style scoped>
</style>

