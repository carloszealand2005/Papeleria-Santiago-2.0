<template>
  <footer class="bg-gray-900 text-white mt-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <div>
          <div class="flex items-center mb-4">
            <img 
              src="@/assets/papeleria_santiago_logo.png" 
              alt="Papelería Santiago" 
              class="h-8 w-auto mr-3 filter brightness-0 invert"
            >
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
            <a
              href="https://www.facebook.com/share/184ng5tPK6/?mibextid=wwXIfr"
              target="_blank"
              rel="noopener noreferrer"
              class="text-xl hover:text-teal-400 transition-colors"
              aria-label="Facebook"
              title="Facebook"
            >
              <i class="fab fa-facebook" aria-hidden="true"></i>
              <span class="sr-only">Facebook</span>
            </a>
            <a
              href="https://www.instagram.com/mega.santiago?igsh=enpqNHJxc3BmeTlo"
              target="_blank"
              rel="noopener noreferrer"
              class="text-xl hover:text-teal-400 transition-colors"
              aria-label="Instagram"
              title="Instagram"
            >
              <i class="fab fa-instagram" aria-hidden="true"></i>
              <span class="sr-only">Instagram</span>
            </a>
            <a
              href="https://ec.linkedin.com/in/santiago-papeler%C3%ADa-05303129b"
              target="_blank"
              rel="noopener noreferrer"
              class="text-xl hover:text-teal-400 transition-colors"
              aria-label="LinkedIn"
              title="LinkedIn"
            >
              <i class="fab fa-linkedin" aria-hidden="true"></i>
              <span class="sr-only">LinkedIn</span>
            </a>
          </div>
        </div>
      </div>
      <div class="border-t border-gray-800 mt-8 pt-8 text-center text-sm text-gray-400">
        <p>&copy; 2026 Papelería Santiago. Todos los derechos reservados.</p>
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

