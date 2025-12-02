<template>
  <div class="min-h-screen bg-gray-50">
    <Header />

    <Hero :heroImage="heroImage" />

    <Categorias :categories="categories" />

    <Novedades :featuredProducts="featuredProducts" />

    <div class="container mx-auto px-4 py-8 flex flex-wrap justify-center">
      <ProductCard
        v-for="product in products"
        :key="product.SKU"
        :product="product"
      />
    </div>

    <Footer />
  </div>
</template>


<script>
import Header from './components/Header.vue'
import Hero from './components/Hero.vue'
import Categorias from './components/categorias.vue'
import Novedades from './components/Novedades.vue'
import Footer from './components/Footer.vue'
import ProductCard from './components/ProductCard.vue'; // Importar ProductCard
import axios from 'axios'; // Importar axios

export default {
  name: "App",
  components: {
    Header,
    Hero,
    Categorias,
    Novedades,
    ProductCard, // Registrar ProductCard
    Footer
  },
  data() {
    return {
      heroImage: "URL_AQUI",
      categories: [],
      featuredProducts: [],
      products: [] // Nueva propiedad para almacenar los productos
    }
  },
  methods: {
    async fetchProducts() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/productos/');
        this.products = response.data;
        console.log('Productos obtenidos:', this.products); // Para verificar en la consola del navegador
      } catch (error) {
        console.error('Error al obtener los productos:', error);
      }
    }
  },
  mounted() {
    this.fetchProducts(); // Llamar a la función cuando el componente se monte
  }
}
</script>
