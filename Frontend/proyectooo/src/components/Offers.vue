<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Banner -->
    <OffersHero />
    
    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-6 py-8">
      <!-- Filter Section -->
      <CategoryFilterComponent
        :selectedCategory="selectedCategory"
        :sortBy="sortBy"
        :filterCategories="filterCategories"
        @category-changed="handleCategoryChange"
        @sort-changed="handleSortChange"
        buttonColor="#2563EB"
      />
      
      <!-- Nuevos Títulos de Ofertas por Descuento y sus Productos -->
      <FeaturedOffers
        title="¡Productos con 90% de descuento!"
        :featuredOffers="products90Discount"
        @add-to-cart="handleAddToCart"
        @select-product="handleSelectProduct"
      />

      <FeaturedOffers
        title="¡Productos con 75% de descuento!"
        :featuredOffers="products75Discount"
        @add-to-cart="handleAddToCart"
        @select-product="handleSelectProduct"
      />

      <FeaturedOffers
        title="¡Productos con 50% de descuento!"
        :featuredOffers="products50Discount"
        @add-to-cart="handleAddToCart"
        @select-product="handleSelectProduct"
      />

      <FeaturedOffers
        title="¡Productos con 30% de descuento!"
        :featuredOffers="products30Discount"
        @add-to-cart="handleAddToCart"
        @select-product="handleSelectProduct"
      />

      <FeaturedOffers
        title="¡Productos con 10% de descuento!"
        :featuredOffers="products10Discount"
        @add-to-cart="handleAddToCart"
        @select-product="handleSelectProduct"
      />

      <FeaturedOffers
        title="¡Productos con descuento!"
        :featuredOffers="productsWithAnyDiscount"
        @add-to-cart="handleAddToCart"
        @select-product="handleSelectProduct"
      />
      
      <!-- Newsletter Section -->
      <OffersNewsletter
        :email="newsletterEmail"
        @update:email="newsletterEmail = $event"
        @subscribe="handleSubscribe"
      />
    </div>
    
    <!-- Security Footer -->
    <OffersFooter />
  </div>
</template>
<script>
import OffersHero from './OffersHero.vue';
import CategoryFilterComponent from './CategoryFilterComponent.vue';
import FeaturedOffers from './FeaturedOffers.vue';
import OffersNewsletter from './OffersNewsletter.vue';
import OffersFooter from './OffersFooter.vue';
import { mapGetters } from 'vuex';
import api from '@/utils/api';

export default {
  name: 'OffersPage',
  components: {
    OffersHero,
    CategoryFilterComponent,
    FeaturedOffers,
    OffersNewsletter,
    OffersFooter
  },
  inject: ['addToCart', 'selectProduct'],
  data() {
    return {
      selectedCategory: 'all',
      sortBy: 'discount',
      newsletterEmail: '',
      filterCategories: [],
      products90Discount: [],
      products75Discount: [],
      products50Discount: [],
      products30Discount: [],
      products10Discount: [],
      productsWithAnyDiscount: [],
    }
  },
  computed: {
    ...mapGetters(['cartItemCount', 'isAuthenticated']), 
  },
  created() {
    this.fetchCategories();
    this.fetchOffersByDiscount(90, 100, 'products90Discount');
    this.fetchOffersByDiscount(75, 89, 'products75Discount');
    this.fetchOffersByDiscount(50, 74, 'products50Discount');
    this.fetchOffersByDiscount(30, 49, 'products30Discount');
    this.fetchOffersByDiscount(10, 29, 'products10Discount');
    this.fetchOffersByDiscount(1, 9, 'productsWithAnyDiscount'); 
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
        this.filterCategories = [{ id: 'all', name: 'Todas', description: 'Ver todas las ofertas' }, ...categoriesFromApi];
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    },
    async fetchOffersByDiscount(minDiscount, maxDiscount, dataProperty) {
      try {
        let url = `/productos/?descuento_min=${minDiscount}&descuento_max=${maxDiscount}&limite=20`;
        if (this.selectedCategory !== 'all') {
          url += `&subcategoria=${this.selectedCategory}`;
        }
        const response = await api.get(url);
          const raw = response && response.data;
          const list = Array.isArray(raw) ? raw : (raw && Array.isArray(raw.results) ? raw.results : []);

          this[dataProperty] = list.map(product => {
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
            category: product.categoria ? product.categoria.toLowerCase() : 'otros',
            badgeColor: product.badge_color || '#EF4444', // Asignar color de badge o un valor por defecto
            isHot: product.is_hot || false // Asignar estado hot o un valor por defecto
            });
          });
      } catch (error) {
        console.error(`Error fetching products with ${minDiscount}-${maxDiscount}% discount:`, error);
      }
    },

    handleCategoryChange(categoryId) {
      this.selectedCategory = categoryId;
      this.fetchOffersByDiscount(90, 100, 'products90Discount');
      this.fetchOffersByDiscount(75, 89, 'products75Discount');
      this.fetchOffersByDiscount(50, 74, 'products50Discount');
      this.fetchOffersByDiscount(30, 49, 'products30Discount');
      this.fetchOffersByDiscount(10, 29, 'products10Discount');
      this.fetchOffersByDiscount(1, 9, 'productsWithAnyDiscount');
    },
    handleSortChange(sortValue) {
      this.sortBy = sortValue
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
    handleSearch(query) {
      this.$emit('search', query);
    },
    handleSubscribe(email) {
      this.$emit('subscribe-newsletter', email);
      this.newsletterEmail = '';
    }
  }
}
</script>
<style scoped>
</style>
