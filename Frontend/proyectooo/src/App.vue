<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Vista de Login -->
    <LoginPage v-if="currentView === 'login'" @go-to-home="currentView = 'home'" />
    
    <!-- Vista de Carrito -->
    <CartPage 
      v-else-if="currentView === 'cart'"
      :cartItems="cartItems"
      @go-home="currentView = 'home'"
      @continue-shopping="currentView = 'home'"
      @cart-updated="handleCartUpdate"
      @proceed-checkout="handleCheckout"
    />
    
    <!-- Vista de Checkout (Pago) -->
    <CheckoutPage
      v-else-if="currentView === 'checkout'"
      :orderItems="checkoutOrderItems"
      :totals="checkoutTotals"
      @go-back="currentView = 'cart'"
      @go-home="currentView = 'home'"
      @complete-order="handleCompleteOrder"
    />
    
    <!-- Vista de Factura -->
    <ReceiptPage
      v-else-if="currentView === 'receipt'"
      :invoiceData="receiptData.invoiceData"
      :customerData="receiptData.customerData"
      :orderItems="receiptData.orderItems"
      :totals="receiptData.totals"
      :paymentInfo="receiptData.paymentInfo"
      :deliveryInfo="receiptData.deliveryInfo"
      @go-home="currentView = 'home'"
    />
    
    <!-- Vista de Ofertas -->
    <OffersPage
      v-else-if="currentView === 'offers'"
      :cartCount="totalCartItems"
      @go-to-cart="currentView = 'cart'"
      @add-to-cart="handleAddToCartFromOffers"
      @search="handleSearch"
      @subscribe-newsletter="handleSubscribeNewsletter"
    />
    
    <!-- Vista de Productos -->
    <ProductsPage
      v-else-if="currentView === 'products'"
      :cartCount="totalCartItems"
      @go-to-cart="currentView = 'cart'"
      @add-to-cart="handleAddToCartFromProducts"
      @search="handleSearch"
      @subscribe-newsletter="handleSubscribeNewsletter"
    />
    
    <!-- Vista Principal (Home) -->
    <template v-else>
      <Header 
        @go-to-login="currentView = 'login'"
        @go-to-cart="currentView = 'cart'"
        @go-to-home="currentView = 'home'"
        @go-to-offers="currentView = 'offers'"
        @go-to-products="currentView = 'products'"
        :cartCount="totalCartItems"
      />
    <Hero />
    <Categorias 
      :mainCategories="mainCategories" 
      :subCategories="subCategories" 
      @select-category="selectCategory" 
    />
    <Novedades :featuredProducts="featuredProducts" />
      <WhyChooseUs />
      <Newsletter />
    <Footer />
    </template>
  </div>
</template>

<script>
// Importa los componentes de la carpeta src/components/
import Header from './components/Header.vue';
import Hero from './components/Hero.vue';
import Categorias from './components/categorias.vue';
import Novedades from './components/Novedades.vue';
import WhyChooseUs from './components/WhyChooseUs.vue';
import Newsletter from './components/Newsletter.vue';
import Footer from './components/Footer.vue';
import LoginPage from './components/Login.vue';
import CartPage from './components/Cart.vue';
import CheckoutPage from './components/Checkout.vue';
import ReceiptPage from './components/Receipt.vue';
import OffersPage from './components/Offers.vue';
import ProductsPage from './components/Products.vue';

export default {
  name: 'App',
  components: {
    Header,
    Hero,
    Categorias,
    Novedades,
    WhyChooseUs,
    Newsletter,
    Footer,
    LoginPage,
    CartPage,
    CheckoutPage,
    ReceiptPage,
    OffersPage,
    ProductsPage
  },
  data() {
    return {
      currentView: 'home', // 'home', 'login', 'cart', 'checkout', 'receipt', 'offers' o 'products'
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
      // ** DATOS DE CATEGORÍAS PRINCIPALES **
      mainCategories: [
        {
          id: 1,
          name: 'Oficina',
          description: 'Todo para tu espacio profesional',
          icon: 'fas fa-briefcase',
          image: 'https://readdy.ai/api/search-image?query=modern%20office%20workspace%20with%20elegant%20stationery%20supplies%20notebooks%20and%20pens%20on%20wooden%20desk%20professional%20minimalist%20setup&width=400&height=250&seq=cat-office-01&orientation=landscape'
        },
        {
          id: 2,
          name: 'Escolar',
          description: 'Materiales para estudiantes',
          icon: 'fas fa-graduation-cap',
          image: 'https://readdy.ai/api/search-image?query=colorful%20school%20supplies%20with%20notebooks%20pencils%20rulers%20and%20backpack%20on%20bright%20background%20student%20materials&width=400&height=250&seq=cat-school-01&orientation=landscape'
        },
        {
          id: 3,
          name: 'Arte y Diseño',
          description: 'Creatividad sin límites',
          icon: 'fas fa-palette',
          image: 'https://readdy.ai/api/search-image?query=artistic%20supplies%20with%20professional%20colored%20pencils%20markers%20sketchbooks%20and%20paint%20tubes%20on%20creative%20workspace&width=400&height=250&seq=cat-art-01&orientation=landscape'
        }
      ],
      // ** DATOS DE SUBCATEGORÍAS **
      subCategories: [
        { id: 11, name: 'Cuadernos', icon: 'fas fa-book' },
        { id: 12, name: 'Bolígrafos', icon: 'fas fa-pen' },
        { id: 13, name: 'Papel', icon: 'fas fa-file-alt' },
        { id: 14, name: 'Carpetas', icon: 'fas fa-folder' },
        { id: 15, name: 'Calculadoras', icon: 'fas fa-calculator' },
        { id: 16, name: 'Adhesivos', icon: 'fas fa-tape' }
      ],
      // ** DATOS DE PRODUCTOS DESTACADOS **
      featuredProducts: [
        {
          id: 1,
          name: 'Cuaderno Premium A4',
          category: 'Cuadernos',
          price: '24.99',
          originalPrice: '29.99',
          isNew: true,
          discount: 17,
          image: 'https://readdy.ai/api/search-image?query=premium%20spiral%20notebook%20with%20elegant%20cover%20design%20on%20clean%20white%20background%20professional%20product%20photography%20high%20quality&width=300&height=300&seq=prod-new-01&orientation=squarish'
        },
        {
          id: 2,
          name: 'Set Bolígrafos Gel',
          category: 'Escritura',
          price: '18.50',
          isNew: true,
          image: 'https://readdy.ai/api/search-image?query=elegant%20gel%20pen%20set%20in%20professional%20packaging%20with%20multiple%20colors%20on%20clean%20white%20background%20product%20photography&width=300&height=300&seq=prod-new-02&orientation=squarish'
        },
        {
          id: 3,
          name: 'Organizador Escritorio',
          category: 'Organización',
          price: '45.00',
          originalPrice: '60.00',
          discount: 25,
          image: 'https://readdy.ai/api/search-image?query=modern%20desk%20organizer%20with%20multiple%20compartments%20for%20office%20supplies%20clean%20minimalist%20design%20professional%20photography&width=300&height=300&seq=prod-new-03&orientation=squarish'
        },
        {
          id: 4,
          name: 'Kit Marcadores Arte',
          category: 'Arte',
          price: '89.99',
          isNew: true,
          image: 'https://readdy.ai/api/search-image?query=professional%20art%20marker%20set%20in%20elegant%20case%20with%20vibrant%20colors%20for%20artists%20clean%20white%20background%20product%20photography&width=300&height=300&seq=prod-new-04&orientation=squarish'
        }
      ]
    };
  },
  computed: {
    totalCartItems() {
      return this.cartItems.reduce((total, item) => total + item.quantity, 0);
    }
  },
  methods: {
    selectCategory(category) {
      console.log('Categoría seleccionada:', category.name);
      this.showNotification(`Navegando a ${category.name}`);
    },
    handleCartUpdate(items) {
      this.cartItems = items;
      this.showNotification('Carrito actualizado');
    },
    handleCheckout(data) {
      console.log('Proceder al checkout:', data);
      
      // Preparar datos para el checkout
      this.prepareCheckoutData(data);
      
      // Cambiar a la vista de checkout
      this.currentView = 'checkout';
    },
    prepareCheckoutData(checkoutData) {
      // Convertir items del carrito al formato del checkout
      this.checkoutOrderItems = checkoutData.items.map(item => ({
        name: item.name,
        quantity: item.quantity,
        price: item.price,
        image: item.image
      }));
      
      // Preparar totales
      const subtotal = checkoutData.totals.subtotal;
      const tax = checkoutData.totals.taxes || (subtotal * 0.16);
      const total = checkoutData.totals.total;
      
      this.checkoutTotals = {
        subtotal: subtotal,
        tax: tax,
        total: total
      };
    },
    handleAddToCartFromOffers(product) {
      // Buscar si el producto ya está en el carrito
      const existingItem = this.cartItems.find(item => item.id === product.id);
      
      if (existingItem) {
        // Si existe, incrementar cantidad
        const updatedItems = this.cartItems.map(item => 
          item.id === product.id 
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
        this.cartItems = updatedItems;
      } else {
        // Si no existe, agregar nuevo item
        const newItem = {
          id: product.id,
          name: product.name,
          price: product.salePrice || product.price,
          quantity: 1,
          image: product.image
        };
        this.cartItems = [...this.cartItems, newItem];
      }
      
      this.showNotification(`${product.name} agregado al carrito`);
    },
    handleAddToCartFromProducts(product) {
      // Buscar si el producto ya está en el carrito
      const existingItem = this.cartItems.find(item => item.id === product.id);
      
      if (existingItem) {
        // Si existe, incrementar cantidad
        const updatedItems = this.cartItems.map(item => 
          item.id === product.id 
            ? { ...item, quantity: item.quantity + 1 }
            : item
        );
        this.cartItems = updatedItems;
      } else {
        // Si no existe, agregar nuevo item
        const newItem = {
          id: product.id,
          name: product.name,
          price: product.price || product.originalPrice || product.salePrice,
          quantity: 1,
          image: product.image
        };
        this.cartItems = [...this.cartItems, newItem];
      }
      
      this.showNotification(`${product.name} agregado al carrito`);
    },
    handleSearch(query) {
      console.log('Buscando:', query);
      // Aquí puedes implementar la lógica de búsqueda
    },
    handleSubscribeNewsletter(email) {
      console.log('Suscribiendo email:', email);
      this.showNotification('¡Gracias por suscribirte!');
    },
    handleCompleteOrder(orderData) {
      console.log('Orden completada:', orderData);
      
      // Preparar datos para la factura
      this.prepareReceiptData(orderData);
      
      // Cambiar a la vista de factura
      this.currentView = 'receipt';
      
      this.showNotification('¡Pedido realizado con éxito!');
    },
    prepareReceiptData(orderData) {
      // Convertir items del checkout al formato de la factura
      const orderItems = orderData.orderItems.map(item => ({
        name: item.name,
        quantity: item.quantity,
        price: item.price,
        total: item.price * item.quantity
      }));
      
      // Calcular totales
      const subtotal = orderData.totals.subtotal;
      const discount = orderData.totals.discount || 0;
      const tax = orderData.totals.tax || (subtotal * 0.19);
      const total = orderData.totals.total;
      
      // Generar número de factura
      const invoiceNumber = 'FAC-B-' + new Date().getTime().toString().slice(-8);
      const invoiceDate = new Date().toLocaleDateString('es-CO');
      
      // Preparar datos de la factura
      this.receiptData = {
        invoiceData: {
          number: invoiceNumber,
          date: invoiceDate
        },
        customerData: {
          name: orderData.billingInfo.fullName || 'Cliente',
          id: '1.059.885.432', // Esto debería venir del usuario logueado
          email: 'cliente@email.com', // Esto debería venir del usuario logueado
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
        daysToAdd = 0; // Recogida en tienda
      }
      
      const deliveryDate = new Date(now.getTime() + daysToAdd * 24 * 60 * 60 * 1000);
      return deliveryDate.toLocaleDateString('es-CO');
    },
    showNotification(message) {
      const notification = document.createElement('div');
      notification.className = 'fixed top-4 right-4 bg-blue-600 text-white px-6 py-3 rounded-lg shadow-lg z-50 transition-all';
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
/* Pega aquí el bloque de estilos (media queries, etc.) que estaba al final del archivo original */
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
/* Receipt specific styles */
.receipt-container {
background: white;
}
/* Table styles for better readability */
table {
border-collapse: collapse;
}
table th,
table td {
border: 1px solid #e5e5e5;
}
/* Hover effects for better UX */
tr:hover {
background-color: #f9f9f9;
}
/* Responsive design */
@media (max-width: 768px) {
.grid-cols-2 {
grid-template-columns: 1fr;
}
.text-3xl {
font-size: 1.5rem;
}
.text-2xl {
font-size: 1.25rem;
}
.space-x-4 {
flex-direction: column;
align-items: flex-start;
}
.space-x-4 > * {
margin-right: 0 !important;
margin-bottom: 0.5rem;
}
.overflow-x-auto {
overflow-x: scroll;
}
table {
min-width: 600px;
}
}
</style>