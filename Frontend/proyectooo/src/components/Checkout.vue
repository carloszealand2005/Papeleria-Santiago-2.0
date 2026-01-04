<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-6 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- Order Summary -->
        <div class="lg:col-span-1">
          <!-- Si no llegan datos de checkout (por ejemplo al recargar /checkout),
               mostramos un aviso y dejamos al usuario en la página en vez de redirigirlo -->
          <div
            v-if="missingCheckoutData"
            class="mb-4 p-4 bg-yellow-50 border border-yellow-200 text-yellow-800 rounded-lg"
          >
            No se encontraron datos del pedido para mostrar. Vuelve al carrito y presiona “Proceder al Pago” nuevamente.
          </div>
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
import api from '@/utils/api';
import CheckoutOrderSummary from './CheckoutOrderSummary.vue';
import BillingInfo from './BillingInfo.vue';
import CheckoutShippingOptions from './CheckoutShippingOptions.vue';
import PaymentMethod from './PaymentMethod.vue';
import CheckoutFooter from './CheckoutFooter.vue';
import { mapGetters } from 'vuex';

export default {
  name: 'CheckoutPage',
  components: {
    CheckoutOrderSummary,
    BillingInfo,
    CheckoutShippingOptions,
    PaymentMethod,
    CheckoutFooter
  },
  inject: ['completeOrderHandler'],
  data() {
    return {
      missingCheckoutData: false,
      cart: null,
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
    ...mapGetters(['isAuthenticated']),
    orderItems() {
      try {
        return this.cart && Array.isArray(this.cart.detalles_carrito) ? this.cart.detalles_carrito : [];
      } catch (error) {
        console.error('Error al obtener orderItems:', error);
        return [];
      }
    },
    totals() {
      try {
        // Totales consistentes con /carrito (backend)
        return {
          subtotal: this.cart ? parseFloat(this.cart.subtotal_carrito || 0) : 0,
          totalDiscount: this.cart ? parseFloat(this.cart.descuento_carrito || 0) : 0,
          totalIva: this.cart ? parseFloat(this.cart.iva_carrito || 0) : 0,
          total: this.cart ? parseFloat(this.cart.total_carrito || 0) : 0
        };
      } catch (error) {
        console.error('Error al obtener totals:', error);
        return {
          subtotal: 0,
          totalDiscount: 0,
          totalIva: 0,
          total: 0
        };
      }
    },
    shippingCost() {
      // Por ahora, envío estático a $0 para mantener consistencia con /carrito
      return 0;
    }
  },
  created() {
    this.fetchCheckoutCart();
  },
  methods: {
    async fetchCheckoutCart() {
      try {
        if (!this.isAuthenticated) {
          this.missingCheckoutData = true;
          this.cart = null;
          return;
        }
        const response = await api.get('/mi-carrito/obtener/');
        this.cart = response.data;
        this.missingCheckoutData = !this.orderItems || this.orderItems.length === 0;
      } catch (error) {
        console.error('Error al cargar el carrito para checkout:', error);
        this.cart = null;
        this.missingCheckoutData = true;
      }
    },
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

