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
          this[dataProperty] = response.data.map(product => ({
            id: product.SKU,
            sku: product.SKU, // Añadir sku
            name: product.nombre,
            brand: product.marca,
            description: product.descripcion,
            image: product.imagen_url,
            originalPrice: parseFloat(product.pvp || '0'),
            salePrice: parseFloat(product.precio_con_descuento_publico || '0'),
            discount: parseFloat(product.descuento_publico || '0'),
            category: product.categoria ? product.categoria.toLowerCase() : 'otros',
            badgeColor: product.badge_color || '#EF4444', // Asignar color de badge o un valor por defecto
            isHot: product.is_hot || false // Asignar estado hot o un valor por defecto
          }));
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
