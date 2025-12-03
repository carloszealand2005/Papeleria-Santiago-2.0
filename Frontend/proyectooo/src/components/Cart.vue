<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <CartHeader 
      :cartCount="totalItems"
      @go-home="$emit('go-home')"
      @navigate="handleNavigate"
      @go-to-cart="$emit('go-to-cart')"
      @search="handleSearch"
    />
    
    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <!-- Cart Header -->
      <CartPageHeader 
        :itemCount="cartItems.length"
        @continue-shopping="$emit('continue-shopping')"
      />
      
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- Cart Items -->
        <div class="lg:col-span-2">
          <CartItems
            :cartItems="cartItems"
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
          @update-cart="updateCart"
          @proceed-checkout="proceedToCheckout"
        />
      </div>
      
      <!-- Additional Information -->
      <CartBenefits />
    </div>
    
    <!-- Footer -->
    <CartFooter 
      @navigate="handleNavigate"
      @social="handleSocial"
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
  props: {
    cartItems: {
      type: Array,
      default: () => [
        {
          id: 1,
          name: 'Cuaderno Universitario',
          description: 'Cuaderno de 100 hojas rayado espiral',
          price: 12.50,
          quantity: 2,
          image: 'https://readdy.ai/api/search-image?query=professional%20spiral%20notebook%20university%20style%20clean%20white%20background%20office%20supplies%20stationery%20product%20photography%20studio%20lighting%20minimal%20commercial%20style&width=200&height=200&seq=cart-notebook-1&orientation=squarish'
        },
        {
          id: 2,
          name: 'Set de Bolígrafos',
          description: 'Pack de 10 bolígrafos azules BIC',
          price: 8.75,
          quantity: 1,
          image: 'https://readdy.ai/api/search-image?query=professional%20blue%20ballpoint%20pens%20set%20office%20supplies%20clean%20white%20background%20stationery%20product%20photography%20studio%20lighting%20minimal%20commercial%20style&width=200&height=200&seq=cart-pens-1&orientation=squarish'
        },
        {
          id: 3,
          name: 'Archivador A4',
          description: 'Archivador de palanca tamaño A4',
          price: 15.99,
          quantity: 1,
          image: 'https://readdy.ai/api/search-image?query=professional%20office%20binder%20folder%20A4%20size%20clean%20white%20background%20office%20supplies%20stationery%20product%20photography%20studio%20lighting%20minimal%20commercial%20style&width=200&height=200&seq=cart-binder-1&orientation=squarish'
        }
      ]
    }
  },
  data() {
    return {
      appliedDiscount: 0,
      selectedShipping: 'standard'
    }
  },
  computed: {
    totalItems() {
      return this.cartItems.reduce((total, item) => total + item.quantity, 0);
    },
    subtotal() {
      return this.cartItems.reduce((total, item) => total + (item.price * item.quantity), 0);
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
      const updatedItems = this.cartItems.map(item => {
        if (item.id === itemId) {
          return { ...item, quantity: item.quantity + 1 };
        }
        return item;
      });
      this.$emit('cart-updated', updatedItems);
    },
    decreaseQuantity(itemId) {
      const updatedItems = this.cartItems.map(item => {
        if (item.id === itemId && item.quantity > 1) {
          return { ...item, quantity: item.quantity - 1 };
        }
        return item;
      });
      this.$emit('cart-updated', updatedItems);
    },
    removeItem(itemId) {
      const updatedItems = this.cartItems.filter(item => item.id !== itemId);
      this.$emit('cart-updated', updatedItems);
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
    updateCart() {
      this.$emit('update-cart', this.cartItems);
      this.showNotification('Carrito actualizado correctamente');
    },
    proceedToCheckout() {
      this.$emit('proceed-checkout', {
        items: this.cartItems,
        totals: {
          subtotal: this.subtotal,
          shipping: this.shipping,
          taxes: this.taxes,
          discount: this.discountAmount,
          total: this.total
        }
      });
    },
    handleNavigate(route) {
      this.$emit('navigate', route);
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

