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
      <div
        v-if="showEmptyState"
        class="mt-8 p-6 bg-white rounded-xl shadow-sm border border-gray-200"
      >
        <div class="flex items-start gap-4">
          <div class="flex-shrink-0 w-12 h-12 rounded-full bg-blue-50 text-blue-700 flex items-center justify-center">
            <i class="fas fa-search" aria-hidden="true"></i>
          </div>
          <div class="min-w-0">
            <div class="text-lg font-semibold text-gray-900">
              No existen productos relacionados a “{{ normalizedSearchQuery }}” actualmente
            </div>
            <div class="text-sm text-gray-600 mt-1">
              Prueba con otra palabra o ajusta el rango de precio para ampliar los resultados.
            </div>
          </div>
        </div>
      </div>
      <FeaturedProducts
        v-else
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
      isSearching: false,
    }
  },
  computed: {
    subtitleText() {
      return `Resultados para: ${this.searchQuery || ''}`.trim();
    },
    normalizedSearchQuery() {
      return String(this.searchQuery || '').trim();
    },
    filteredProducts() {
      return Array.isArray(this.products) ? this.products : [];
    },
    showEmptyState() {
      return this.normalizedSearchQuery.length > 0 && !this.isSearching && this.filteredProducts.length === 0;
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
        this.isSearching = false;
        return;
      }

      this.isSearching = true;
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
        const raw = response && response.data;
        const list = Array.isArray(raw) ? raw : (raw && Array.isArray(raw.results) ? raw.results : []);

        this.products = list.map(product => {
          // Backend: usar campos *_activo (ya vienen ajustados según token público vs mayorista)
          const precioBaseActivo = parseFloat(product.precio_base_activo || '0');
          const descuentoActivo = parseFloat(product.descuento_activo || '0');
          const precioConDescuentoActivo = parseFloat(product.precio_con_descuento_activo || precioBaseActivo || '0');
          const precioConIvaActivo = parseFloat(product.precio_con_iva_activo || precioConDescuentoActivo || precioBaseActivo || '0');
          const hasDiscount =
            descuentoActivo >= 1.0 &&
            precioBaseActivo > 0 &&
            precioConDescuentoActivo > 0 &&
            precioConDescuentoActivo < precioBaseActivo;

          return ({
          id: product.SKU,
          sku: product.SKU,
          name: product.nombre,
          brand: product.marca,
          description: product.descripcion,
          image: product.imagen_url,
          // Mantener compatibilidad con componentes existentes, pero SIN mezclar bases:
          // - "originalPrice" y "salePrice" deben estar en la misma base (aquí: sin IVA)
          // - si quieres mostrar el precio final con IVA, usa `precio_con_iva_activo` en otra parte del UI
          originalPrice: precioBaseActivo,
          salePrice: hasDiscount ? precioConDescuentoActivo : null,
          discount: hasDiscount ? descuentoActivo : 0,

          // Campos activos (para futuras mejoras de UI mayorista)
          tipo_precio_activo: product.tipo_precio_activo,
          precio_base_activo: precioBaseActivo,
          descuento_activo: descuentoActivo,
          precio_con_descuento_activo: precioConDescuentoActivo,
          precio_con_iva_activo: precioConIvaActivo,
          bulto_minimo_mayorista: product.bulto_minimo_mayorista,
          category: product.categoria ? product.categoria.toLowerCase() : 'otros'
          });
        });
      } catch (error) {
        console.error('Error fetching searched products:', error);
        this.products = [];
      } finally {
        this.isSearching = false;
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


