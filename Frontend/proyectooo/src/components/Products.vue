<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Banner -->
    <ProductsHero />

    <div class="max-w-7xl mx-auto px-6 py-8">
      <!-- Filtros -->
      <CategoryFilterComponent
        :selectedCategory="selectedCategory"
        :sortBy="sortBy"
        :filterCategories="filterCategories"
        @category-changed="handleCategoryChange"
        @sort-changed="handleSortChange"
        buttonColor="#1F2937"
      />

      <!-- Grilla plana -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
        <FeaturedProduct
          v-for="product in products"
          :key="product.id"
          :product="product"
          badgeText=""
          @add-to-cart="handleAddToCart"
          @select-product="handleSelectProduct"
        />
      </div>

      <!-- Paginación smart (truncada) -->
      <div v-if="totalPages > 1" class="mt-8 flex flex-col sm:flex-row items-center justify-between gap-3">
        <button
          type="button"
          class="px-4 py-2 border border-gray-300 hover:bg-gray-50 text-gray-800 rounded-lg transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="currentPage <= 1"
          @click="goToPage(currentPage - 1)"
        >
          Anterior
        </button>

        <div class="flex flex-wrap items-center justify-center gap-2">
          <button
            v-for="(item, idx) in paginationItems"
            :key="`page-item-${idx}-${item}`"
            type="button"
            class="min-w-[40px] px-3 py-2 rounded-lg border text-sm font-medium transition-colors"
            :class="item === currentPage
              ? 'bg-blue-600 border-blue-700 text-white cursor-pointer'
              : (item === '...'
                ? 'bg-white border-transparent text-gray-500 cursor-default'
                : 'bg-white border-gray-300 text-gray-800 hover:bg-gray-50 cursor-pointer')"
            :disabled="item === '...'"
            @click="item !== '...' && goToPage(item)"
          >
            {{ item }}
          </button>
        </div>

        <button
          type="button"
          class="px-4 py-2 border border-gray-300 hover:bg-gray-50 text-gray-800 rounded-lg transition-colors cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
          :disabled="currentPage >= totalPages"
          @click="goToPage(currentPage + 1)"
        >
          Siguiente
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import ProductsHero from './ProductsHero.vue';
import CategoryFilterComponent from './CategoryFilterComponent.vue';
import FeaturedProduct from './FeaturedProduct.vue';
import { mapGetters } from 'vuex';
import api from '@/utils/api';

export default {
  name: 'ProductsPage',
  components: {
    ProductsHero,
    CategoryFilterComponent,
    FeaturedProduct
  },
  inject: ['addToCart', 'selectProduct'],
  data() {
    return {
      selectedCategory: 'all',
      sortBy: 'discount',
      filterCategories: [],
      products: [], // Inicializar para asegurar reactividad
      // Si la navegación viene desde Home con ?subcategoria=Papeleria, la aplicamos cuando carguen las categorías
      pendingSubcategoriaFromRoute: '',
      currentPage: 1,
      totalPages: 1,
      totalCount: 0,
      pageSize: 9,
      searchQuery: '',
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'cartItemCount']), 
    paginationItems() {
      const total = Number(this.totalPages || 1);
      const current = Number(this.currentPage || 1);
      if (total <= 1) return [1];

      // Si hay pocas páginas, mostramos todas
      if (total <= 7) {
        return Array.from({ length: total }, (_, i) => i + 1);
      }

      const items = [];
      const push = (v) => items.push(v);

      // Siempre primera
      push(1);

      const left = Math.max(2, current - 1);
      const right = Math.min(total - 1, current + 1);

      if (left > 2) push('...');

      for (let p = left; p <= right; p++) {
        push(p);
      }

      if (right < total - 1) push('...');

      // Siempre última
      push(total);

      return items;
    },
  },
  watch: {
    // Nuevo: Observar cambios en el parámetro de búsqueda de la URL
    '$route.query.search': {
      immediate: true, // Ejecutar inmediatamente al cargar el componente
      handler(newSearchQuery) {
        this.searchQuery = newSearchQuery || '';
        // CRÍTICO: al cambiar filtros, volver siempre a página 1
        this.currentPage = 1;
        this.fetchProducts();
      }
    }
    ,
    // Nuevo: permitir preseleccionar la subcategoría desde la URL (ej: /productos?subcategoria=Papeleria)
    '$route.query.subcategoria': {
      immediate: true,
      handler(newSubcategoria) {
        const value = String(newSubcategoria || '').trim();
        if (!value) return;

        // Si todavía no cargamos las categorías, lo guardamos para aplicarlo luego
        if (!Array.isArray(this.filterCategories) || this.filterCategories.length === 0) {
          this.pendingSubcategoriaFromRoute = value;
          return;
        }

        this.applySubcategoriaFromRoute(value);
      }
    },
  },
  async created() {
    // Cargar categorías primero para poder mapear nombre -> id del filtro
    await this.fetchCategories();

    // Si venimos con ?subcategoria=..., aplicarlo antes de pedir productos
    const subcategoria = String(this.$route?.query?.subcategoria || '').trim();
    if (subcategoria) {
      this.applySubcategoriaFromRoute(subcategoria);
    } else if (this.pendingSubcategoriaFromRoute) {
      this.applySubcategoriaFromRoute(this.pendingSubcategoriaFromRoute);
      this.pendingSubcategoriaFromRoute = '';
    }

    this.fetchProducts();
  },
  methods: {
    async fetchCategories() {
      try {
        const response = await api.get('/subcategorias/');
        const categoriesFromApi = response.data.map(cat => ({
          id: cat.nombre_subcategoria.toLowerCase(),
          name: cat.nombre_subcategoria,
          description: cat.descripcion_categoria
        }));
        this.filterCategories = [{ id: 'all', name: 'Todos', description: 'Ver todos los productos' }, ...categoriesFromApi];

        // Si ya tenemos una subcategoría pendiente desde la URL, aplicarla ahora
        if (this.pendingSubcategoriaFromRoute) {
          this.applySubcategoriaFromRoute(this.pendingSubcategoriaFromRoute);
          this.pendingSubcategoriaFromRoute = '';
        }
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    },
    applySubcategoriaFromRoute(subcategoriaNombre) {
      const q = String(subcategoriaNombre || '').trim().toLowerCase();
      if (!q) return;

      const match = (this.filterCategories || []).find(c => {
        if (!c) return false;
        const byName = String(c.name || '').trim().toLowerCase() === q;
        const byId = String(c.id || '').trim().toLowerCase() === q;
        return byName || byId;
      });

      this.selectedCategory = match ? match.id : 'all';

      // Al cambiar vía URL, recargamos el contenido para reflejar el filtro seleccionado
      this.currentPage = 1;
      this.fetchProducts();
    },
    fetchProducts() {
      const params = {
        // Activar paginación en backend
        page: this.currentPage,
      };

      // Filtros
      if (this.selectedCategory !== 'all') {
        params.subcategoria = this.selectedCategory;
      }
      if (this.searchQuery) {
        params.search = this.searchQuery;
      }

      // Ordenamiento (backend)
      if (this.sortBy === 'discount') params.ordering = 'descuento';
      else if (this.sortBy === 'name') params.ordering = 'alphabet';
      else if (this.sortBy === 'price') params.ordering = 'pvp';

      api.get('/productos/', { params })
        .then(response => {
          const raw = response && response.data;
          const list = Array.isArray(raw) ? raw : (raw && Array.isArray(raw.results) ? raw.results : []);

          // Paginación estándar DRF
          const count = (raw && typeof raw.count === 'number') ? raw.count : list.length;
          this.totalCount = count;
          this.totalPages = Math.max(1, Math.ceil(count / this.pageSize));

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
            sku: product.SKU, // Añadir sku
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
        })
        .catch(error => {
          console.error('Error fetching products:', error);
        });
    },
    handleCategoryChange(categoryId) {
      this.selectedCategory = categoryId;
      // CRÍTICO: al cambiar filtros, volver siempre a página 1
      this.currentPage = 1;
      this.fetchProducts(); // Vuelve a cargar todos los productos con el filtro de categoría
    },
    handleSortChange(sortValue) {
      this.sortBy = sortValue;
      // CRÍTICO: al cambiar filtros, volver siempre a página 1
      this.currentPage = 1;
      this.fetchProducts();
    },
    goToPage(page) {
      const next = Number(page);
      if (!Number.isFinite(next)) return;
      if (next < 1 || next > this.totalPages) return;
      if (next === this.currentPage) return;
      this.currentPage = next;
      this.fetchProducts();
    },
    handleAddToCart(product) {
      // Utiliza la función addToCart inyectada desde App.vue
      if (this.addToCart) {
        this.addToCart(product);
      }
    },
    handleSelectProduct(product) {
      if (this.selectProduct) {
        this.selectProduct(product);
      }
    },
    handleSearch(query) {
      this.$emit('search', query);
    },
  }
}
</script>

<style scoped>
</style>