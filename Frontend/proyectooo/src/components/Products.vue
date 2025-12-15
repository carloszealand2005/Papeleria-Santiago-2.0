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
      featuredProducts: [
        {
          id: 'featured-1',
          name: 'Pack Escolar Completo',
          description: 'Incluye 5 cuadernos, 10 plumas, estuche y más',
          image: 'https://readdy.ai/api/search-image?query=back%20to%20school%20stationery%20bundle%20with%20notebooks%20pens%20pencils%20and%20supplies%20on%20clean%20white%20background%20professional%20product%20photography%20minimalist%20style%20commercial%20lighting&width=400&height=250&seq=004&orientation=landscape',
          price: 498.00,
          category: 'school'
        },
        {
          id: 'featured-2',
          name: 'Set de Oficina Premium',
          description: 'Carpetas, archivadores y organizadores profesionales',
          image: 'https://readdy.ai/api/search-image?query=professional%20office%20supplies%20set%20with%20folders%20binders%20and%20organizers%20on%20clean%20white%20background%20modern%20minimalist%20product%20photography%20commercial%20style&width=400&height=250&seq=005&orientation=landscape',
          price: 599.00,
          category: 'office'
        },
        {
          id: 'featured-3',
          name: 'Kit Artístico Profesional',
          description: 'Lápices de colores, marcadores y materiales de dibujo',
          image: 'https://readdy.ai/api/search-image?query=creative%20art%20supplies%20set%20with%20colored%20pencils%20markers%20and%20drawing%20materials%20on%20clean%20white%20background%20professional%20product%20photography%20minimalist%20style&width=400&height=250&seq=006&orientation=landscape',
          price: 599.00,
          category: 'art'
        }
      ],
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
    }
  }
}
</script>

<style scoped>
</style>

