<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Banner -->
    <ProductsHero />
    
    <!-- Main Content -->
    <div class="max-w-7xl mx-auto px-6 py-8">
      <!-- Filter Section -->
      <CategoryFilterComponent
        :selectedCategory="selectedCategory"
        :sortBy="sortBy"
        :filterCategories="filterCategories"
        @category-changed="handleCategoryChange"
        @sort-changed="handleSortChange"
        buttonColor="#1F2937"
      />
      
      <!-- Featured Products -->
      <FeaturedProducts
        title="Productos Destacados"
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
    
  </div>
</template>

<script>
import ProductsHero from './ProductsHero.vue';
import CategoryFilterComponent from './CategoryFilterComponent.vue';
import FeaturedProducts from './FeaturedProducts.vue';
import AllProducts from './AllProducts.vue';
import ProductsNewsletter from './ProductsNewsletter.vue';
import ProductsFooter from './ProductsFooter.vue';
import { mapGetters } from 'vuex';
import api from '@/utils/api';

export default {
  name: 'ProductsPage',
  components: {
    ProductsHero,
    CategoryFilterComponent,
    FeaturedProducts,
    AllProducts,
    ProductsNewsletter,
    ProductsFooter
  },
  inject: ['addToCart', 'selectProduct'],
  data() {
    return {
      selectedCategory: 'all',
      sortBy: 'discount',
      newsletterEmail: '',
      filterCategories: [],
      products: [], // Inicializar para asegurar reactividad
      featuredProducts: [], // Inicializar para asegurar reactividad
    }
  },
  computed: {
    ...mapGetters(['isAuthenticated', 'cartItemCount']), 
    filteredProducts() {
      let filtered = Array.isArray(this.products) ? [...this.products] : [];
      
      // Filtrar por término de búsqueda
      if (this.searchQuery) {
        const lowerCaseQuery = this.searchQuery.toLowerCase();
        filtered = filtered.filter(product => 
          product.name.toLowerCase().includes(lowerCaseQuery) ||
          product.description.toLowerCase().includes(lowerCaseQuery) ||
          (product.category && product.category.toLowerCase().includes(lowerCaseQuery))
        );
      }

      // Filtrar por categoría
      if (this.selectedCategory !== 'all') {
        filtered = filtered.filter(product => product.category === this.selectedCategory);
      }
      
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
  watch: {
    // Nuevo: Observar cambios en el parámetro de búsqueda de la URL
    '$route.query.search': {
      immediate: true, // Ejecutar inmediatamente al cargar el componente
      handler(newSearchQuery) {
        this.searchQuery = newSearchQuery || '';
        // No es necesario llamar a fetchProducts o handleCategoryChange aquí,
        // ya que el computed property filteredProducts reaccionará automáticamente.
      }
    }
  },
  created() {
    this.fetchCategories();
    this.fetchProducts();
    this.fetchFeaturedProducts(this.selectedCategory);
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
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    },
    fetchProducts() {
      let url = '/productos/';
      if (this.selectedCategory !== 'all') {
        url += `?subcategoria=${this.selectedCategory}&limite=20`;
      } else {
        url += `?limite=20`;
      }
      api.get(url)
        .then(response => {
          this.products = response.data.map(product => ({
            id: product.SKU,
            sku: product.SKU, // Añadir sku
            name: product.nombre,
            brand: product.marca,
            description: product.descripcion, 
            image: product.imagen_url,
            originalPrice: parseFloat(product.pvp || '0'), // Asegurar que sea numérico
            salePrice: parseFloat(product.precio_con_descuento_publico || '0'), // Asegurar que sea numérico
            discount: parseFloat(product.descuento_publico || '0'), // Asegurar que sea numérico
            category: product.categoria ? product.categoria.toLowerCase() : 'otros'
          }));
        })
        .catch(error => {
          console.error('Error fetching products:', error);
        });
    },
    handleCategoryChange(categoryId) {
      this.selectedCategory = categoryId;
      this.fetchProducts(); // Vuelve a cargar todos los productos con el filtro de categoría
      this.fetchFeaturedProducts(categoryId);
    },
    handleSortChange(sortValue) {
      this.sortBy = sortValue;
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
    handleSubscribe(email) {
      this.$emit('subscribe-newsletter', email);
      this.newsletterEmail = '';
    },
    fetchFeaturedProducts(subcategoria = 'all') {
      let url = 'http://127.0.0.1:8000/api/productos/destacados/';
      if (subcategoria && subcategoria !== 'all') {
        url += `?limite=20&subcategoria=${subcategoria}`;
      } else {
        url += `?limite=20`;
      }

      api.get(url)
        .then(response => {
          this.featuredProducts = response.data.map(product => ({
            id: product.SKU,
            sku: product.SKU, // Añadir sku
            name: product.nombre,
            description: product.descripcion, 
            image: product.imagen_url,
            originalPrice: parseFloat(product.pvp || '0'), // Asegurar que sea numérico
            salePrice: parseFloat(product.precio_con_descuento_publico || '0'), // Asegurar que sea numérico
            discount: parseFloat(product.descuento_publico || '0'), // Asegurar que sea numérico
            category: product.categoria ? product.categoria.toLowerCase() : 'otros'
          }));
        })
        .catch(error => {
          console.error('Error fetching featured products:', error);
        });
    }
  }
}
</script>

<style scoped>
</style>