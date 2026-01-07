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
      // Si la navegación viene desde Home con ?subcategoria=Papeleria, la aplicamos cuando carguen las categorías
      pendingSubcategoriaFromRoute: '',
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
      this.fetchProducts();
      this.fetchFeaturedProducts(this.selectedCategory);
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
    fetchFeaturedProducts(selectedCategoryId = 'all') {
      const params = {
        ordering: 'total_vendidos',
        limite: 20,
      };

      // Para 'subcategoria' usamos el nombre del filtro (viene del backend).
      // Nota: selectedCategoryId normalmente es el id del filtro (en minúsculas).
      if (selectedCategoryId && selectedCategoryId !== 'all') {
        const selected = (this.filterCategories || []).find(c => c.id === selectedCategoryId);
        const subcategoriaNombre = selected && selected.name ? selected.name : selectedCategoryId;
        params.subcategoria = subcategoriaNombre;
      }

      api.get('/productos/', { params })
        .then(response => {
          const raw = response && response.data;
          const list = Array.isArray(raw) ? raw : (raw && Array.isArray(raw.results) ? raw.results : []);

          this.featuredProducts = list.map(product => ({
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
          console.error('Error fetching featured products:', error);
        });
    }
  }
}
</script>

<style scoped>
</style>