<template>
<header class="bg-orange-400 shadow-sm">
  <div class="max-w-7xl mx-auto px-4">
    <div class="flex items-center justify-between h-16">

      <!-- Logo -->
      <div class="flex items-center">
        <i class="fas fa-pen-nib text-2xl text-white mr-3"></i>
        <h1 class="text-2xl font-bold text-white">SANTIAGO</h1>
      </div>

      <!-- Navigation -->
      <nav class="hidden md:flex space-x-8">
        <a href="#" class="text-white hover:text-orange-100">Inicio</a>
        <a href="#" class="text-white hover:text-orange-100">Categorías</a>
        <a href="#" class="text-white hover:text-orange-100">Ofertas</a>
        <a href="#" class="text-white hover:text-orange-100">Contacto</a>
      </nav>

      <!-- Buscador y carrito -->
      <div class="flex items-center space-x-4">
        <div class="relative">
          <input type="text" placeholder="Buscar productos..."
            class="pl-10 pr-4 py-2 rounded-lg w-64 text-sm">
          <i class="fas fa-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"></i>
        </div>
        <button class="text-white hover:text-orange-100">
          <i class="fas fa-shopping-cart text-xl"></i>
        </button>
      </div>

    </div>
  </div>
</header>
</template>

<script>
export default {
  name: 'HeaderComponent'
}
</script>
