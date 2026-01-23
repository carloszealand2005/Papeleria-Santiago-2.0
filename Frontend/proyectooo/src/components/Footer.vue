<template>
  <footer class="bg-slate-900 text-white py-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-4 gap-12">
        <div class="col-span-2">
          <img 
            src="@/assets/papeleria_santiago_logo.png" 
            alt="Santiago Papelería" 
            class="h-16 w-auto mb-6"
          >
          <p class="text-slate-300 mb-6 text-lg">
            Desde 1980, Santiago Papelería ha sido el aliado confiable para estudiantes, profesionales y empresas. Ofrecemos productos de la más alta calidad para todas tus necesidades.
          </p>
          <div class="flex space-x-4">
            <div class="flex items-center space-x-2 text-slate-400">
              <i class="fas fa-map-marker-alt" aria-hidden="true"></i>
              <span>Loja, Ecuador</span>
            </div>
            <div class="flex items-center space-x-2 text-slate-400">
              <i class="fas fa-phone" aria-hidden="true"></i>
              <span>(07) 257-3358</span>
            </div>
          </div>
        </div>

        <!-- Products Links -->
        <div>
          <h4 class="font-bold text-lg mb-6">Productos</h4>
          <ul class="space-y-3 text-slate-400">
            <li>
              <a href="#" @click.prevent="goToProducts" class="hover:text-white transition-colors cursor-pointer">Oficina</a>
            </li>
            <li>
              <a href="#" @click.prevent="goToProducts" class="hover:text-white transition-colors cursor-pointer">Escolar</a>
            </li>
            <li>
              <a href="#" @click.prevent="goToProducts" class="hover:text-white transition-colors cursor-pointer">Arte y Diseño</a>
            </li>
            <li>
              <a href="#" @click.prevent="goToProducts" class="hover:text-white transition-colors cursor-pointer">Tecnología</a>
            </li>
            <li>
              <a href="#" @click.prevent="goToProducts" class="hover:text-white transition-colors cursor-pointer">Papel</a>
            </li>
          </ul>
        </div>

        <!-- Help Links -->
        <div>
          <h4 class="font-bold text-lg mb-6">Ayuda</h4>
          <ul class="space-y-3 text-slate-400">
            <li>
              <a href="#" class="hover:text-white transition-colors">Centro de ayuda</a>
            </li>
            <li>
              <a href="#" class="hover:text-white transition-colors">Envíos y devoluciones</a>
            </li>
            <li>
              <a href="#" class="hover:text-white transition-colors">Términos y condiciones</a>
            </li>
            <li>
              <a href="#" class="hover:text-white transition-colors">Política de privacidad</a>
            </li>
            <li>
              <a href="#" class="hover:text-white transition-colors">Contacto</a>
            </li>
          </ul>
        </div>
      </div>

      <div class="border-t border-slate-800 mt-12 pt-8 flex justify-between items-center">
        <p class="text-slate-400">&copy; 2026 Santiago Papelería. Todos los derechos reservados.</p>
        <div class="flex space-x-6">
          <a
            href="https://www.facebook.com/share/184ng5tPK6/?mibextid=wwXIfr"
            target="_blank"
            rel="noopener noreferrer"
            class="text-slate-400 hover:text-white transition-colors"
            aria-label="Facebook"
            title="Facebook"
          >
            <i class="fab fa-facebook-f text-xl" aria-hidden="true"></i>
            <span class="sr-only">Facebook</span>
          </a>
          <a
            href="https://www.instagram.com/mega.santiago?igsh=enpqNHJxc3BmeTlo"
            target="_blank"
            rel="noopener noreferrer"
            class="text-slate-400 hover:text-white transition-colors"
            aria-label="Instagram"
            title="Instagram"
          >
            <i class="fab fa-instagram text-xl" aria-hidden="true"></i>
            <span class="sr-only">Instagram</span>
          </a>
          <a
            href="https://ec.linkedin.com/in/santiago-papeler%C3%ADa-05303129b"
            target="_blank"
            rel="noopener noreferrer"
            class="text-slate-400 hover:text-white transition-colors"
            aria-label="LinkedIn"
            title="LinkedIn"
          >
            <i class="fab fa-linkedin text-xl" aria-hidden="true"></i>
            <span class="sr-only">LinkedIn</span>
          </a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'FooterComponent',
  methods: {
    goToProducts() {
      this.$router.push('/productos');
    },
    goToOffers() {
      this.$router.push('/ofertas');
    },
    goToHome() {
      this.$router.push('/');
    }
  }
}
</script>

<style scoped>
</style>