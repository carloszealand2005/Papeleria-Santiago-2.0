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
import axios from 'axios'; // Importamos axios

export default {
  name: 'ProductsPage',
  components: {
    ProductsHeader,
    ProductsHero,
    ProductsFilter,
    FeaturedProducts,
    AllProducts,
    ProductsNewsletter,
    ProductsFooter
  },
  inject: ['totalCartItems', 'addToCart', 'selectProduct'],
  data() {
    return {
      selectedCategory: 'all',
      sortBy: 'discount',
      newsletterEmail: '',
      filterCategories: [
        { id: 'all', name: 'Todas' },
        { id: 'school', name: 'Escolares' },
        { id: 'office', name: 'Oficina' },
        { id: 'art', name: 'Artísticos' },
        { id: 'tech', name: 'Tecnología' }
      ],
      featuredProducts: [], // Inicializamos un array vacío para los productos destacados de la API
      products: [] // Inicializamos un array vacío para los productos de la API
    }
  },
  computed: {
    cartCount() {
      return this.totalCartItems || 0;
    },
    filteredProducts() {
      let filtered = this.products;
      
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
  created() {
    this.fetchProducts();
    this.fetchFeaturedProducts();
  },
  methods: {
    fetchProducts() {
      axios.get('http://127.0.0.1:8000/api/productos/')
        .then(response => {
          this.products = response.data.map(product => ({
            // Mapeamos los campos del backend a la estructura que espera el frontend
            id: product.SKU,
            name: product.nombre,
            brand: product.marca, // Añadimos la marca para el ProductCard
            image: product.imagen_url,
            originalPrice: parseFloat(product.pvp), // Usamos pvp como originalPrice
            salePrice: parseFloat(product.pvp), // Por ahora, salePrice es igual a pvp
            discount: 0, // Por ahora no hay descuento desde el backend, lo dejamos en 0
            category: product.categoria ? product.categoria.toLowerCase() : 'otros' // Aseguramos que la categoría sea minúscula para el filtro, y un default si es null
          }));
        })
        .catch(error => {
          console.error('Error fetching products:', error);
          // Puedes añadir lógica para mostrar un mensaje de error al usuario
        });
    },
    handleCategoryChange(categoryId) {
      this.selectedCategory = categoryId;
    },
    handleSortChange(sortValue) {
      this.sortBy = sortValue;
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
      console.log('Searching for:', query);
      this.$emit('search', query);
    },
    handleSubscribe(email) {
      console.log('Subscribing email:', email);
      this.$emit('subscribe-newsletter', email);
      this.newsletterEmail = '';
    },
    fetchFeaturedProducts() {
      axios.get('http://127.0.0.1:8000/api/productos/destacados/')
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
    }
  }
}
</script>

<style scoped>
</style>

