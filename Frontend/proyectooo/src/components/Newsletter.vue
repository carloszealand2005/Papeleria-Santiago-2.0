<template>
  <section class="py-16 bg-gradient-to-r from-blue-600 to-purple-600">
    <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
      <h2 class="text-3xl font-bold text-white mb-4">Mantente al día</h2>
      <p class="text-blue-100 text-lg mb-8">
        Recibe ofertas exclusivas y novedades directamente en tu email
      </p>
      
      <form 
        @submit.prevent="handleSubscribe"
        class="flex max-w-md mx-auto"
      >
        <input
          type="email"
          v-model="email"
          placeholder="Tu correo electrónico"
          required
          class="flex-1 px-4 py-3 border-none !rounded-button rounded-r-none focus:outline-none focus:ring-2 focus:ring-white text-slate-900"
        >
        <button 
          type="submit"
          class="bg-slate-900 hover:bg-slate-800 text-white px-6 py-3 !rounded-button rounded-l-none font-semibold transition-colors whitespace-nowrap"
        >
          Suscribirse
        </button>
      </form>

      <p v-if="message" :class="messageClass" class="mt-4 text-sm">
        {{ message }}
      </p>
    </div>
  </section>
</template>

<script>
export default {
  name: 'NewsletterSection',
  data() {
    return {
      email: '',
      message: '',
      messageClass: ''
    }
  },
  methods: {
    handleSubscribe() {
      if (this.email.trim()) {
        console.log('Suscribiendo:', this.email);
        // Aquí puedes agregar la lógica para enviar el email al backend
        this.message = '¡Gracias por suscribirte!';
        this.messageClass = 'text-green-100';
        this.email = '';
        
        // Limpiar el mensaje después de 5 segundos
        setTimeout(() => {
          this.message = '';
        }, 5000);
        
        this.$emit('subscribe', this.email);
      }
    }
  }
}
</script>

<style scoped>
</style>