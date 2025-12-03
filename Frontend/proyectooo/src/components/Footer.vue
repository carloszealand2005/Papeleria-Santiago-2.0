<template>
  <footer class="bg-slate-900 text-white py-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="grid grid-cols-4 gap-12">
        <div class="col-span-2">
          <img 
            src="https://static.readdy.ai/image/a6354382ff0904464d2c460063bc60ba/a517923db6583f4c953e5c11089dec01.jpeg" 
            alt="Santiago Papelería" 
            class="h-16 w-auto mb-6"
          >
          <p class="text-slate-300 mb-6 text-lg">
            Desde 1985, Santiago Papelería ha sido el aliado confiable para estudiantes, profesionales y empresas. Ofrecemos productos de la más alta calidad para todas tus necesidades.
          </p>
          <div class="flex space-x-4">
            <div class="flex items-center space-x-2 text-slate-400">
              <i class="fas fa-map-marker-alt"></i>
              <span>Bogotá, Colombia</span>
            </div>
            <div class="flex items-center space-x-2 text-slate-400">
              <i class="fas fa-phone"></i>
              <span>(601) 234-5678</span>
            </div>
          </div>
        </div>

        <!-- Products Links -->
        <div>
          <h4 class="font-bold text-lg mb-6">Productos</h4>
          <ul class="space-y-3 text-slate-400">
            <li>
              <a href="#" class="hover:text-white transition-colors">Oficina</a>
            </li>
            <li>
              <a href="#" class="hover:text-white transition-colors">Escolar</a>
            </li>
            <li>
              <a href="#" class="hover:text-white transition-colors">Arte y Diseño</a>
            </li>
            <li>
              <a href="#" class="hover:text-white transition-colors">Tecnología</a>
            </li>
            <li>
              <a href="#" class="hover:text-white transition-colors">Papel</a>
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
        <p class="text-slate-400">&copy; 2024 Santiago Papelería. Todos los derechos reservados.</p>
        <div class="flex space-x-6">
          <a href="#" class="text-slate-400 hover:text-white transition-colors">
            <i class="fab fa-facebook-f text-xl"></i>
          </a>
          <a href="#" class="text-slate-400 hover:text-white transition-colors">
            <i class="fab fa-instagram text-xl"></i>
          </a>
          <a href="#" class="text-slate-400 hover:text-white transition-colors">
            <i class="fab fa-twitter text-xl"></i>
          </a>
          <a href="#" class="text-slate-400 hover:text-white transition-colors">
            <i class="fab fa-linkedin text-xl"></i>
          </a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'FooterComponent'
}
</script>

<style scoped>
</style>