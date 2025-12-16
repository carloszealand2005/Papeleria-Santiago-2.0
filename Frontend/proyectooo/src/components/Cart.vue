<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <CartHeader 
      :cartCount="totalItems"
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
          :taxes="taxes"
          :discountAmount="discountAmount"
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
      selectedShipping: 'standard'
    }
  },
  computed: {
    currentCartItems() {
      return this.cartItems || [];
    },
    totalItems() {
      return this.currentCartItems.reduce((total, item) => total + item.quantity, 0);
    },
    subtotal() {
      return this.currentCartItems.reduce((total, item) => total + (item.price * item.quantity), 0);
    },
    shipping() {
      return this.selectedShipping === 'express' ? 15.00 : 0;
    },
    taxes() {
      return this.subtotal * 0.08;
    },
    discountAmount() {
      return this.subtotal * (this.appliedDiscount / 100);
    },
    total() {
      return this.subtotal + this.shipping + this.taxes - this.discountAmount;
    }
  },
  methods: {
    increaseQuantity(itemId) {
      const updatedItems = this.currentCartItems.map(item => {
        if (item.id === itemId) {
          return { ...item, quantity: item.quantity + 1 };
        }
        return item;
      });
      if (this.updateCart) {
        this.updateCart(updatedItems);
      }
    },
    decreaseQuantity(itemId) {
      const updatedItems = this.currentCartItems.map(item => {
        if (item.id === itemId && item.quantity > 1) {
          return { ...item, quantity: item.quantity - 1 };
        }
        return item;
      });
      if (this.updateCart) {
        this.updateCart(updatedItems);
      }
    },
    removeItem(itemId) {
      const updatedItems = this.currentCartItems.filter(item => item.id !== itemId);
      if (this.updateCart) {
        this.updateCart(updatedItems);
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
      if (this.updateCart) {
        this.updateCart(this.currentCartItems);
      }
      this.showNotification('Carrito actualizado correctamente');
    },
    proceedToCheckout() {
      // Validar que el carrito no esté vacío
      if (!this.currentCartItems || this.currentCartItems.length === 0) {
        this.showNotification('Tu carrito está vacío. Agrega productos antes de proceder al pago.', 'error');
        return;
      }

      // Validar que todos los items tengan los datos necesarios
      const validItems = this.currentCartItems.filter(item => item.name && item.price);
      if (validItems.length === 0) {
        this.showNotification('Error: Los productos en el carrito no tienen información válida.', 'error');
        return;
      }

      const checkoutData = {
        items: validItems,
        totals: {
          subtotal: this.subtotal,
          shipping: this.shipping,
          taxes: this.taxes,
          discount: this.discountAmount,
          total: this.total
        }
      };
      
      try {
        // Preparar los datos primero
        if (this.proceedCheckout) {
          this.proceedCheckout(checkoutData);
        }
        
        // Esperar un momento para que los datos se actualicen antes de navegar
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
      } else if (route === 'products') {
        this.$router.push('/productos');
      } else if (route === 'offers') {
        this.$router.push('/ofertas');
      } else if (route === 'notebooks' || route === 'pens' || route === 'folders' || route === 'school') {
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
      // Implementar redirección a redes sociales
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
}
</style>

