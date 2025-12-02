<template>
<section class="py-16 bg-gray-50">
  <div class="max-w-7xl mx-auto px-4">
    <h3 class="text-3xl font-bold text-gray-800 mb-12">Novedades</h3>

    <div class="grid md:grid-cols-3 gap-8">
      <div v-for="product in featuredProducts" :key="product.id"
        class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg">

        <img :src="product.image" :alt="product.title" class="h-48 w-full object-cover">

        <div class="p-6">
          <h4 class="text-xl font-semibold">{{ product.title }}</h4>
          <p class="text-gray-600 mb-4">{{ product.description }}</p>
          <button class="text-blue-600 hover:text-blue-800">
            Ver más →
          </button>
        </div>

      </div>
    </div>

  </div>
</section>
</template>

<script>
export default {
  name: "NovedadesSection"
}
</script>
