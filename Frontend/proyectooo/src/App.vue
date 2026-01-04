<template>
  <div class="min-h-screen bg-gray-50">
    <GlobalHeader /> <!-- Nuevo: La barra superior global -->
    <!-- Botón de Logout Temporal -->
    <div v-if="isAuthenticated" class="fixed top-4 right-4 z-50">
      <button @click="logout" class="bg-red-500 hover:bg-red-600 text-white font-bold py-2 px-4 rounded shadow-lg transition duration-200">
        Cerrar Sesión
      </button>
    </div>
    <router-view />
  </div>
</template>

<script>
import './assets/tailwind.css'
import { mapGetters, mapActions } from 'vuex';
import api from './utils/api';
import GlobalHeader from './components/GlobalHeader.vue'; // Nuevo: Importar GlobalHeader

export default {
  name: 'App',
  components: {
    GlobalHeader // Nuevo: Registrar GlobalHeader
  },
  data() {
    return {
      selectedProduct: null,
      checkoutOrderItems: [],
      checkoutTotals: {
        subtotal: 0,
        tax: 0,
        total: 0
      },
      receiptData: {
        invoiceData: {
          number: '',
          date: ''
        },
        customerData: {
          name: '',
          id: '',
          email: '',
          address: ''
        },
        orderItems: [],
        totals: {
          subtotal: 0,
          discount: 0,
          tax: 0,
          total: 0
        },
        paymentInfo: {
          method: '',
          status: 'Pagado',
          reference: ''
        },
        deliveryInfo: {
          type: '',
          date: '',
          address: ''
        }
      },
      cartItems: [
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
      ],
      mainCategories: [
        {
          id: 1,
          name: 'Oficina',
          description: 'Todo para tu espacio profesional',
          icon: 'fas fa-briefcase',
          image: 'https://readdy.ai/api/search-image?query=modern%20office%20workspace%20con%20elegant%20stationery%20supplies%20notebooks%20and%20pens%20on%20wooden%20desk%20professional%20minimalist%20setup&width=400&height=250&seq=cat-office-01&orientation=landscape'
        },
        {
          id: 2,
          name: 'Escolar',
          description: 'Materiales para estudiantes',
          icon: 'fas fa-graduation-cap',
          image: 'https://readdy.ai/api/search-image?query=colorful%20school%20supplies%20con%20notebooks%20pencils%20rulers%20and%20backpack%20on%20bright%20background%20student%20materials&width=400&height=250&seq=cat-school-01&orientation=landscape'
        },
        {
          id: 3,
          name: 'Arte y Diseño',
          description: 'Creatividad sin límites',
          icon: 'fas fa-palette',
          image: 'https://readdy.ai/api/search-image?query=artistic%20supplies%20con%20professional%20colored%20pencils%20markers%20sketchbooks%20and%20paint%20tubes%20on%20creative%20workspace&width=400&height=250&seq=cat-art-01&orientation=landscape'
        }
      ],
      subCategories: [
        { id: 11, name: 'Cuadernos', icon: 'fas fa-book' },
        { id: 12, name: 'Bolígrafos', icon: 'fas fa-pen' },
        { id: 13, name: 'Papel', icon: 'fas fa-file-alt' },
        { id: 14, name: 'Carpetas', icon: 'fas fa-folder' },
        { id: 15, name: 'Calculadoras', icon: 'fas fa-calculator' },
        { id: 16, name: 'Adhesivos', icon: 'fas fa-tape' }
      ],
      featuredProducts: [
        {
          id: 1,
          name: 'Cuaderno Premium A4',
          category: 'Cuadernos',
          price: '24.99',
          originalPrice: '29.99',
          isNew: true,
          discount: 17,
          image: 'https://readdy.ai/api/search-image?query=premium%20spiral%20notebook%20con%20elegant%20cover%20design%20on%20clean%20white%20background%20professional%20product%20photography%20high%20quality&width=300&height=300&seq=prod-new-01&orientation=squarish'
        },
        {
          id: 2,
          name: 'Set Bolígrafos Gel',
          category: 'Escritura',
          price: '18.50',
          isNew: true,
          image: 'https://readdy.ai/api/search-image?query=elegant%20gel%20pen%20set%20in%20professional%20packaging%20con%20multiple%20colors%20on%20clean%20white%20background%20product%20photography&width=300&height=300&seq=prod-new-02&orientation=squarish'
        },
        {
          id: 3,
          name: 'Organizador Escritorio',
          category: 'Organización',
          price: '45.00',
          originalPrice: '60.00',
          discount: 25,
          image: 'https://readdy.ai/api/search-image?query=modern%20desk%20organizer%20con%20multiple%20compartments%20for%20office%20supplies%20clean%20minimalist%20design%20professional%20photography&width=300&height=300&seq=prod-new-03&orientation=squarish'
        },
        {
          id: 4,
          name: 'Kit Marcadores Arte',
          category: 'Arte',
          price: '89.99',
          isNew: true,
          image: 'https://readdy.ai/api/search-image?query=professional%20art%20marker%20set%20in%20elegant%20case%20con%20vibrant%20colors%20for%20artists%20clean%20white%20background%20product%20photography&width=300&height=300&seq=prod-new-04&orientation=squarish'
        }
      ],
      // localCartItemCount: 0, // Eliminado, ya que el conteo viene de Vuex
    };
  },
  provide() {
    return {
      cartItems: this.cartItems,
      // cartItemCount: this.cartItemCount, // Eliminado, ya que el conteo viene de Vuex
      mainCategories: this.mainCategories,
      subCategories: this.subCategories,
      featuredProducts: this.featuredProducts,
      checkoutOrderItems: this.checkoutOrderItems,
      checkoutTotals: this.checkoutTotals,
      receiptData: this.receiptData,
      selectedProduct: this.selectedProduct,
      addToCart: this.handleAddToCart,
      updateCart: this.handleCartUpdate,
      proceedCheckout: this.handleCheckout,
      completeOrderHandler: this.handleCompleteOrder,
      selectProduct: this.handleSelectProduct
    };
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'cartItemCount']), // Mapeamos los getters de Vuex
    // cartItemCount() { // Eliminado, ya que el conteo viene de Vuex
    //   return this.localCartItemCount; 
    // }
  },
  watch: {
    isAuthenticated(newVal) {
      if (newVal) {
        this.fetchCartItemCount();
      } else {
        this.$store.commit('SET_CART_ITEM_COUNT', 0); // Reseteamos el conteo en Vuex
      }
    }
  },
  created() {
    if (this.isAuthenticated) {
      this.fetchCartItemCount();
    }
  },
  methods: {
    ...mapActions(['logout']), // Mapeamos la acción 'logout' de Vuex
    async fetchCartItemCount() {
      try {
        const response = await api.get('/mi-carrito/conteo/');
        this.$store.commit('SET_CART_ITEM_COUNT', response.data.conteo_items_carrito);
      } catch (error) {
        console.error('App.vue - Error al obtener el conteo del carrito:', error);
        this.$store.commit('SET_CART_ITEM_COUNT', 0);
      }
    },
    handleCartUpdate(items) {
      this.cartItems = items;
      this.showNotification('Carrito actualizado');
      this.fetchCartItemCount(); // Actualizar el conteo después de una actualización
    },
    async handleAddToCart(product) {
      if (!this.isAuthenticated) {
        this.showNotification('Debes iniciar sesión para añadir productos al carrito.', 'error');
        return;
      }

      const producto_sku = product.sku; // Usar product.sku que es el identificador del backend
      const cantidad = product.quantity || 1; // Asume 1 si no se especifica

      try {
        await api.post(`/mi-carrito-detalles/`, {
          producto_sku: producto_sku,
          cantidad: cantidad
        });
        this.showNotification(`"${product.name}" añadido al carrito.`, 'success');
        this.fetchCartItemCount(); // Actualizar el conteo después de añadir al carrito
      } catch (error) {
        console.error('Error al añadir producto al carrito:', error);
        this.showNotification('Error al añadir producto al carrito.', 'error');
      }
    },
    handleCheckout(data) {
      try {
        // Validar que haya datos
        if (!data || !data.items || data.items.length === 0) {
          console.error('Error: No hay items en el checkout');
          return;
        }
        
        this.prepareCheckoutData(data);
        // No navegar aquí porque Cart.vue ya lo hace
        // this.$router.push('/checkout');
      } catch (error) {
        console.error('Error en handleCheckout:', error);
      }
    },
    prepareCheckoutData(checkoutData) {
      try {
        this.checkoutOrderItems = checkoutData.items.map(item => ({
          name: item.name || 'Producto sin nombre',
          quantity: item.quantity || 1,
          price: item.price || 0,
          image: item.image || ''
        }));
        
        const subtotal = checkoutData.totals?.subtotal || 0;
        const tax = checkoutData.totals?.taxes || (subtotal * 0.16);
        const total = checkoutData.totals?.total || (subtotal + tax);
        
        this.checkoutTotals = {
          subtotal: subtotal,
          tax: tax,
          total: total
        };
      } catch (error) {
        console.error('Error en prepareCheckoutData:', error);
        throw error;
      }
    },
    handleCompleteOrder(orderData) {
      const invoiceNumber = 'INV-' + Date.now();
      const invoiceDate = new Date().toLocaleDateString('es-CO');
      
      const orderItems = orderData.items.map(item => ({
        name: item.name,
        quantity: item.quantity,
        price: item.price,
        subtotal: item.price * item.quantity
      }));
      
      const subtotal = orderItems.reduce((sum, item) => sum + item.subtotal, 0);
      const discount = orderData.discount || 0;
      const tax = (subtotal - discount) * 0.16;
      const total = subtotal - discount + tax;
      
      this.receiptData = {
        invoiceData: {
          number: invoiceNumber,
          date: invoiceDate
        },
        customerData: {
          name: orderData.billingInfo.fullName || 'Cliente',
          id: '1.059.885.432',
          email: 'cliente@email.com',
          address: orderData.billingInfo.address || 'No especificada'
        },
        orderItems: orderItems,
        totals: {
          subtotal: subtotal,
          discount: discount,
          tax: tax,
          total: total
        },
        paymentInfo: {
          method: this.getPaymentMethodName(orderData.payment),
          status: 'Pagado',
          reference: 'TXN-' + Math.random().toString(36).substr(2, 9).toUpperCase()
        },
        deliveryInfo: {
          type: this.getShippingTypeName(orderData.shipping),
          date: this.calculateDeliveryDate(orderData.shipping),
          address: orderData.billingInfo.address || 'No especificada'
        }
      };
      
      this.$router.push('/factura');
    },
    handleSelectProduct(product) {
      const productWithDetails = {
        ...product,
        sku: product.sku || `PROD-${product.id}`,
        rating: product.rating || 4,
        reviewCount: product.reviewCount || 0,
        description: product.description || 'Descripción del producto',
        features: product.features || [
          'Alta calidad',
          'Diseño moderno',
          'Garantía incluida'
        ],
        mainImage: product.image || product.mainImage,
        gallery: product.gallery || [
          product.image,
          product.image,
          product.image,
          product.image
        ],
        originalPrice: product.originalPrice || null,
        discount: product.discount || null
      };
      
      this.selectedProduct = productWithDetails;
      this.$router.push({ name: 'ProductDetails', params: { id: product.id } });
    },
    getPaymentMethodName(payment) {
      const methods = {
        'card': 'Tarjeta de Crédito',
        'paypal': 'PayPal',
        'transfer': 'Transferencia Bancaria'
      };
      return methods[payment] || 'Tarjeta de Crédito';
    },
    getShippingTypeName(shipping) {
      const types = {
        'standard': 'Domicilio - Estándar',
        'express': 'Domicilio - Express',
        'pickup': 'Recogida en Tienda'
      };
      return types[shipping] || 'Domicilio';
    },
    calculateDeliveryDate(shipping) {
      const now = new Date();
      let daysToAdd = 0;
      
      if (shipping === 'express') {
        daysToAdd = 2;
      } else if (shipping === 'standard') {
        daysToAdd = 5;
      } else {
        daysToAdd = 0;
      }
      
      const deliveryDate = new Date(now.getTime() + daysToAdd * 24 * 60 * 60 * 1000);
      return deliveryDate.toLocaleDateString('es-CO');
    },
    showNotification(message, type = 'success') {
      const notification = document.createElement('div');
      const bgColor = type === 'error' ? 'bg-red-600' : 'bg-green-600'; // Default to green for success
      notification.className = `fixed top-4 right-4 ${bgColor} text-white px-6 py-3 rounded-lg shadow-lg z-50 transition-all`;
      notification.textContent = message;
      document.body.appendChild(notification);
      setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
          document.body.removeChild(notification);
        }, 300);
      }, 3000);
    }
  }
};
</script>

<style scoped>
@media print {
  body {
    margin: 0;
    padding: 0;
  }
  .max-w-4xl {
    max-width: 100%;
    margin: 0;
    padding: 0;
  }
  .bg-gray-100 {
    background: white !important;
  }
  .shadow-lg {
    box-shadow: none !important;
  }
  button {
    display: none !important;
  }
}
</style>
