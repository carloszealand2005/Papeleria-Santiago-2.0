<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <ProductsHeader 
      :cartCount="cartCount"
      @search="handleSearch"
    />
    
    <!-- Hero Banner -->
    <ProductsHero />
    
    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-6 py-8">
      <!-- Filter Section -->
      <ProductsFilter
        :selectedCategory="selectedCategory"
        :sortBy="sortBy"
        :filterCategories="filterCategories"
        @category-changed="handleCategoryChange"
        @sort-changed="handleSortChange"
      />
      
      <!-- Featured Products -->
      <FeaturedProducts
        :featuredProducts="featuredProducts"
        @add-to-cart="handleAddToCart"
        @select-product="handleSelectProduct"
      />
      
      <!-- All Products Grid -->
      <AllProducts
        :filteredProducts="filteredProducts"
        @add-to-cart="handleAddToCart"
        @select-product="handleSelectProduct"
      />
      
      <!-- Newsletter Section -->
      <ProductsNewsletter
        :email="newsletterEmail"
        @update:email="newsletterEmail = $event"
        @subscribe="handleSubscribe"
      />
    </div>
    
    <!-- Security Footer -->
    <ProductsFooter />
    
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
import ProductsHeader from './ProductsHeader.vue';
import ProductsHero from './ProductsHero.vue';
import ProductsFilter from './ProductsFilter.vue';
import FeaturedProducts from './FeaturedProducts.vue';
import AllProducts from './AllProducts.vue';
import ProductsNewsletter from './ProductsNewsletter.vue';
import ProductsFooter from './ProductsFooter.vue';
import AuthPromptModal from './AuthPromptModal.vue'; // Importamos el nuevo modal
import { mapGetters } from 'vuex';
import api from '@/utils/api';

export default {
  name: 'ProductsPage',
  components: {
    ProductsHeader,
    ProductsHero,
    ProductsFilter,
    FeaturedProducts,
    AllProducts,
    ProductsNewsletter,
    ProductsFooter,
    AuthPromptModal // Registramos el nuevo modal
  },
  inject: ['totalCartItems', 'selectProduct'], // addToCart ha sido removido
  data() {
    return {
      selectedCategory: 'all',
      sortBy: 'discount',
      newsletterEmail: '',
      filterCategories: [
        { id: 'all', name: 'Todos' },
        { id: 'manualidades', name: 'Manualidades' },
        { id: 'escritura', name: 'Escritura' },
        { id: 'papeleria', name: 'Papelería' }
      ],
      featuredProducts: [],
      products: [],
      showAuthPromptModal: false, // Controla la visibilidad del modal
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated']),
    cartCount() {
      return this.totalCartItems || 0;
    },
    filteredProducts() {
      let filtered = this.products;
      
      // Ordenar
      if (this.sortBy === 'discount') {
        filtered = filtered.sort((a, b) => b.discount - a.discount);
      } else if (this.sortBy === 'price') {
        filtered = filtered.sort((a, b) => a.salePrice - b.salePrice);
      } else if (this.sortBy === 'name') {
        filtered = filtered.sort((a, b) => a.name.localeCompare(b.name));
      }
      
      return filtered;
    }
  },
  created() {
    this.fetchProducts();
    this.fetchFeaturedProducts(this.selectedCategory);
  },
  methods: {
    fetchProducts() {
      api.get('/productos/')
        .then(response => {
          this.products = response.data.map(product => ({
            id: product.SKU,
            name: product.nombre,
            brand: product.marca,
            image: product.imagen_url,
            originalPrice: parseFloat(product.pvp),
            salePrice: parseFloat(product.pvp),
            discount: 0,
            category: product.categoria ? product.categoria.toLowerCase() : 'otros'
          }));
        })
        .catch(error => {
          console.error('Error fetching products:', error);
        });
    },
    handleCategoryChange(categoryId) {
      this.selectedCategory = categoryId;
      this.fetchFeaturedProducts(categoryId);
    },
    handleSortChange(sortValue) {
      this.sortBy = sortValue;
    },
    async handleAddToCart(product) {
      if (!this.isAuthenticated) {
        this.showAuthPromptModal = true; // Muestra el modal si no está autenticado
        return;
      }
      try {
        await api.post('/mi-carrito-detalles/', {
          producto_sku: product.id,
          cantidad: 1
        });
        this.showNotification(`"${product.name}" añadido al carrito.`, 'success');
        // Opcional: Recargar el contador del carrito si es necesario
        // this.$emit('cart-updated'); 
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
      console.log('Searching for:', query);
      this.$emit('search', query);
    },
    handleSubscribe(email) {
      console.log('Subscribing email:', email);
      this.$emit('subscribe-newsletter', email);
      this.newsletterEmail = '';
    },
    fetchFeaturedProducts(subcategoria = 'all') {
      let url = 'http://127.0.0.1:8000/api/productos/destacados/';
      if (subcategoria !== 'all') {
        url += `?limite=15&subcategoria=${subcategoria}`;
      } else {
        url += `?limite=15`;
      }

      api.get(url)
        .then(response => {
          this.featuredProducts = response.data.map(product => ({
            id: product.SKU,
            name: product.nombre,
            description: product.descripcion,
            image: product.imagen_url,
            price: parseFloat(product.pvp),
            category: product.categoria ? product.categoria.toLowerCase() : 'otros'
          }));
        })
        .catch(error => {
          console.error('Error fetching featured products:', error);
        });
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
