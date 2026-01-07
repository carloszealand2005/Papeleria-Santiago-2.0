<template>
  <section class="py-20 bg-gradient-to-b from-white to-slate-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <h2 class="text-4xl font-bold text-slate-900 mb-4">Nuestras Categorías</h2>
        <p class="text-xl text-slate-600">Encuentra exactamente lo que necesitas</p>
      </div>

      <!-- Main Categories -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
        <div 
          v-for="category in mainCategories" 
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
          <div class="absolute top-4 right-4 bg-white/20 backdrop-blur-sm rounded-full p-3">
            <i :class="category.icon" class="text-2xl text-white"></i>
          </div>
        </div>
      </div>

      <!-- Sub Categories -->
      <div class="grid grid-cols-6 gap-4">
        <div 
          v-for="category in subCategories" 
          :key="category.id"
          @click="selectCategory(category)"
          class="flex flex-col items-center p-4 bg-white rounded-xl hover:shadow-md transition-all cursor-pointer border border-slate-200 hover:border-blue-300"
        >
          <div class="w-12 h-12 bg-slate-100 rounded-lg flex items-center justify-center mb-3">
            <i :class="category.icon" class="text-lg text-slate-600"></i>
          </div>
          <h4 class="text-sm font-medium text-slate-700 text-center">{{ category.name }}</h4>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
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
  methods: {
    selectCategory(category) {
      console.log('Categoría seleccionada:', category.name);
      this.$emit('select-category', category);
      // Navegar a búsqueda como si fuera un término buscado (ej: /productos/search?producto=cuadernos)
      const producto = String(category?.name || '').trim().toLowerCase();
      this.$router.push({ path: '/productos/search', query: { producto } });
    }
  }
};
</script>

<style scoped>
</style>