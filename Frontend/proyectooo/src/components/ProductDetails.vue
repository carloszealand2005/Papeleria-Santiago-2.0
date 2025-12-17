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
import api from '@/utils/api'; // Importamos la instancia configurada de Axios
import { mapGetters } from 'vuex'; // Importamos mapGetters de Vuex

export default {
  name: 'ProductDetailsPage',
  components: {
    ProductDetailsHeader,
    ProductDetailsContent
  },
  inject: ['addToCart', 'selectProduct'],
  computed: {
    ...mapGetters(['isAuthenticated']),
  },
  data() {
    return {
      product: null, // Para almacenar los detalles del producto de la API
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
  created() {
    this.fetchProductDetails();
  },
  watch: {
    '$route.params.id': {
      immediate: true,
      handler(newId) {
        if (newId) {
          this.fetchProductDetails();
        }
      }
    }
  },
  methods: {
    fetchProductDetails() {
      const sku = this.$route.params.id;
      if (!sku) {
        console.error('SKU not found in route params.');
        return;
      }
      api.get(`/productos/?SKU=${sku}`)
        .then(response => {
          if (response.data && response.data.length > 0) {
            const productData = response.data[0];
            this.product = {
              id: productData.SKU,
              name: productData.nombre,
              description: productData.descripcion,
              price: parseFloat(productData.pvp),
              originalPrice: parseFloat(productData.pvp), // Usamos pvp como originalPrice
              discount: 0, // No hay descuento en el JSON, lo dejamos en 0
              category: productData.categoria,
              mainImage: productData.imagen_url,
              gallery: [
                productData.imagen_url,
                productData.imagen_url2,
                productData.imagen_url3,
                productData.imagen_url4,
              ].filter(url => url !== null && url !== ''), // Filtramos URLs nulas o vacías
              features: [
                productData.caracteristica1,
                productData.caracteristica2,
                productData.caracteristica3,
                productData.caracteristica4,
                productData.caracteristica5,
              ].filter(feature => feature !== null && feature !== ''), // Filtramos características nulas o vacías
              brand: productData.marca,
            };
          } else {
            console.warn('No product data found for SKU:', sku);
            this.product = null; // O establecer un producto por defecto si es necesario
          }
        })
        .catch(error => {
          console.error('Error fetching product details:', error);
          this.product = null; // Restablecer el producto en caso de error
        });
    },
    handleAddToCart(cartItem) {
      if (!this.isAuthenticated) {
        this.$router.push('/registro');
        return;
      }

      const { id: producto_sku, quantity } = cartItem; // El cartItem ya tiene el id (SKU) y la quantity
      const cartId = 1; // ID de carrito estático por ahora

      api.post(`/carritos/${cartId}/detalles/`, {
        producto_sku: producto_sku,
        cantidad: quantity
      })
      .then(response => {
        console.log('Producto añadido al carrito:', response.data);
        // Aquí puedes añadir lógica para mostrar una notificación de éxito al usuario
        // o actualizar el contador del carrito en el frontend (tarea pendiente)
      })
      .catch(error => {
        console.error('Error al añadir producto al carrito:', error);
        // Aquí puedes añadir lógica para mostrar una notificación de error al usuario
      });
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

