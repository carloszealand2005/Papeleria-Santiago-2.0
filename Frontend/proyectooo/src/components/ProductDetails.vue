<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <!-- <ProductDetailsHeader
      @search="handleSearch"
    /> -->
    
    <ProductDetailsContent
      :product="product"
      :isAuthenticated="isAuthenticated"
      @add-to-cart="handleAddToCart"
      @select-product="handleSelectProduct"
      @prompt-login-for-favorites="showAuthPromptModal = true"
    />

    <!-- Auth Prompt Modal -->
    <AuthPromptModal 
      :showModal="showAuthPromptModal"
      @close="closeAuthPromptModal"
      @go-to-register="goToRegisterFromModal"
      @go-to-login="goToLoginFromModal"
      @continue-shopping="continueShoppingFromModal"
    />
  </div>
</template>

<script>
// import ProductDetailsHeader from './ProductDetailsHeader.vue'; // Eliminado
import ProductDetailsContent from './ProductDetailsContent.vue';
import AuthPromptModal from './AuthPromptModal.vue'; 
import api from '@/utils/api';
import { mapGetters } from 'vuex';

export default {
  name: 'ProductDetailsPage',
  components: {
    // ProductDetailsHeader, // Eliminado
    ProductDetailsContent,
    AuthPromptModal 
  },
  inject: ['addToCart', 'selectProduct'],
  computed: {
    ...mapGetters(['isAuthenticated', 'cartItemCount']),
  },
  data() {
    return {
      product: null,
      showAuthPromptModal: false, 
    };
  },
  created() {
    this.fetchProductDetails();
  },
  watch: {
    '$route.params.id': {
      immediate: true,
      handler(newId) {
        if (newId) {
          this.fetchProductDetails();
        }
      }
    }
  },
  methods: {
    fetchProductDetails() {
      const sku = this.$route.params.id;
      if (!sku) {
        console.error('SKU not found in route params.');
        return;
      }
      api.get(`/productos/?SKU=${sku}`)
        .then(response => {
          if (response.data && response.data.length > 0) {
            const productData = response.data[0];
            this.product = {
              id: productData.SKU,
              name: productData.nombre,
              description: productData.descripcion,
              originalPrice: parseFloat(productData.pvp),
              salePrice: parseFloat(productData.precio_con_descuento_publico), 
              discount: parseFloat(productData.descuento_publico),
              iva: parseFloat(productData.iva),
              precio_con_iva_publico: parseFloat(productData.precio_con_iva_publico),
              category: productData.categoria,
              mainImage: productData.imagen_url,
              gallery: [
                productData.imagen_url,
                productData.imagen_url2,
                productData.imagen_url3,
                productData.imagen_url4,
              ].filter(url => url !== null && url !== ''),
              features: [
                productData.caracteristica1,
                productData.caracteristica2,
                productData.caracteristica3,
                productData.caracteristica4,
                productData.caracteristica5,
              ].filter(feature => feature !== null && feature !== ''),
              brand: productData.marca,
            };
          } else {
            console.warn('No product data found for SKU:', sku);
            this.product = null;
          }
        })
        .catch(error => {
          console.error('Error fetching product details:', error);
          this.product = null;
        });
    },
    async handleAddToCart(cartItem) {
      if (!this.isAuthenticated) {
        this.showAuthPromptModal = true;
        return;
      }

      const { id: producto_sku, quantity } = cartItem;

      try {
        await api.post(`/mi-carrito-detalles/`, {
          producto_sku: producto_sku,
          cantidad: quantity
        });
        this.showNotification(`"${cartItem.name}" añadido al carrito.`, 'success');
        this.$store.commit('SET_CART_ITEM_COUNT', this.cartItemCount + 1);
      } catch (error) {
        console.error('Error al añadir producto al carrito:', error);
        this.showNotification('Error al añadir producto al carrito.', 'error');
      }
    },
    handleSelectProduct(product) {
      if (this.selectProduct) {
        this.selectProduct(product);
      }
    },
    handleSearch(query) {
      this.$router.push({ path: '/productos', query: { search: query } });
    },
    // Métodos para manejar los eventos del AuthPromptModal
    closeAuthPromptModal() {
      this.showAuthPromptModal = false;
    },
    goToRegisterFromModal() {
      this.showAuthPromptModal = false;
      this.$router.push('/registro');
    },
    goToLoginFromModal() {
      this.showAuthPromptModal = false;
      this.$router.push('/login');
    },
    continueShoppingFromModal() {
      this.showAuthPromptModal = false;
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
</style>
