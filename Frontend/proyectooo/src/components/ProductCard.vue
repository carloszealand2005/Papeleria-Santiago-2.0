<template>
  <div class="bg-white rounded-lg shadow-md overflow-hidden m-2 w-64">
    <img :src="product.imagen_url" :alt="product.nombre" class="w-full h-48 object-cover">
    <div class="p-4">
      <h3 class="font-bold text-lg mb-1">{{ product.nombre }}</h3>
      <p class="text-sm text-gray-600 mb-1">{{ product.marca }} - {{ product.categoria }}</p>
      <p class="text-gray-700 text-sm mb-2">{{ product.descripcion }}</p>
      <p class="font-bold text-xl text-green-600">S/. {{ product.pvp }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductCard',
  props: {
    product: {
      type: Object,
      required: true
    }
  }
}
</script>

<style scoped>
/* Puedes añadir estilos específicos si es necesario, aunque Tailwind CSS ya nos da bastante */
</style>
