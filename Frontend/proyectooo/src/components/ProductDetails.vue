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
    extractApiErrorMessage(error) {
      const data = error && error.response && error.response.data;
      if (!data) return '';
      if (typeof data === 'string') return data;
      if (typeof data.message === 'string') return data.message;
      if (typeof data.detail === 'string') return data.detail;
      const firstKey = Object.keys(data || {})[0];
      const val = firstKey ? data[firstKey] : null;
      if (Array.isArray(val) && typeof val[0] === 'string') return val[0];
      return '';
    },
    getBulkStepFromProduct(product) {
      const raw = product && product.bulto_minimo_mayorista;
      const n = parseInt(raw, 10);
      return Number.isFinite(n) && n > 0 ? n : 1;
    },
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
            // Backend: usar campos *_activo (ya vienen ajustados según token público vs mayorista)
            const precioBaseActivo = parseFloat(productData.precio_base_activo || '0');
            const descuentoActivo = parseFloat(productData.descuento_activo || '0');
            const precioConDescuentoActivo = parseFloat(productData.precio_con_descuento_activo || precioBaseActivo || '0');
            const precioConIvaActivo = parseFloat(productData.precio_con_iva_activo || precioConDescuentoActivo || precioBaseActivo || '0');
            const hasDiscount =
              descuentoActivo >= 1.0 &&
              precioBaseActivo > 0 &&
              precioConDescuentoActivo > 0 &&
              precioConDescuentoActivo < precioBaseActivo;

            this.product = {
              id: productData.SKU,
              sku: productData.SKU,
              name: productData.nombre,
              description: productData.descripcion,
            // Mantener compatibilidad con componentes existentes, pero SIN mezclar bases:
            // - "originalPrice" y "salePrice" deben estar en la misma base (aquí: sin IVA)
            // - el precio final con IVA se puede mostrar aparte con `precio_con_iva_activo`
            originalPrice: precioBaseActivo,
            salePrice: hasDiscount ? precioConDescuentoActivo : null,
              discount: hasDiscount ? descuentoActivo : 0,

              // Campos activos (para futuras mejoras de UI mayorista)
              tipo_precio_activo: productData.tipo_precio_activo,
              precio_base_activo: precioBaseActivo,
              descuento_activo: descuentoActivo,
              precio_con_descuento_activo: precioConDescuentoActivo,
              precio_con_iva_activo: precioConIvaActivo,
              bulto_minimo_mayorista: productData.bulto_minimo_mayorista,
              iva: parseFloat(productData.iva),
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

      const { id: producto_sku } = cartItem;
      const step = this.getBulkStepFromProduct(cartItem);
      let quantity = cartItem && cartItem.quantity != null ? Number(cartItem.quantity) : step;
      if (!Number.isFinite(quantity) || quantity <= 0) quantity = step;
      if (step > 1 && quantity < step) quantity = step;

      try {
        await api.post(`/mi-carrito-detalles/`, {
          producto_sku: producto_sku,
          cantidad: quantity
        });
        this.showNotification(`"${cartItem.name}" añadido al carrito.`, 'success');
        this.$store.commit('SET_CART_ITEM_COUNT', this.cartItemCount + 1);
      } catch (error) {
        console.error('Error al añadir producto al carrito:', error);
        const msg = this.extractApiErrorMessage(error);
        this.showNotification(msg || 'Error al añadir producto al carrito.', 'error');
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
