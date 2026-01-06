<template>
  <div class="relative overflow-hidden" style="background: linear-gradient(135deg, #1F2937 0%, #111827 100%);">
    <div class="max-w-7xl mx-auto px-6 py-16">
      <div class="text-center text-white">
        <h1 class="text-4xl font-bold mb-4">{{ title }}</h1>
        <p class="text-xl mb-8">{{ subtitle }}</p>
        <div class="flex justify-center items-center space-x-2">
          <i v-if="leftIconClass" :class="leftIconClass"></i>
          <span class="text-lg font-semibold">{{ highlight }}</span>
          <i v-if="rightIconClass" :class="rightIconClass"></i>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductsHero',
  props: {
    title: {
      type: String,
      default: 'Nuevos Productos'
    },
    subtitle: {
      type: String,
      default: 'Descubre las últimas novedades en papelería y artículos de oficina'
    },
    highlight: {
      type: String,
      default: 'Recién llegados'
    },
    leftIconClass: {
      type: String,
      default: 'fas fa-star text-yellow-400 text-2xl'
    },
    rightIconClass: {
      type: String,
      default: 'fas fa-star text-yellow-400 text-2xl'
    }
  }
}
</script>

<style scoped>
</style>

