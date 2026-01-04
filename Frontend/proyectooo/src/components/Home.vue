<template>
  <div>
    <!-- <Header 
      @go-to-login="goToLogin"
      @go-to-cart="goToCart"
      @go-to-home="goToHome"
      @go-to-offers="goToOffers"
      @go-to-products="goToProducts"
    /> -->
    <Hero />
    <Categorias 
      :mainCategories="mainCategories" 
      :subCategories="subCategories" 
      @select-category="selectCategory" 
    />
    <Novedades 
      :featuredProducts="featuredProducts"
      @add-to-cart="handleAddToCart"
      @select-product="handleSelectProduct"
    />
    <WhyChooseUs />
    <Newsletter />
    <Footer />
  </div>
</template>

<script>
// import Header from './Header.vue'; // Eliminado
import Hero from './Hero.vue';
import Categorias from './categorias.vue';
import Novedades from './Novedades.vue';
import WhyChooseUs from './WhyChooseUs.vue';
import Newsletter from './Newsletter.vue';
import Footer from './Footer.vue';

export default {
  name: 'HomePage',
  components: {
    // Header, // Eliminado
    Hero,
    Categorias,
    Novedades,
    WhyChooseUs,
    Newsletter,
    Footer
  },
  inject: ['cartItems', 'mainCategories', 'subCategories', 'featuredProducts', 'addToCart', 'selectProduct'],
  methods: {
    goToLogin() {
      this.$router.push('/login');
    },
    goToCart() {
      this.$router.push('/carrito');
    },
    goToHome() {
      this.$router.push('/');
    },
    goToOffers() {
      this.$router.push('/ofertas');
    },
    goToProducts() {
      this.$router.push('/productos');
    },
    selectCategory(category) {
      console.log('Categoría seleccionada:', category.name);
    },
    handleSelectProduct(product) {
      if (this.selectProduct) {
        this.selectProduct(product);
      }
    },
    handleAddToCart(product) {
      if (this.addToCart) {
        this.addToCart(product);
      }
    }
  }
}
</script>

<style scoped>
</style>
