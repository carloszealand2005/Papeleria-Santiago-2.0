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
            :totals="displayTotals"
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
            @card-validation-changed="handleCardValidationChanged"
          />

          <!-- Transferencia bancaria: instrucciones + comprobante -->
          <div
            v-if="selectedPayment === 'transfer'"
            class="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
          >
            <h2 class="text-xl font-semibold text-gray-900 mb-2">Realiza una transferencia bancaria</h2>
            <p class="text-sm text-gray-600 mb-4">
              Sube el comprobante para que podamos verificar tu pago.
            </p>

            <div class="p-4 rounded-lg border border-blue-200 bg-blue-50 text-blue-900">
              <div class="font-semibold">Banco de Loja</div>
              <div class="text-sm mt-2 space-y-1">
                <div><span class="font-medium">N. Cuenta:</span> 2902563522</div>
                <div><span class="font-medium">Tipo de cuenta:</span> Cuenta de ahorros</div>
                <div><span class="font-medium">Nombre:</span> Aarón Robles</div>
              </div>
            </div>

            <div class="mt-5">
              <label class="block text-sm font-medium text-gray-700 mb-2">
                Comprobante de transferencia (solo fotos)
              </label>
              <input
                ref="transferProofInput"
                type="file"
                accept="image/*"
                class="block w-full text-sm text-gray-700 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-gray-100 file:text-gray-800 hover:file:bg-gray-200"
                @change="handleTransferProofChange"
              />

              <div v-if="transferProofError" class="text-xs text-red-600 mt-2">
                {{ transferProofError }}
              </div>

              <div v-if="transferProofFile" class="mt-4 flex flex-col sm:flex-row gap-4 sm:items-center">
                <div class="text-sm text-gray-700">
                  <div class="font-medium text-gray-900">Archivo cargado</div>
                  <div class="text-xs text-gray-600 mt-1 break-all">{{ transferProofFile.name }}</div>
                </div>
                <div class="sm:ml-auto flex items-center gap-2">
                  <button
                    type="button"
                    class="px-4 py-2 border border-gray-300 hover:bg-gray-50 text-gray-800 rounded-lg transition-colors cursor-pointer"
                    @click="removeTransferProof"
                  >
                    Quitar
                  </button>
                </div>
              </div>

              <div v-if="transferProofPreviewUrl" class="mt-4">
                <div class="text-xs font-medium text-gray-600 mb-2">Vista previa</div>
                <img
                  :src="transferProofPreviewUrl"
                  alt="Vista previa del comprobante de transferencia"
                  class="max-h-64 w-auto rounded-lg border border-gray-200"
                />
              </div>

              <div v-else class="text-xs text-gray-500 mt-3">
                El botón “Finalizar Compra” se habilitará cuando subas tu comprobante.
              </div>
            </div>
          </div>
          
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
              :disabled="isFinalizeDisabled"
              :class="{ 'opacity-60 cursor-not-allowed': isFinalizeDisabled }"
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
        cedula: '',
        phone: '',
        address: '',
        city: '',
        houseNumber: '',
        reference: '',
        zipCode: ''
      },
      selectedShipping: 'standard',
      selectedPayment: 'card',
      cardInfo: {
        number: '',
        expiry: '',
        cvv: '',
        holderName: ''
      },
      cardValidation: {
        isValid: false,
        brand: null,
        errors: {}
      },
      transferProofFile: null,
      transferProofPreviewUrl: '',
      transferProofError: '',
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated']),
    isFinalizeDisabled() {
      if (this.isProcessingPayment) return true;
      if (this.selectedPayment === 'card') return !this.cardValidation.isValid;
      if (this.selectedPayment === 'transfer') return !this.transferProofFile;
      return false;
    },
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
      // Por ahora es visual (luego se integra con backend).
      // Envío Estándar fijo: $3.00
      return 3.00;
    },
    displayTotals() {
      // Total visual: total backend + envío
      const base = this.totals || { subtotal: 0, totalDiscount: 0, totalIva: 0, total: 0 };
      return {
        ...base,
        total: (parseFloat(base.total || 0) || 0) + (parseFloat(this.shippingCost || 0) || 0),
      };
    }
  },
  created() {
    this.fetchCheckoutCart();
    this.autofillBillingFromProfile();
  },
  methods: {
    paymentMethodLabel() {
      // Backend espera: "Tarjeta" o "Transferencia bancaria"
      return this.selectedPayment === 'card' ? 'Tarjeta' : 'Transferencia bancaria';
    },
    buildCheckoutPayload() {
      const b = this.billingInfo || {};
      return {
        ciudad_envio: String(b.city || '').trim(),
        direccion_envio: String(b.address || '').trim(),
        numero_casa_envio: String(b.houseNumber || '').trim(),
        codigo_postal_envio: String(b.zipCode || '').trim(),
        cedula_envio: String(b.cedula || '').trim(),
        telefono_envio: String(b.phone || '').trim(),
        referencia_envio: String(b.reference || '').trim(),
        metodo_pago: this.paymentMethodLabel(),
        costo_envio: Number.parseFloat(this.shippingCost || 0) || 0,
      };
    },
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
        if (!this.billingInfo.cedula) {
          this.billingInfo.cedula = profile.cedula ?? '';
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
    handleCardValidationChanged(payload) {
      this.cardValidation = payload || { isValid: false, brand: null, errors: {} };
    },
    handleTransferProofChange(event) {
      this.transferProofError = '';
      const file = event && event.target && event.target.files && event.target.files[0] ? event.target.files[0] : null;
      if (!file) {
        this.removeTransferProof();
        return;
      }
      if (!String(file.type || '').startsWith('image/')) {
        this.transferProofError = 'El archivo debe ser una imagen.';
        this.removeTransferProof();
        return;
      }
      this.transferProofFile = file;
      try {
        if (this.transferProofPreviewUrl) URL.revokeObjectURL(this.transferProofPreviewUrl);
      } catch (e) {
        // No bloqueamos por esto
      }
      this.transferProofPreviewUrl = URL.createObjectURL(file);
    },
    removeTransferProof() {
      this.transferProofFile = null;
      this.transferProofError = '';
      try {
        if (this.transferProofPreviewUrl) URL.revokeObjectURL(this.transferProofPreviewUrl);
      } catch (e) {
        // No bloqueamos por esto
      }
      this.transferProofPreviewUrl = '';
      const input = this.$refs && this.$refs.transferProofInput;
      if (input) input.value = '';
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
        // Transferencia: se paga como "EN REVISIÓN" (subiendo comprobante) y NO se genera factura/envío aún.
        if (this.selectedPayment === 'transfer') {
          const payload = this.buildCheckoutPayload();
          const form = new FormData();
          Object.keys(payload || {}).forEach((k) => {
            const v = payload[k];
            // FormData solo acepta string/blob; normalizamos a string
            form.append(k, v === null || v === undefined ? '' : String(v));
          });
          // Backend espera este nombre para guardar en Pedido.comprobante_transferencia
          form.append('comprobante_transferencia', this.transferProofFile);

          const payRes = await api.post('/mi-carrito/pagar/', form, {
            headers: { 'Content-Type': 'multipart/form-data' },
          });
          const pedidoId = payRes?.data?.pedido_id;
          if (!pedidoId) {
            throw new Error('No se recibió pedido_id al pagar el carrito (transferencia).');
          }

          // UX: llevar al usuario a Mis pedidos para ver estado "En revisión"
          this.$router.push({ path: '/mi-cuenta', query: { section: 'orders' } });
          return;
        }

        // 1) Pagar el carrito (crea pedido + comprobante en backend)
        const payload = this.buildCheckoutPayload();
        const payRes = await api.post('/mi-carrito/pagar/', payload);
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
      // Nota: el backend ahora prioriza estos datos enviados en /mi-carrito/pagar/,
      // por lo que validamos que lo esencial no se envíe vacío.
      if (
        !this.billingInfo.fullName ||
        !this.billingInfo.cedula ||
        !this.billingInfo.phone ||
        !this.billingInfo.address ||
        !this.billingInfo.city ||
        !this.billingInfo.houseNumber ||
        !this.billingInfo.zipCode
      ) {
        this.paymentError = 'Por favor completa todos los campos de facturación.';
        return false;
      }
      if (!this.isValidEcuadorCedula(String(this.billingInfo.cedula || '').trim())) {
        this.paymentError = 'Por favor ingresa una cédula válida.';
        return false;
      }
      if (this.selectedPayment === 'card') {
        if (!this.cardValidation.isValid) {
          this.paymentError = 'Revisa los datos de la tarjeta.';
          return false;
        }
      }
      if (this.selectedPayment === 'transfer') {
        if (!this.transferProofFile) {
          this.paymentError = 'Por favor sube el comprobante de transferencia.';
          return false;
        }
      }
      return true;
    },
    // Validación de cédula ecuatoriana (10 dígitos + checksum)
    isValidEcuadorCedula(cedula) {
      const value = String(cedula || '').trim();
      if (!/^\d{10}$/.test(value)) return false;

      const province = parseInt(value.slice(0, 2), 10);
      if (province < 1 || province > 24) return false;

      const third = parseInt(value[2], 10);
      if (third < 0 || third > 5) return false;

      const digits = value.split('').map((d) => parseInt(d, 10));
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

