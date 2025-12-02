<template>
  <section class="py-12 bg-white">
    <div class="max-w-7xl mx-auto px-6">
      <h2 class="text-3xl font-bold text-gray-800 mb-8">Categorías</h2>

      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        <div
          v-for="category in categories"
          :key="category.id"
          class="bg-gray-100 p-6 rounded-lg shadow hover:shadow-lg transition"
        >
          <h3 class="text-xl font-semibold text-gray-700">{{ category.name }}</h3>
          <p class="text-gray-600 mt-2">{{ category.description }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "CategoriasList",
  props: {
    categories: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
</style>
