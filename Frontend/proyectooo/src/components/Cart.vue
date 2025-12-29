<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <CartHeader 
      @search="handleSearch"
    />
    
    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Cart Header -->
          <CartPageHeader 
        :itemCount="currentCartItems.length"
      />
      
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Cart Items -->
        <div class="lg:col-span-2">
          <CartItems
            :cartItems="currentCartItems"
            @increase-quantity="increaseQuantity"
            @decrease-quantity="decreaseQuantity"
            @remove-item="removeItem"
          />
          
          <!-- Discount Code Section -->
          <DiscountCode
            :appliedDiscount="appliedDiscount"
            @apply-discount="applyDiscount"
          />
        </div>
        
        <!-- Order Summary -->
        <OrderSummary
          :subtotal="subtotal"
          :shipping="shipping"
          :totalDiscount="totalDiscount"
          :totalIva="totalIva"
          :total="total"
          :selectedShipping="selectedShipping"
          @shipping-changed="handleShippingChanged"
          @update-cart="updateCartItems"
          @proceed-checkout="proceedToCheckout"
        />
      </div>
      
      <!-- Additional Information -->
      <CartBenefits />
    </div>
    
    <!-- Footer -->
    <CartFooter 
      @navigate="handleNavigate"
    />
  </div>
</template>

<script>
import CartHeader from './CartHeader.vue';
import CartPageHeader from './CartPageHeader.vue';
import CartItems from './CartItems.vue';
import DiscountCode from './DiscountCode.vue';
import OrderSummary from './OrderSummary.vue';
import CartBenefits from './CartBenefits.vue';
import CartFooter from './CartFooter.vue';
import api from '@/utils/api';
import { mapGetters } from 'vuex';

export default {
  name: 'CartPage',
  components: {
    CartHeader,
    CartPageHeader,
    CartItems,
    DiscountCode,
    OrderSummary,
    CartBenefits,
    CartFooter
  },
  inject: ['cartItems', 'updateCart', 'proceedCheckout'],
  data() {
    return {
      appliedDiscount: 0,
      selectedShipping: 'standard',
      cart: null,
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'cartItemCount']),
    currentCartItems() {
      return this.cart ? this.cart.detalles_carrito : [];
    },
    totalItems() {
      return this.currentCartItems.reduce((total, item) => total + item.cantidad, 0);
    },
    subtotal() {
      // Usar subtotal_carrito del backend para el subtotal, con fallback a 0
      return this.cart && this.cart.subtotal_carrito !== null
        ? parseFloat(this.cart.subtotal_carrito)
        : 0;
    },
    shipping() {
      return this.selectedShipping === 'express' ? 15.00 : 0;
    },
    totalDiscount() {
      return this.cart && this.cart.descuento_carrito !== null ? parseFloat(this.cart.descuento_carrito) : 0;
    },
    totalIva() {
      return this.cart && this.cart.iva_carrito !== null ? parseFloat(this.cart.iva_carrito) : 0;
    },
    total() {
      return this.cart && this.cart.total_carrito !== null ? parseFloat(this.cart.total_carrito) : 0;
    }
  },
  created() {
    this.fetchCartItems();
  },
  methods: {
    async fetchCartItems() {
      if (!this.isAuthenticated) {
        console.log('Usuario no autenticado, no se puede cargar el carrito.');
        this.cart = null;
        return;
      }
      try {
        const response = await api.get('/mi-carrito/obtener/');
        this.cart = response.data;
        console.log('Carrito cargado:', this.cart);
        // Después de cargar el carrito, actualizamos el conteo en Vuex
        this.$store.commit('SET_CART_ITEM_COUNT', this.cart.detalles_carrito.reduce((total, item) => total + item.cantidad, 0));
      } catch (error) {
        console.error('Error al cargar el carrito:', error);
        this.cart = null;
        this.showNotification('Error al cargar el carrito.', 'error');
        this.$store.commit('SET_CART_ITEM_COUNT', 0); // Resetear conteo en caso de error
      }
    },
    async increaseQuantity(productSku) {
      const item = this.currentCartItems.find(i => i.producto.SKU === productSku);
      if (!item) return;
      const newQuantity = item.cantidad + 1;
      try {
        await api.post('/mi-carrito-detalles/', { producto_sku: productSku, cantidad: newQuantity });
        this.showNotification('Cantidad actualizada correctamente.', 'success');
        await this.fetchCartItems();
      } catch (error) {
        console.error('Error al aumentar la cantidad:', error);
        this.showNotification('Error al aumentar la cantidad.', 'error');
      }
    },
    async decreaseQuantity(productSku) {
      const item = this.currentCartItems.find(i => i.producto.SKU === productSku);
      if (!item || item.cantidad <= 1) {
        this.showNotification('La cantidad no puede ser menor a 1.', 'error');
        return;
      }
      const newQuantity = item.cantidad - 1;
      try {
        await api.post('/mi-carrito-detalles/', { producto_sku: productSku, cantidad: newQuantity });
        this.showNotification('Cantidad actualizada correctamente.', 'success');
        await this.fetchCartItems();
      } catch (error) {
        console.error('Error al disminuir la cantidad:', error);
        this.showNotification('Error al disminuir la cantidad.', 'error');
      }
    },
    async removeItem(productSku) {
      try {
        await api.delete(`/mi-carrito-detalles/${productSku}/`);
        this.showNotification('Producto eliminado del carrito.', 'success');
        await this.fetchCartItems(); // Recargar el carrito para actualizar la UI
      } catch (error) {
        console.error('Error al eliminar producto del carrito:', error);
        this.showNotification('Error al eliminar producto del carrito.', 'error');
      }
    },
    applyDiscount(code) {
      if (code === 'SAVE10') {
        this.appliedDiscount = 10;
        this.showNotification('Descuento del 10% aplicado');
      } else if (code === 'SAVE20') {
        this.appliedDiscount = 20;
        this.showNotification('Descuento del 20% aplicado');
      } else {
        this.appliedDiscount = 0;
        this.showNotification('Código de descuento inválido', 'error');
      }
    },
    updateCartItems() {
      this.fetchCartItems();
      this.showNotification('Carrito actualizado correctamente');
    },
    proceedToCheckout() {
      if (!this.cart || !this.cart.detalles_carrito || this.cart.detalles_carrito.length === 0) {
        this.showNotification('Tu carrito está vacío. Agrega productos antes de proceder al pago.', 'error');
        return;
      }

      const validItems = this.currentCartItems.filter(item => item.producto && item.producto.nombre && item.precio_unitario);
      if (validItems.length === 0) {
        this.showNotification('Error: Los productos en el carrito no tienen información válida.', 'error');
        return;
      }

      const checkoutData = {
        items: validItems.map(item => ({
          sku: item.producto.SKU,
          name: item.producto.nombre,
          quantity: item.cantidad,
          price: parseFloat(item.precio_unitario),
        })),
        totals: {
          subtotal: this.subtotal,
          shipping: this.shipping,
          totalDiscount: this.totalDiscount,
          totalIva: this.totalIva,
          total: this.total
        }
      };
      
      try {
        if (this.proceedCheckout) {
          this.proceedCheckout(checkoutData);
        }
        this.$nextTick(() => {
          this.$router.push('/checkout');
        });
      } catch (error) {
        console.error('Error al proceder al checkout:', error);
        this.showNotification('Error al procesar el checkout. Por favor intenta de nuevo.', 'error');
      }
    },
    handleNavigate(route) {
      if (route === 'home') {
        this.$router.push('/');
      }
      else if (route === 'products') {
        this.$router.push('/productos');
      }
      else if (route === 'offers') {
        this.$router.push('/ofertas');
      }
      else if (route === 'notebooks' || route === 'pens' || route === 'folders' || route === 'school') {
        this.$router.push('/productos');
      }
    },
    handleSearch(query) {
      this.$emit('search', query);
    },
    handleShippingChanged(value) {
      this.selectedShipping = value;
      this.$emit('shipping-changed', value);
    },
    handleSocial(platform) {
      console.log(`Redirigir a ${platform}`);
    },
    showNotification(message, type = 'success') {
      const notification = document.createElement('div');
      const bgColor = type === 'error' ? 'bg-red-600' : 'bg-green-600';
      notification.className = `fixed top-4 right-4 ${bgColor} text-white px-6 py-3 rounded-lg shadow-lg z-50 transition-all`;
      notification.textContent = message;

      document.body.appendChild(notification);

      setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
          if (document.body.contains(notification)) {
            document.body.removeChild(notification);
          }
        }, 300);
      }, 3000);
    }
  }
}
</script>

<style scoped>
.rounded-button {
  border-radius: 8px;
}

input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type="number"] {
  -moz-appearance: textfield;
  appearance: textfield;
}

</style>
