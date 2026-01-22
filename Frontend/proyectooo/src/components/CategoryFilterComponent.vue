<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <div class="flex flex-wrap items-center gap-2 md:gap-3">
        <span class="font-semibold text-gray-900 shrink-0">Filtrar por:</span>
        <button
          v-for="category in filterCategories"
          :key="category.id"
          @click="selectCategory(category.id)"
          :class="selectedCategory === category.id ? 'text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
          :style="selectedCategory === category.id ? `background-color: ${buttonColor};` : ''"
          class="px-4 py-2 rounded-lg text-sm font-medium transition-colors !rounded-button whitespace-nowrap"
          :title="category.description"
        >
          {{ category.name }}
        </button>
      </div>
      <div class="flex items-center space-x-4">
        <label for="category-filter-sort" class="text-sm text-gray-600">Ordenar por:</label>
        <select 
          id="category-filter-sort"
          :value="sortBy" 
          @change="handleSortChange"
          aria-label="Ordenar por"
          class="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:border-blue-600" 
          :style="`--tw-ring-color: ${buttonColor};`"
        >
          <option value="discount">Mayor descuento</option>
          <option value="price">Menor precio</option>
          <option value="name">Nombre A-Z</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CategoryFilterComponent',
  props: {
    selectedCategory: {
      type: String,
      default: 'all'
    },
    sortBy: {
      type: String,
      default: 'discount'
    },
    filterCategories: {
      type: Array,
      required: true
    },
    buttonColor: {
      type: String,
      default: '#1F2937' // Color por defecto (gris oscuro) si no se especifica
    }
  },
  methods: {
    selectCategory(categoryId) {
      this.$emit('category-changed', categoryId);
    },
    handleSortChange(event) {
      this.$emit('sort-changed', event.target.value);
    }
  }
}
</script>

<style scoped>
</style>
