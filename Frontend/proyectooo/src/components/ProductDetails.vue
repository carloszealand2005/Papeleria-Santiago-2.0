<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <ProductDetailsHeader
      @search="handleSearch"
    />
    
    <ProductDetailsContent
      :product="product"
      :related-products="relatedProducts"
      @add-to-cart="handleAddToCart"
      @select-product="handleSelectProduct"
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
import ProductDetailsHeader from './ProductDetailsHeader.vue';
import ProductDetailsContent from './ProductDetailsContent.vue';
import AuthPromptModal from './AuthPromptModal.vue'; // Importamos el nuevo modal
import api from '@/utils/api';
import { mapGetters } from 'vuex';

export default {
  name: 'ProductDetailsPage',
  components: {
    ProductDetailsHeader,
    ProductDetailsContent,
    AuthPromptModal // Registramos el nuevo modal
  },
  inject: ['addToCart', 'selectProduct'],
  computed: {
    ...mapGetters(['isAuthenticated']),
  },
  data() {
    return {
      product: null,
      relatedProducts: [
        {
          id: 2,
          name: 'Set Bolígrafos Gel',
          category: 'Escritura',
          price: 18.50,
          rating: 5,
          image: 'https://readdy.ai/api/search-image?query=Set%20of%20gel%20pens%20colorful%20writing%20instruments%20stationery%20office%20supplies%20clean%20white%20background%20product%20photography&width=300&height=300&seq=rel-prod-001&orientation=squarish'
        },
        {
          id: 3,
          name: 'Organizador Escritorio',
          category: 'Organización',
          price: 45.00,
          rating: 4,
          image: 'https://readdy.ai/api/search-image?query=Desktop%20organizer%20office%20supplies%20holder%20clean%20modern%20design%20white%20background%20product%20photography&width=300&height=300&seq=rel-prod-002&orientation=squarish'
        },
        {
          id: 4,
          name: 'Kit Marcadores Arte',
          category: 'Arte y Diseño',
          price: 89.99,
          rating: 5,
          image: 'https://readdy.ai/api/search-image?query=Art%20markers%20set%20colorful%20drawing%20supplies%20creative%20tools%20clean%20white%20background%20product%20photography&width=300&height=300&seq=rel-prod-003&orientation=squarish'
        },
        {
          id: 5,
          name: 'Carpeta Premium A4',
          category: 'Organización',
          price: 32.50,
          rating: 4,
          image: 'https://readdy.ai/api/search-image?query=Premium%20A4%20folder%20office%20organization%20supplies%20clean%20professional%20design%20white%20background%20product%20photography&width=300&height=300&seq=rel-prod-004&orientation=squarish'
        }
      ],
      showAuthPromptModal: false, // Controla la visibilidad del modal
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
              price: parseFloat(productData.pvp),
              originalPrice: parseFloat(productData.pvp),
              discount: 0,
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
    handleAddToCart(cartItem) {
      if (!this.isAuthenticated) {
        this.showAuthPromptModal = true; // Muestra el modal si no está autenticado
        return;
      }

      const { id: producto_sku, quantity } = cartItem;
      const cartId = 1;

      api.post(`/carritos/${cartId}/detalles/`, {
        producto_sku: producto_sku,
        cantidad: quantity
      })
      .then(response => {
        console.log('Producto añadido al carrito:', response.data);
      })
      .catch(error => {
        console.error('Error al añadir producto al carrito:', error);
      });
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
  }
}
</script>

<style scoped>
</style>
