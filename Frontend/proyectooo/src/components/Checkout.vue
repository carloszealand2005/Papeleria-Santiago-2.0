<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <CheckoutHeader @go-home="$emit('go-home')" />
    
    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-6 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Order Summary -->
        <div class="lg:col-span-1">
          <CheckoutOrderSummary
            :orderItems="orderItems"
            :totals="totals"
            :shippingCost="shippingCost"
          />
        </div>
        
        <!-- Payment Form -->
        <div class="space-y-6">
          <!-- Billing Information -->
          <BillingInfo
            :billingInfo="billingInfo"
            @update:billing-info="handleBillingUpdate"
          />
          
          <!-- Shipping Options -->
          <CheckoutShippingOptions
            :selectedShipping="selectedShipping"
            @shipping-changed="handleShippingChanged"
          />
          
          <!-- Payment Method -->
          <PaymentMethod
            :selectedPayment="selectedPayment"
            :cardInfo="cardInfo"
            @payment-changed="handlePaymentChanged"
            @update:card-info="handleCardUpdate"
          />
          
          <!-- Action Buttons -->
          <div class="flex flex-col sm:flex-row gap-4">
            <button
              @click="goBack"
              class="flex-1 px-6 py-3 border text-white rounded-lg hover:bg-blue-700 transition-colors !rounded-button whitespace-nowrap cursor-pointer"
              style="border-color: #2563EB; background-color: #2563EB;"
            >
              <i class="fas fa-arrow-left mr-2"></i>
              Regresar
            </button>
            <button
              @click="completeOrder"
              class="flex-1 px-6 py-3 text-white rounded-lg hover:bg-blue-700 transition-colors !rounded-button whitespace-nowrap cursor-pointer"
              style="background-color: #2563EB;"
            >
              <i class="fas fa-check mr-2"></i>
              Finalizar Compra
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Security Footer -->
    <CheckoutFooter @navigate="handleNavigate" />
  </div>
</template>

<script>
import CheckoutHeader from './CheckoutHeader.vue';
import CheckoutOrderSummary from './CheckoutOrderSummary.vue';
import BillingInfo from './BillingInfo.vue';
import CheckoutShippingOptions from './CheckoutShippingOptions.vue';
import PaymentMethod from './PaymentMethod.vue';
import CheckoutFooter from './CheckoutFooter.vue';

export default {
  name: 'CheckoutPage',
  components: {
    CheckoutHeader,
    CheckoutOrderSummary,
    BillingInfo,
    CheckoutShippingOptions,
    PaymentMethod,
    CheckoutFooter
  },
  props: {
    orderItems: {
      type: Array,
      default: () => [
        {
          name: 'Cuaderno Profesional A4',
          quantity: 2,
          price: 120.00,
          image: 'https://readdy.ai/api/search-image?query=modern%20office%20notebook%20with%20spiral%20binding%20on%20clean%20white%20background%20minimalist%20product%20photography%20studio%20lighting%20professional%20commercial%20style&width=80&height=80&seq=001&orientation=squarish'
        },
        {
          name: 'Set de Plumas Gel',
          quantity: 1,
          price: 85.00,
          image: 'https://readdy.ai/api/search-image?query=set%20of%20colorful%20gel%20pens%20arranged%20neatly%20on%20white%20background%20professional%20product%20photography%20clean%20minimalist%20style%20office%20supplies&width=80&height=80&seq=002&orientation=squarish'
        },
        {
          name: 'Marcadores Fluorescentes',
          quantity: 1,
          price: 65.00,
          image: 'https://readdy.ai/api/search-image?query=yellow%20highlighter%20markers%20set%20on%20clean%20white%20background%20professional%20product%20photography%20minimalist%20style%20office%20supplies%20commercial%20lighting&width=80&height=80&seq=003&orientation=squarish'
        }
      ]
    },
    totals: {
      type: Object,
      default: () => ({
        subtotal: 270.00,
        tax: 43.20,
        total: 313.20
      })
    }
  },
  data() {
    return {
      billingInfo: {
        fullName: '',
        phone: '',
        address: '',
        city: '',
        zipCode: ''
      },
      selectedShipping: 'standard',
      selectedPayment: 'card',
      cardInfo: {
        number: '',
        expiry: '',
        cvv: '',
        holderName: ''
      }
    }
  },
  computed: {
    shippingCost() {
      if (this.selectedShipping === 'express') {
        return 50.00;
      }
      return 0;
    }
  },
  methods: {
    handleBillingUpdate(info) {
      this.billingInfo = info;
    },
    handleShippingChanged(shipping) {
      this.selectedShipping = shipping;
      this.$emit('shipping-changed', shipping);
    },
    handlePaymentChanged(payment) {
      this.selectedPayment = payment;
      this.$emit('payment-changed', payment);
    },
    handleCardUpdate(cardInfo) {
      this.cardInfo = cardInfo;
    },
    goBack() {
      this.$emit('go-back');
    },
    completeOrder() {
      if (this.validateForm()) {
        const orderData = {
          billingInfo: this.billingInfo,
          shipping: this.selectedShipping,
          shippingCost: this.shippingCost,
          payment: this.selectedPayment,
          cardInfo: this.selectedPayment === 'card' ? this.cardInfo : null,
          orderItems: this.orderItems,
          totals: {
            ...this.totals,
            shipping: this.shippingCost,
            total: this.totals.total + this.shippingCost
          }
        };
        this.$emit('complete-order', orderData);
      }
    },
    validateForm() {
      if (!this.billingInfo.fullName || !this.billingInfo.address || !this.billingInfo.city) {
        alert('Por favor completa todos los campos de facturación.');
        return false;
      }
      if (this.selectedPayment === 'card') {
        if (!this.cardInfo.number || !this.cardInfo.expiry || !this.cardInfo.cvv || !this.cardInfo.holderName) {
          alert('Por favor completa todos los datos de la tarjeta.');
          return false;
        }
      }
      return true;
    },
    handleNavigate(route) {
      this.$emit('navigate', route);
    }
  }
}
</script>

<style scoped>
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type="number"] {
  -moz-appearance: textfield;
}
</style>

