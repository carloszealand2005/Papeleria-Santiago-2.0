<template>
  <footer class="bg-gray-900 text-white mt-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <div>
          <div class="flex items-center mb-4">
            <img 
              src="https://static.readdy.ai/image/a6354382ff0904464d2c460063bc60ba/1d728dd92f6f8bab5ded8741c3d0bbae.jpeg" 
              alt="Santiago Papelería" 
              class="h-8 w-auto mr-3 filter brightness-0 invert"
            >
            <h3 class="text-xl font-bold">SANTIAGO</h3>
          </div>
          <p class="text-gray-400 text-sm">
            Tu papelería de confianza con los mejores productos para oficina, escuela y hogar.
          </p>
        </div>
        <div>
          <h4 class="font-semibold mb-4">Productos</h4>
          <ul class="space-y-2 text-sm text-gray-400">
            <li>
              <a href="#" class="hover:text-white cursor-pointer" @click.prevent="goToProducts">Cuadernos</a>
            </li>
            <li>
              <a href="#" class="hover:text-white cursor-pointer" @click.prevent="goToProducts">Bolígrafos</a>
            </li>
            <li>
              <a href="#" class="hover:text-white cursor-pointer" @click.prevent="goToProducts">Archivadores</a>
            </li>
            <li>
              <a href="#" class="hover:text-white cursor-pointer" @click.prevent="goToProducts">Material Escolar</a>
            </li>
          </ul>
        </div>
        <div>
          <h4 class="font-semibold mb-4">Soporte</h4>
          <ul class="space-y-2 text-sm text-gray-400">
            <li>
              <a href="#" class="hover:text-white cursor-pointer" @click.prevent="goToHome">Centro de Ayuda</a>
            </li>
            <li>
              <a href="#" class="hover:text-white cursor-pointer" @click.prevent="goToHome">Contacto</a>
            </li>
            <li>
              <a href="#" class="hover:text-white cursor-pointer" @click.prevent="goToHome">Garantías</a>
            </li>
            <li>
              <a href="#" class="hover:text-white cursor-pointer" @click.prevent="goToHome">Devoluciones</a>
            </li>
          </ul>
        </div>
        <div>
          <h4 class="font-semibold mb-4">Síguenos</h4>
          <div class="flex space-x-4">
            <i class="fab fa-facebook text-xl hover:text-teal-400 cursor-pointer" @click="$emit('social', 'facebook')"></i>
            <i class="fab fa-twitter text-xl hover:text-teal-400 cursor-pointer" @click="$emit('social', 'twitter')"></i>
            <i class="fab fa-instagram text-xl hover:text-teal-400 cursor-pointer" @click="$emit('social', 'instagram')"></i>
            <i class="fab fa-youtube text-xl hover:text-teal-400 cursor-pointer" @click="$emit('social', 'youtube')"></i>
          </div>
        </div>
      </div>
      <div class="border-t border-gray-800 mt-8 pt-8 text-center text-sm text-gray-400">
        <p>&copy; 2025 Papelería Santiago. Todos los derechos reservados.</p>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'CartFooter',
  methods: {
    goToProducts() {
      this.$router.push('/productos');
    },
    goToHome() {
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
</style>

