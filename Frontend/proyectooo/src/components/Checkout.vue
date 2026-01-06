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
          <div
            v-if="isProcessingPayment"
            class="p-4 bg-blue-50 border border-blue-200 text-blue-800 rounded-lg"
          >
            Procesando tu compra y generando el comprobante... Por favor espera.
          </div>
          <div
            v-if="paymentError"
            class="p-4 bg-red-50 border border-red-200 text-red-800 rounded-lg"
          >
            {{ paymentError }}
          </div>
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
              :disabled="isProcessingPayment"
              :class="{ 'opacity-60 cursor-not-allowed': isProcessingPayment }"
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
  // Nota: Antes se usaba `completeOrderHandler` para construir una factura HTML.
  // Ahora, la factura real viene del backend como PDF (embebido + descarga).
  data() {
    return {
      missingCheckoutData: false,
      cart: null,
      isProcessingPayment: false,
      paymentError: '',
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
    this.autofillBillingFromProfile();
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
    async autofillBillingFromProfile() {
      try {
        if (!this.isAuthenticated) return;

        const res = await api.get('/mi-perfil/');
        const profile = res?.data || {};

        // Autocompletar solo si el usuario aún no escribió en el campo
        if (!this.billingInfo.fullName) {
          this.billingInfo.fullName = profile.nombre ?? '';
        }
        if (!this.billingInfo.phone) {
          this.billingInfo.phone = profile.telefono ?? '';
        }
        if (!this.billingInfo.address) {
          this.billingInfo.address = profile.direccion ?? '';
        }
        if (!this.billingInfo.city) {
          this.billingInfo.city = profile.ciudad ?? '';
        }
        // zipCode queda vacío (dirección postal)
      } catch (error) {
        // No bloqueamos el checkout por esto; solo dejamos campos vacíos si falla.
        console.error('Error autocompletando datos de facturación desde /mi-perfil/:', error);
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
    async completeOrder() {
      if (this.isProcessingPayment) return;
      this.paymentError = '';

      if (!this.validateForm()) return;
      if (!this.isAuthenticated) {
        this.paymentError = 'Debes iniciar sesión para finalizar la compra.';
        this.$router.push('/login');
        return;
      }
      if (!this.orderItems || this.orderItems.length === 0) {
        this.paymentError = 'No hay productos en el carrito para pagar.';
        return;
      }

      this.isProcessingPayment = true;

      try {
        // 1) Pagar el carrito (crea pedido + comprobante en backend)
        const payRes = await api.post('/mi-carrito/pagar/');
        const pedidoId = payRes?.data?.pedido_id;

        if (!pedidoId) {
          throw new Error('No se recibió pedido_id al pagar el carrito.');
        }

        // 2) Obtener links del comprobante (PDF embebible + descarga)
        const linkRes = await api.get(`/mis-pedidos/${pedidoId}/comprobante/link/`);
        const pdfUrl = linkRes?.data?.pdf_url || '';
        const pdfUrlDownload = linkRes?.data?.pdf_url_download || '';
        const expiresInSeconds = linkRes?.data?.expires_in_seconds || 0;

        if (!pdfUrl || !pdfUrlDownload) {
          throw new Error('No se recibieron enlaces del comprobante (pdf_url / pdf_url_download).');
        }

        // Persistimos datos para /factura (evita depender de query params largos)
        const now = Date.now();
        const expiresAtMs = expiresInSeconds ? now + (expiresInSeconds * 1000) : 0;

        sessionStorage.setItem('receipt_pedido_id', String(pedidoId));
        sessionStorage.setItem('receipt_pdf_url', pdfUrl);
        sessionStorage.setItem('receipt_pdf_url_download', pdfUrlDownload);
        sessionStorage.setItem('receipt_pdf_expires_at_ms', String(expiresAtMs));

        // Navegar a factura una vez que el PDF ya está listo para embebido
        this.$router.push('/factura');
      } catch (error) {
        console.error('Error al finalizar la compra:', error);
        this.paymentError = 'No se pudo finalizar la compra. Por favor intenta nuevamente.';
      } finally {
        this.isProcessingPayment = false;
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
  appearance: textfield;
  -moz-appearance: textfield;
}
</style>

