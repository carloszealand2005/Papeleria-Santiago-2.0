<template>
  <div>
    <Header 
      @go-to-login="goToLogin"
      @go-to-cart="goToCart"
      @go-to-home="goToHome"
      @go-to-offers="goToOffers"
      @go-to-products="goToProducts"
      :cartCount="cartCount"
    />
    <Hero />
    <Categorias 
      :mainCategories="mainCategories" 
      :subCategories="subCategories" 
      @select-category="selectCategory" 
    />
    <Novedades 
      :featuredProducts="featuredProducts"
      @select-product="handleSelectProduct"
      @add-to-cart="handleAddToCart"
    />
    <WhyChooseUs />
    <Newsletter />
    <Footer />
  </div>
</template>

<script>
import Header from './Header.vue';
import Hero from './Hero.vue';
import Categorias from './categorias.vue';
import Novedades from './Novedades.vue';
import WhyChooseUs from './WhyChooseUs.vue';
import Newsletter from './Newsletter.vue';
import Footer from './Footer.vue';

export default {
  name: 'HomePage',
  components: {
    Header,
    Hero,
    Categorias,
    Novedades,
    WhyChooseUs,
    Newsletter,
    Footer
  },
  inject: ['cartItems', 'totalCartItems', 'mainCategories', 'subCategories', 'featuredProducts', 'addToCart', 'selectProduct'],
  computed: {
    cartCount() {
      return this.totalCartItems || 0;
    }
  },
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

