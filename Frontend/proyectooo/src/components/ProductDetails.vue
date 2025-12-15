<template>
  <div class="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
    <ProductDetailsHeader
      @search="handleSearch"
    />
    
    <ProductDetailsContent
      :product="product"
      :related-products="relatedProducts"
      @add-to-cart="handleAddToCart"
      @select-product="handleSelectProduct"
    />
  </div>
</template>

<script>
import ProductDetailsHeader from './ProductDetailsHeader.vue';
import ProductDetailsContent from './ProductDetailsContent.vue';

export default {
  name: 'ProductDetailsPage',
  components: {
    ProductDetailsHeader,
    ProductDetailsContent
  },
  inject: ['selectedProduct', 'addToCart', 'selectProduct'],
  computed: {
    product() {
      return this.selectedProduct || this.getDefaultProduct();
    }
  },
  data() {
    return {
      relatedProducts: [
        {
          id: 2,
          name: 'Set Bolígrafos Gel',
          category: 'Escritura',
          price: 18.50,
          rating: 5,
          image: 'https://readdy.ai/api/search-image?query=Set%20of%20gel%20pens%20colorful%20writing%20instruments%20stationery%20office%20supplies%20clean%20white%20background%20product%20photography&width=300&height=300&seq=rel-prod-001&orientation=squarish'
        },
        {
          id: 3,
          name: 'Organizador Escritorio',
          category: 'Organización',
          price: 45.00,
          rating: 4,
          image: 'https://readdy.ai/api/search-image?query=Desktop%20organizer%20office%20supplies%20holder%20clean%20modern%20design%20white%20background%20product%20photography&width=300&height=300&seq=rel-prod-002&orientation=squarish'
        },
        {
          id: 4,
          name: 'Kit Marcadores Arte',
          category: 'Arte y Diseño',
          price: 89.99,
          rating: 5,
          image: 'https://readdy.ai/api/search-image?query=Art%20markers%20set%20colorful%20drawing%20supplies%20creative%20tools%20clean%20white%20background%20product%20photography&width=300&height=300&seq=rel-prod-003&orientation=squarish'
        },
        {
          id: 5,
          name: 'Carpeta Premium A4',
          category: 'Organización',
          price: 32.50,
          rating: 4,
          image: 'https://readdy.ai/api/search-image?query=Premium%20A4%20folder%20office%20organization%20supplies%20clean%20professional%20design%20white%20background%20product%20photography&width=300&height=300&seq=rel-prod-004&orientation=squarish'
        }
      ]
    };
  },
  methods: {
    getDefaultProduct() {
      return {
        id: 1,
        name: 'Cuaderno Premium A4',
        sku: 'CUA-001',
        price: 24.99,
        originalPrice: 29.99,
        discount: 17,
        rating: 4,
        reviewCount: 156,
        category: 'Cuadernos',
        description: 'Cuaderno de alta calidad con hojas punteadas, perfecto para tomar notas, dibujar o planificar. Fabricado con materiales sostenibles y tapa dura resistente que protege el contenido.',
        features: [
          '120 páginas de papel de 90g/m²',
          'Hojas punteadas para máxima versatilidad',
          'Tapa dura resistente al desgaste',
          'Banda elástica y marcapáginas incluido',
          'Papel sin ácido que previene el amarillamiento',
          'Tamaño A4 (210 x 297 mm)'
        ],
        mainImage: 'https://readdy.ai/api/search-image?query=Premium%20A4%20notebook%20with%20dotted%20pages%20high%20quality%20hardcover%20stationery%20office%20supplies%20clean%20white%20background%20product%20photography&width=500&height=500&seq=prod-main-001&orientation=squarish',
        gallery: [
          'https://readdy.ai/api/search-image?query=Premium%20A4%20notebook%20with%20dotted%20pages%20high%20quality%20hardcover%20stationery%20office%20supplies%20clean%20white%20background%20product%20photography&width=120&height=120&seq=prod-gal-001&orientation=squarish',
          'https://readdy.ai/api/search-image?query=Premium%20A4%20notebook%20opened%20showing%20dotted%20pages%20clean%20white%20background%20product%20detail%20photography&width=120&height=120&seq=prod-gal-002&orientation=squarish',
          'https://readdy.ai/api/search-image?query=Premium%20A4%20notebook%20back%20cover%20with%20elastic%20band%20bookmark%20clean%20white%20background%20product%20photography&width=120&height=120&seq=prod-gal-003&orientation=squarish',
          'https://readdy.ai/api/search-image?query=Premium%20A4%20notebook%20side%20view%20showing%20thickness%20and%20quality%20binding%20clean%20white%20background%20product%20photography&width=120&height=120&seq=prod-gal-004&orientation=squarish'
        ]
      };
    },
    handleAddToCart(product) {
      if (this.addToCart) {
        this.addToCart(product);
      }
    },
    handleSelectProduct(product) {
      if (this.selectProduct) {
        this.selectProduct(product);
      }
    },
    handleSearch(query) {
      // Navegar a productos con búsqueda
      this.$router.push({ path: '/productos', query: { search: query } });
    }
  }
}
</script>

<style scoped>
</style>

