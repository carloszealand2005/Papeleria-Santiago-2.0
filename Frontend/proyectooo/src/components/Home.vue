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
      :featuredProducts="homeFeaturedProducts"
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
import api from '@/utils/api';

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
  data() {
    return {
      premiumFeaturedProducts: [],
    };
  },
  computed: {
    // Mantener fallback: si falla la API, seguimos mostrando los productos "mock" inyectados desde App.vue
    homeFeaturedProducts() {
      return (this.premiumFeaturedProducts && this.premiumFeaturedProducts.length > 0)
        ? this.premiumFeaturedProducts
        : (this.featuredProducts || []);
    },
  },
  async created() {
    await this.fetchPremiumFeaturedProducts();
  },
  methods: {
    async fetchPremiumFeaturedProducts() {
      try {
        const response = await api.get('/productos/', { params: { precio_min: '25.00', limite: 8 } });
        const raw = response && response.data;
        const list = Array.isArray(raw) ? raw : (raw && Array.isArray(raw.results) ? raw.results : []);

        this.premiumFeaturedProducts = list.map(product => {
          // Backend: usar campos *_activo (ya vienen ajustados según token público vs mayorista)
          const precioBaseActivo = parseFloat(product.precio_base_activo || '0');
          const descuentoActivo = parseFloat(product.descuento_activo || '0');
          const precioConDescuentoActivo = parseFloat(product.precio_con_descuento_activo || precioBaseActivo || '0');
          const precioConIvaActivo = parseFloat(product.precio_con_iva_activo || precioConDescuentoActivo || precioBaseActivo || '0');
          const hasDiscount =
            descuentoActivo >= 1.0 &&
            precioBaseActivo > 0 &&
            precioConDescuentoActivo > 0 &&
            precioConDescuentoActivo < precioBaseActivo;

          return {
            id: product.SKU, // Importante: el detalle usa /producto/:id donde id = SKU
            sku: product.SKU,
            name: product.nombre,
            brand: product.marca,
            description: product.descripcion,
            image: product.imagen_url,
            category: product.subcategoria || product.categoria || '',
            // Novedades.vue usa `price` y opcionalmente `originalPrice`.
            // Importante: no mezclar bases (sin IVA vs con IVA) entre precio original y precio con descuento.
            price: (hasDiscount ? precioConDescuentoActivo : precioBaseActivo).toFixed(2),
            originalPrice: hasDiscount ? precioBaseActivo.toFixed(2) : null,
            discount: hasDiscount ? descuentoActivo : 0,

            // Campos activos (para futuras mejoras de UI mayorista)
            tipo_precio_activo: product.tipo_precio_activo,
            precio_base_activo: precioBaseActivo,
            descuento_activo: descuentoActivo,
            precio_con_descuento_activo: precioConDescuentoActivo,
            precio_con_iva_activo: precioConIvaActivo,
            bulto_minimo_mayorista: product.bulto_minimo_mayorista,
          };
        });
      } catch (error) {
        console.error('Home.vue - Error fetching premium featured products:', error);
        this.premiumFeaturedProducts = [];
      }
    },
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
