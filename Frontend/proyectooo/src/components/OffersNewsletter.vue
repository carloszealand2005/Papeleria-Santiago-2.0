<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
    <h2 class="text-2xl font-bold text-gray-900 mb-4">¡No te pierdas nuestras ofertas!</h2>
    <p class="text-gray-600 mb-6">Suscríbete a nuestro boletín y recibe las mejores promociones directamente en tu email</p>
    <div class="max-w-md mx-auto flex gap-3">
      <input
        type="email"
        :value="email"
        @input="updateEmail"
        @keyup.enter="subscribe"
        placeholder="tu-email@ejemplo.com"
        class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:border-blue-600 text-sm"
        style="--tw-ring-color: #2563EB;"
      >
      <button 
        @click="subscribe"
        class="px-6 py-3 text-white rounded-lg hover:bg-blue-700 transition-colors !rounded-button whitespace-nowrap" 
        style="background-color: #2563EB;"
      >
        Suscribirse
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OffersNewsletter',
  props: {
    email: {
      type: String,
      default: ''
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

