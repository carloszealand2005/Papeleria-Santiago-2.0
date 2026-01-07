<template>
  <section class="py-20 bg-gradient-to-b from-white to-slate-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <h2 class="text-4xl font-bold text-slate-900 mb-4">Nuestras Categorías</h2>
        <p class="text-xl text-slate-600">Encuentra exactamente lo que necesitas</p>
      </div>

      <!-- Categorías (desde backend: /subcategorias/) -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
        <div 
          v-for="category in displayedCategories" 
          :key="category.id"
          @click="selectCategory(category)"
          class="group relative bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 cursor-pointer overflow-hidden"
        >
          <div class="aspect-w-16 aspect-h-9 h-48">
            <img 
              :src="category.image" 
              :alt="category.name" 
              class="w-full h-full object-cover object-top group-hover:scale-110 transition-transform duration-300"
            >
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
          </div>
          <div class="absolute bottom-0 left-0 right-0 p-6">
            <h3 class="text-2xl font-bold text-white mb-2">{{ category.name }}</h3>
            <p class="text-blue-100">{{ category.description }}</p>
          </div>
        </div>
      </div>

      <!-- Sub Categories (cuadros pequeños como antes) -->
      <div
        v-if="Array.isArray(subCategories) && subCategories.length > 0"
        class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-6 gap-4"
      >
        <div 
          v-for="category in subCategories" 
          :key="category.id"
          @click="selectSubCategory(category)"
          class="flex flex-col items-center p-4 bg-white rounded-xl hover:shadow-md transition-all cursor-pointer border border-slate-200 hover:border-blue-300"
        >
          <div class="w-12 h-12 bg-slate-100 rounded-lg flex items-center justify-center mb-3">
            <i :class="category.icon" class="text-lg text-slate-600"></i>
          </div>
          <h4 class="text-sm font-medium text-slate-700 text-center">{{ category.name }}</h4>
        </div>
      </div>

      <div v-if="isLoading" class="text-center text-slate-500">
        Cargando categorías...
      </div>
      <div v-else-if="loadError" class="text-center text-red-600">
        {{ loadError }}
      </div>
    </div>
  </section>
</template>

<script>
import api from '@/utils/api';

export default {
  name: "CategoriasList",
  props: {
    mainCategories: {
      type: Array,
      default: () => []
    },
    subCategories: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      apiCategories: [],
      isLoading: false,
      loadError: ''
    };
  },
  computed: {
    displayedCategories() {
      // Preferimos las categorías dinámicas del backend; si no hay, usamos las props como fallback
      if (Array.isArray(this.apiCategories) && this.apiCategories.length > 0) return this.apiCategories;
      return Array.isArray(this.mainCategories) ? this.mainCategories : [];
    }
  },
  created() {
    this.fetchSubcategorias();
  },
  methods: {
    async fetchSubcategorias() {
      this.isLoading = true;
      this.loadError = '';
      try {
        const response = await api.get('/subcategorias/');
        const list = Array.isArray(response.data) ? response.data : (response.data?.results || []);

        this.apiCategories = list.map((item) => ({
          id: item.id,
          name: item.nombre_subcategoria,
          description: item.descripcion_categoria,
          image: item.foto_categoria_url,
          // Guardamos el nombre tal como viene del backend para poder filtrar en /productos
          subcategoriaNombre: item.nombre_subcategoria,
        }));
      } catch (e) {
        console.error('Error cargando subcategorías:', e);
        this.apiCategories = [];
        this.loadError = 'No se pudieron cargar las categorías. Intenta nuevamente.';
      } finally {
        this.isLoading = false;
      }
    },
    selectCategory(category) {
      console.log('Categoría seleccionada:', category.name);
      this.$emit('select-category', category);
      // Navegar a /productos con el filtro (subcategoría) seleccionado
      const subcategoria = String(category?.subcategoriaNombre || category?.name || '').trim();
      this.$router.push({ path: '/productos', query: { subcategoria } });
    },
    selectSubCategory(category) {
      // Mantener la funcionalidad anterior: navegar a búsqueda como si fuera un término buscado
      const producto = String(category?.name || '').trim().toLowerCase();
      this.$router.push({ path: '/productos/search', query: { producto } });
    }
  }
};
</script>

<style scoped>
</style>