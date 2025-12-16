<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <CheckoutHeader />
    
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
    <CheckoutFooter />
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
  inject: ['checkoutOrderItems', 'checkoutTotals', 'completeOrderHandler'],
  mounted() {
    // Validar que haya datos de checkout antes de mostrar la página
    this.$nextTick(() => {
      try {
        const hasOrderItems = (this.checkoutOrderItems && this.checkoutOrderItems.length > 0) ||
                              (this.orderItems && this.orderItems.length > 0);
        
        if (!hasOrderItems) {
          console.warn('No hay items en el checkout, redirigiendo al carrito');
          this.$router.push('/carrito');
        }
      } catch (error) {
        console.error('Error en mounted de Checkout:', error);
        this.$router.push('/carrito');
      }
    });
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
    orderItems() {
      try {
        return this.checkoutOrderItems || [];
      } catch (error) {
        console.error('Error al obtener orderItems:', error);
        return [];
      }
    },
    totals() {
      try {
        return this.checkoutTotals || {
          subtotal: 0,
          tax: 0,
          total: 0
        };
      } catch (error) {
        console.error('Error al obtener totals:', error);
        return {
          subtotal: 0,
          tax: 0,
          total: 0
        };
      }
    },
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
      this.$router.push('/carrito');
    },
    completeOrder() {
      if (this.validateForm()) {
        const orderData = {
          billingInfo: this.billingInfo,
          shipping: this.selectedShipping,
          shippingCost: this.shippingCost,
          payment: this.selectedPayment,
          cardInfo: this.selectedPayment === 'card' ? this.cardInfo : null,
          items: this.orderItems,
          totals: {
            ...this.totals,
            shipping: this.shippingCost,
            total: this.totals.total + this.shippingCost
          }
        };
        if (this.completeOrderHandler) {
          this.completeOrderHandler(orderData);
        }
        // Navegar a la factura después de completar la orden
        this.$router.push('/factura');
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

