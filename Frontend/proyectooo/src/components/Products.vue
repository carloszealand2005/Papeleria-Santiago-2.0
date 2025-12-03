<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Header -->
    <ProductsHeader 
      :cartCount="cartCount"
      @search="handleSearch"
      @go-to-cart="$emit('go-to-cart')"
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
      />
      
      <!-- All Products Grid -->
      <AllProducts
        :filteredProducts="filteredProducts"
        @add-to-cart="handleAddToCart"
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
  props: {
    cartCount: {
      type: Number,
      default: 0
    }
  },
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
      products: [
        {
          id: 1,
          name: 'Cuaderno Rayado A4',
          image: 'https://readdy.ai/api/search-image?query=lined%20notebook%20A4%20size%20on%20clean%20white%20background%20professional%20product%20photography%20minimalist%20style%20office%20supplies&width=300&height=200&seq=007&orientation=landscape',
          originalPrice: 45.00,
          salePrice: 31.50,
          discount: 30,
          category: 'school'
        },
        {
          id: 2,
          name: 'Set Plumas Colores',
          image: 'https://readdy.ai/api/search-image?query=colorful%20pen%20set%20arranged%20on%20white%20background%20professional%20product%20photography%20clean%20minimalist%20style%20office%20supplies&width=300&height=200&seq=008&orientation=landscape',
          originalPrice: 89.00,
          salePrice: 62.30,
          discount: 30,
          category: 'school'
        },
        {
          id: 3,
          name: 'Calculadora Científica',
          image: 'https://readdy.ai/api/search-image?query=scientific%20calculator%20on%20clean%20white%20background%20professional%20product%20photography%20minimalist%20style%20office%20supplies%20technology&width=300&height=200&seq=009&orientation=landscape',
          originalPrice: 299.00,
          salePrice: 179.40,
          discount: 40,
          category: 'tech'
        },
        {
          id: 4,
          name: 'Carpeta Archivadora',
          image: 'https://readdy.ai/api/search-image?query=office%20binder%20folder%20on%20clean%20white%20background%20professional%20product%20photography%20minimalist%20style%20office%20supplies&width=300&height=200&seq=010&orientation=landscape',
          originalPrice: 65.00,
          salePrice: 45.50,
          discount: 30,
          category: 'office'
        },
        {
          id: 5,
          name: 'Lápices de Colores 24 pzs',
          image: 'https://readdy.ai/api/search-image?query=colored%20pencils%20set%2024%20pieces%20arranged%20on%20white%20background%20professional%20product%20photography%20clean%20minimalist%20style%20art%20supplies&width=300&height=200&seq=011&orientation=landscape',
          originalPrice: 159.00,
          salePrice: 111.30,
          discount: 30,
          category: 'art'
        },
        {
          id: 6,
          name: 'Goma y Sacapuntas Set',
          image: 'https://readdy.ai/api/search-image?query=eraser%20and%20pencil%20sharpener%20set%20on%20clean%20white%20background%20professional%20product%20photography%20minimalist%20style%20school%20supplies&width=300&height=200&seq=012&orientation=landscape',
          originalPrice: 35.00,
          salePrice: 24.50,
          discount: 30,
          category: 'school'
        },
        {
          id: 7,
          name: 'Regla Geométrica 30cm',
          image: 'https://readdy.ai/api/search-image?query=geometric%20ruler%2030cm%20on%20clean%20white%20background%20professional%20product%20photography%20minimalist%20style%20office%20supplies&width=300&height=200&seq=013&orientation=landscape',
          originalPrice: 25.00,
          salePrice: 17.50,
          discount: 30,
          category: 'school'
        },
        {
          id: 8,
          name: 'Marcadores Permanentes',
          image: 'https://readdy.ai/api/search-image?query=permanent%20markers%20set%20on%20clean%20white%20background%20professional%20product%20photography%20minimalist%20style%20office%20supplies&width=300&height=200&seq=014&orientation=landscape',
          originalPrice: 79.00,
          salePrice: 55.30,
          discount: 30,
          category: 'office'
        }
      ]
    }
  },
  computed: {
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
  methods: {
    handleCategoryChange(categoryId) {
      this.selectedCategory = categoryId;
    },
    handleSortChange(sortValue) {
      this.sortBy = sortValue;
    },
    handleAddToCart(product) {
      console.log('Adding to cart:', product.name);
      this.$emit('add-to-cart', product);
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

