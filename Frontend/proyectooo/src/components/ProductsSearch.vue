<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Banner -->
    <ProductsHero
      title="Búsqueda de productos"
      :subtitle="subtitleText"
      highlight="🔍 Ordena y filtra distintos productos 🔍"
      leftIconClass=""
      rightIconClass=""
    />

    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-6 py-8">
      <!-- Filter Section -->
      <OrderFilter
        :sortBy="sortBy"
        @sort-changed="handleSortChange"
        @apply-price="handleApplyPrice"
        buttonColor="#1F2937"
      />

      <!-- Results Grid -->
      <FeaturedProducts
        title="Resultados"
        :featuredProducts="filteredProducts"
        badgeText=""
        @add-to-cart="handleAddToCart"
        @select-product="handleSelectProduct"
      />
    </div>

    <!-- Security Footer -->
    <ProductsFooter />
  </div>
</template>

<script>
import ProductsHero from './ProductsHero.vue';
import OrderFilter from './OrderFilter.vue';
import FeaturedProducts from './FeaturedProducts.vue';
import ProductsFooter from './ProductsFooter.vue';
import api from '@/utils/api';

export default {
  name: 'ProductsSearchPage',
  components: {
    ProductsHero,
    OrderFilter,
    FeaturedProducts,
    ProductsFooter
  },
  inject: ['addToCart', 'selectProduct'],
  data() {
    return {
      sortBy: 'relevance',
      products: [],
      priceRange: { min: 0.30, max: 30 },
      isPriceFilterApplied: false,
      searchQuery: '',
    }
  },
  computed: {
    subtitleText() {
      return `Resultados para: ${this.searchQuery || ''}`.trim();
    },
    filteredProducts() {
      return Array.isArray(this.products) ? this.products : [];
    }
  },
  watch: {
    '$route.query.producto': {
      immediate: true,
      handler(newQuery) {
        this.searchQuery = newQuery || '';
        this.fetchProducts();
      }
    }
  },
  methods: {
    getOrderingParam() {
      const map = {
        relevance: 'total_vendidos',
        discount: 'descuento',
        name: 'alphabet',
      };
      return map[this.sortBy] || 'total_vendidos';
    },
    async fetchProducts() {
      const query = (this.searchQuery || '').trim();
      if (!query) {
        this.products = [];
        return;
      }

      try {
        const params = {
          search: query,
          ordering: this.getOrderingParam(),
          limite: 100,
        };

        // Solo aplicar rango de precio cuando el usuario presione "Aplicar"
        if (this.isPriceFilterApplied && this.priceRange) {
          params.precio_min = Number(this.priceRange.min).toFixed(2);
          params.precio_max = Number(this.priceRange.max).toFixed(2);
        }

        const response = await api.get('/productos/', { params });
        this.products = (response.data || []).map(product => ({
          id: product.SKU,
          sku: product.SKU,
          name: product.nombre,
          brand: product.marca,
          description: product.descripcion,
          image: product.imagen_url,
          originalPrice: parseFloat(product.pvp || '0'),
          salePrice: parseFloat(product.precio_con_descuento_publico || '0'),
          discount: parseFloat(product.descuento_publico || '0'),
          category: product.categoria ? product.categoria.toLowerCase() : 'otros'
        }));
      } catch (error) {
        console.error('Error fetching searched products:', error);
        this.products = [];
      }
    },
    handleSortChange(sortValue) {
      this.sortBy = sortValue;
      this.fetchProducts();
    },
    handleApplyPrice(range) {
      this.priceRange = range;
      this.isPriceFilterApplied = true;
      this.fetchProducts();
    },
    handleAddToCart(product) {
      if (this.addToCart) {
        this.addToCart(product);
      }
    },
    handleSelectProduct(product) {
      if (this.selectProduct) {
        this.selectProduct(product);
      }
    },
  }
}
</script>

<style scoped>
</style>


