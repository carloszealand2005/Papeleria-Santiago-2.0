<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <div class="flex items-center space-x-4">
        <span class="font-semibold text-gray-900">Filtrar por:</span>
        <button
          v-for="category in filterCategories"
          :key="category.id"
          @click="selectCategory(category.id)"
          :class="selectedCategory === category.id ? 'text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
          :style="selectedCategory === category.id ? 'background-color: #2563EB;' : ''"
          class="px-4 py-2 rounded-lg text-sm font-medium transition-colors !rounded-button whitespace-nowrap"
        >
          {{ category.name }}
        </button>
      </div>
      <div class="flex items-center space-x-4">
        <span class="text-sm text-gray-600">Ordenar por:</span>
        <select 
          :value="sortBy" 
          @change="handleSortChange"
          class="border border-gray-300 rounded-lg px-3 py-2 text-sm focus:ring-2 focus:border-blue-600" 
          style="--tw-ring-color: #2563EB;"
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
  name: 'OffersFilter',
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

