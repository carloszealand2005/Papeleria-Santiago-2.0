<template>
  <section class="relative bg-white overflow-hidden">
    <div class="absolute inset-0 bg-gradient-to-br from-slate-50 to-blue-50"></div>
    <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24">
      <div class="grid grid-cols-2 gap-16 items-center">
        <!-- Left Content -->
        <div class="space-y-8">
          <div class="space-y-4">
            <span class="inline-block px-4 py-2 bg-blue-100 text-blue-800 text-sm font-semibold rounded-full">
              Nueva Colección 2026
            </span>
            <h1 class="text-6xl font-bold text-slate-900 leading-tight">
              <template v-if="isAuthenticated">
                Te damos la bienvenida,<br>
                <span class="text-blue-600">{{ firstName }}</span>
              </template>
              <template v-else>
                Papelería de
                <span class="text-blue-600"> calidad</span>
              </template>
            </h1>
            <p class="text-xl text-slate-600 leading-relaxed">
              Descubre nuestra amplia selección de productos para oficina, escuela y arte. Calidad premium para profesionales y estudiantes.
            </p>
          </div>
          <div class="flex space-x-4">
            <button 
              class="bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 !rounded-button font-semibold text-lg transition-all transform hover:scale-105 whitespace-nowrap"
              @click="exploreProducts"
            >
              <i class="fas fa-shopping-bag mr-2"></i>
              Explorar productos
            </button>
            <button 
              class="border-2 border-slate-300 hover:border-blue-600 text-slate-700 hover:text-blue-600 px-8 py-4 !rounded-button font-semibold text-lg transition-all whitespace-nowrap"
              @click="viewCatalog"
            >
              <i class="fas fa-play mr-2"></i>
              Ver catálogo
            </button>
          </div>
        </div>

        <!-- Right Image -->
        <div class="relative">
          <div class="absolute -inset-4 bg-gradient-to-r from-blue-600 to-purple-600 rounded-3xl opacity-20 blur-lg"></div>
          <div class="relative bg-white rounded-2xl shadow-2xl p-8">
            <img
              src="https://readdy.ai/api/search-image?query=elegant%20office%20supplies%20arrangement%20with%20premium%20notebooks%20colorful%20pens%20and%20modern%20stationery%20items%20on%20clean%20marble%20surface%20professional%20product%20photography&width=600&height=500&seq=hero-new-01&orientation=landscape"
              alt="Productos Santiago Papelería"
              class="w-full h-80 object-cover object-top rounded-xl"
            >
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
import { mapGetters } from 'vuex';

export default {
  name: "HeroSection",
  computed: {
    ...mapGetters(['isAuthenticated', 'getUser']),
    firstName() {
      const user = this.getUser;
      const raw = (user && (user.username || user.email)) ? String(user.username || user.email) : '';
      const fromEmail = raw.includes('@') ? raw.split('@')[0] : raw;
      const cleaned = String(fromEmail).trim();
      if (!cleaned) return 'Cliente';
      // Tomar el primer nombre/segmento
      return cleaned.split(/\s+/)[0];
    }
  },
  methods: {
    exploreProducts() {
      this.$router.push('/productos');
    },
    viewCatalog() {
      this.$router.push('/productos');
    }
  }
}
</script>

<style scoped>
</style>