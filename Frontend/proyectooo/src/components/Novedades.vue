<template>
  <section class="py-20 bg-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center mb-16">
        <div>
          <h2 class="text-4xl font-bold text-slate-900 mb-4">Productos Destacados</h2>
          <p class="text-xl text-slate-600">Lo mejor de nuestra selección premium</p>
        </div>
        <button 
          class="bg-slate-100 hover:bg-slate-200 text-slate-700 px-6 py-3 !rounded-button font-medium transition-colors whitespace-nowrap"
          @click="viewAllProducts"
        >
          Ver todos los productos
        </button>
      </div>

      <div class="grid grid-cols-4 gap-6">
        <div 
          v-for="product in featuredProducts" 
          :key="product.id"
          class="group bg-white rounded-2xl shadow-md hover:shadow-xl transition-all duration-300 overflow-hidden border border-slate-100"
        >
          <!-- Product Image -->
          <div class="relative h-56 overflow-hidden bg-slate-50">
            <img 
              :src="product.image" 
              :alt="product.name" 
              class="w-full h-full object-cover object-top group-hover:scale-105 transition-transform duration-300"
            >
            <!-- Badges -->
            <div class="absolute top-3 left-3">
              <span 
                v-if="product.isNew" 
                class="bg-blue-600 text-white px-3 py-1 rounded-full text-xs font-semibold"
              >
                Nuevo
              </span>
              <span 
                v-if="product.discount" 
                class="bg-red-500 text-white px-3 py-1 rounded-full text-xs font-semibold ml-2"
              >
                -{{ product.discount }}%
              </span>
            </div>
            <!-- Favorite Button -->
            <div class="absolute top-3 right-3">
              <button 
                class="bg-white/80 hover:bg-white text-slate-600 hover:text-red-500 p-2 rounded-full transition-all"
              >
                <i class="fas fa-heart text-sm"></i>
              </button>
            </div>
          </div>

          <!-- Product Info -->
          <div class="p-5">
            <div class="mb-3">
              <h3 class="font-semibold text-slate-900 text-lg mb-1 group-hover:text-blue-600 transition-colors">
                {{ product.name }}
              </h3>
              <p class="text-slate-600 text-sm">{{ product.category }}</p>
            </div>
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-2">
                <span class="text-2xl font-bold text-slate-900">${{ product.price }}</span>
                <span 
                  v-if="product.originalPrice" 
                  class="text-sm text-slate-400 line-through"
                >
                  ${{ product.originalPrice }}
                </span>
              </div>
              <button 
                class="bg-blue-600 hover:bg-blue-700 text-white p-2 !rounded-button transition-colors"
                @click="addToCart(product)"
              >
                <i class="fas fa-plus text-sm"></i>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "NovedadesSection",
  props: {
    featuredProducts: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    addToCart(product) {
      console.log('Agregar al carrito:', product);
      this.$emit('add-to-cart', product);
    },
    viewAllProducts() {
      console.log('Ver todos los productos');
      this.$emit('view-all-products');
    }
  }
}
</script>

<style scoped>
</style>