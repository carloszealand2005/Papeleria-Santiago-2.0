<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
    <h2 class="text-2xl font-bold text-gray-900 mb-4">¡Mantente al día con nuestros nuevos productos!</h2>
    <p class="text-gray-600 mb-6">Suscríbete a nuestro boletín y entérate de las últimas novedades en papelería</p>
    <div class="max-w-md mx-auto flex gap-3">
      <input
        type="email"
        :value="email"
        @input="updateEmail"
        @keyup.enter="subscribe"
        placeholder="tu-email@ejemplo.com"
        class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:border-blue-600 text-sm"
        style="--tw-ring-color: #1F2937;"
      >
      <button 
        @click="subscribe"
        @mouseover="hoverButton = true"
        @mouseout="hoverButton = false"
        class="px-6 py-3 text-white rounded-lg transition-colors !rounded-button whitespace-nowrap" 
        :style="hoverButton ? 'background-color: #111827;' : 'background-color: #1F2937;'"
      >
        Suscribirse
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductsNewsletter',
  props: {
    email: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      hoverButton: false
    }
  },
  methods: {
    updateEmail(event) {
      this.$emit('update:email', event.target.value);
    },
    subscribe() {
      if (this.email) {
        this.$emit('subscribe', this.email);
      }
    }
  }
}
</script>

<style scoped>
</style>

