<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Section -->
    <section class="relative bg-gradient-to-r from-blue-500 to-indigo-600 text-white py-20 px-4 sm:px-6 lg:px-8 overflow-hidden">
      <div class="absolute inset-0 z-0 opacity-20">
        <img
          src="https://readdy.ai/api/search-image?query=stationery%20supplies%20background%20abstract%20pattern&width=1600&height=800&orientation=landscape&seq=hero-bg-pattern"
          alt="Background Pattern"
          class="w-full h-full object-cover"
        />
      </div>
      <div class="relative z-10 max-w-7xl mx-auto text-center">
        <h1 class="text-5xl font-extrabold mb-4 leading-tight">Productos favoritos</h1>
        <p class="text-xl font-light mb-8 opacity-90">Todos tus productos favoritos en un solo lugar.</p>
        <div class="flex justify-center items-center text-2xl font-semibold opacity-95">
          <span class="mr-2">❤️</span>
          <span>Explora lo que más te ha gustado</span>
          <span class="ml-2">❤️</span>
        </div>
      </div>
    </section>

    <!-- Contenido de productos favoritos -->
    <div class="max-w-7xl mx-auto px-6 py-8">
      <CategoryFilterComponent
        :selectedCategory="selectedCategory"
        :sortBy="sortBy"
        :filterCategories="filterCategories"
        @category-changed="handleCategoryChange"
        @sort-changed="handleSortChange"
        buttonColor="#DC2626"
      />
      <template v-if="isLoading">
        <p class="text-center text-gray-500 text-lg mt-10">Cargando productos favoritos...</p>
      </template>
      <template v-else-if="favoriteProducts.length > 0">
        <FeaturedProducts
          title="Tus Favoritos"
          :featuredProducts="favoriteProducts"
          @add-to-cart="handleAddToCart"
          @select-product="handleSelectProduct"
          badgeText="Favorito"
          badgeColor="#DC2626"
        />
      </template>
      <template v-else>
        <p class="text-center text-gray-500 text-lg mt-10">Cuando agregues productos a tu lista de favoritos aparecerán aquí.</p>
      </template>
    </div>

    <!-- Success/Error Notification -->
    <div
      v-if="isNotificationVisible"
      class="fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 transform transition-transform duration-300"
    >
      <div class="flex items-center">
        <i class="fas fa-check-circle mr-2"></i>
        {{ notificationMessage }}
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/utils/api';
import FeaturedProducts from './FeaturedProducts.vue';
import { mapGetters } from 'vuex';
import CategoryFilterComponent from './CategoryFilterComponent.vue';

export default {
  name: 'FavoritesPage',
  components: {
    FeaturedProducts,
    CategoryFilterComponent
  },
  inject: ['selectProduct', 'addToCart'],
  data() {
    return {
      favoriteProducts: [],
      isLoading: true,
      isNotificationVisible: false,
      notificationMessage: '',
      selectedCategory: 'all',
      sortBy: 'discount',
      filterCategories: [],
    };
  },
  computed: {
    ...mapGetters(['isAuthenticated']),
  },
  watch: {
    isAuthenticated: { 
      immediate: true, 
      handler(newStatus) {
        if (newStatus) {
          this.fetchCategories();
          this.fetchFavoriteProducts();
        } else {
          this.favoriteProducts = [];
          this.isLoading = false;
        }
      }
    }
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
        this.filterCategories = [{ id: 'all', name: 'Todos', description: 'Ver todos los productos favoritos' }, ...categoriesFromApi];
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    },
    async fetchFavoriteProducts() {
      this.isLoading = true;
      try {
        let url = '/favoritos/';
        if (this.selectedCategory !== 'all') {
          url += `?subcategoria=${this.selectedCategory}`;
        }
        const response = await api.get(url);
        this.favoriteProducts = response.data.map(item => {
          const p = item && item.producto_detail ? item.producto_detail : {};
          // Backend: usar campos *_activo (ya vienen ajustados según token público vs mayorista)
          const precioBaseActivo = parseFloat(p.precio_base_activo || '0');
          const descuentoActivo = parseFloat(p.descuento_activo || '0');
          const precioConDescuentoActivo = parseFloat(p.precio_con_descuento_activo || precioBaseActivo || '0');
          const precioConIvaActivo = parseFloat(p.precio_con_iva_activo || precioConDescuentoActivo || precioBaseActivo || '0');
          const hasDiscount =
            descuentoActivo >= 1.0 &&
            precioBaseActivo > 0 &&
            precioConDescuentoActivo > 0 &&
            precioConDescuentoActivo < precioBaseActivo;

          return ({
            id: p.SKU, // Se mantiene 'id' por compatibilidad con FeaturedProduct
            sku: p.SKU, // Añadimos 'sku' para el handleAddToCart global
            name: p.nombre,
            brand: p.marca,
            description: p.descripcion,
            image: p.imagen_url,

            // Mantener compatibilidad con componentes existentes, pero SIN mezclar bases:
            // - "originalPrice" y "salePrice" deben estar en la misma base (aquí: sin IVA)
            // - si quieres mostrar el precio final con IVA, usa `precio_con_iva_activo` en otra parte del UI
            originalPrice: precioBaseActivo,
            salePrice: hasDiscount ? precioConDescuentoActivo : null,
            discount: hasDiscount ? descuentoActivo : 0,

            // Campos activos (para futuras mejoras de UI mayorista)
            tipo_precio_activo: p.tipo_precio_activo,
            precio_base_activo: precioBaseActivo,
            descuento_activo: descuentoActivo,
            precio_con_descuento_activo: precioConDescuentoActivo,
            precio_con_iva_activo: precioConIvaActivo,
            bulto_minimo_mayorista: p.bulto_minimo_mayorista,

            category: p.categoria ? String(p.categoria).toLowerCase() : 'otros',
            iva: parseFloat(p.iva),
          });
        });
      } catch (error) {
        console.error('Error fetching favorite products:', error);
        this.showNotification('Error al cargar productos favoritos.', 'error');
        this.favoriteProducts = [];
      } finally {
        this.isLoading = false;
      }
    },
    handleAddToCart(product) {
      // Llama a la función global addToCart inyectada
      this.addToCart(product);
    },
    handleSelectProduct(product) {
      // Llama a la función global selectProduct inyectada
      this.selectProduct(product);
    },
    handleCategoryChange(categoryId) {
      this.selectedCategory = categoryId;
      this.fetchFavoriteProducts(); // Cargar productos favoritos con la nueva categoría
    },
    handleSortChange(sortValue) {
      this.sortBy = sortValue;
      this.fetchFavoriteProducts(); // Cargar productos favoritos con el nuevo orden
    },
    showNotification(message, type = 'success') {
      this.notificationMessage = message;
      this.isNotificationVisible = true;
      const notificationElement = document.querySelector('.fixed.top-4.right-4');
      if (notificationElement) {
        notificationElement.classList.remove('bg-green-500', 'bg-red-500');
        notificationElement.classList.add(type === 'error' ? 'bg-red-500' : 'bg-green-500');
      }

      setTimeout(() => {
        this.isNotificationVisible = false;
      }, 3000);
    }
  }
}
</script>

<style scoped>
/* Estilos específicos si son necesarios */
</style>
