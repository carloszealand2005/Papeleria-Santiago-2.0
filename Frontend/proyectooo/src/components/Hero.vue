<template>
<section class="relative h-80 bg-cover bg-center" :style="{ backgroundImage: `url(${heroImage})` }">
  <div class="absolute inset-0 bg-black bg-opacity-50"></div>

  <div class="relative max-w-7xl mx-auto px-4 h-full flex items-center">
    <div class="text-white max-w-lg">
      <h2 class="text-4xl font-bold mb-4">Regreso a clases</h2>
      <p class="text-xl mb-6 text-gray-200">Todo lo que necesitas para tu año escolar exitoso.</p>
      <button class="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-lg">
        Ver ofertas
      </button>
    </div>
  </div>
</section>
</template>

<script>
export default {
  name: "HeroSection"
}
</script>
