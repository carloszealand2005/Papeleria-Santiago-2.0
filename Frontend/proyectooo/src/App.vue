<template>
  <div class="min-h-screen bg-gray-50">
    <Header />

    <Hero :heroImage="heroImage" />

    <Categorias :categories="categories" />

    <Novedades :featuredProducts="featuredProducts" />
    <Footer />
  </div>
</template>


<script>
import Header from './components/Header.vue'
import Hero from './components/Hero.vue'
import Categorias from './components/categorias.vue'
import Novedades from './components/Novedades.vue'
import Footer from './components/Footer.vue'

export default {
  name: "App",
  components: {
    Header,
    Hero,
    Categorias,
    Novedades,
    Footer
  },
  data() {
    return {
      heroImage: "URL_AQUI",
      categories: [],
      featuredProducts: []
    }
  }
}
</script>
