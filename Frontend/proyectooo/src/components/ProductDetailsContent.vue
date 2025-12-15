<template>
  <div class="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
    <!-- Breadcrumb -->
    <nav class="flex mb-6" aria-label="Breadcrumb">
      <ol class="flex items-center space-x-2 text-sm text-gray-500">
        <li><a href="#" class="hover:text-indigo-600 cursor-pointer" @click.prevent="goToHome">Inicio</a></li>
        <li><i class="fas fa-chevron-right text-xs"></i></li>
        <li><a href="#" class="hover:text-indigo-600 cursor-pointer" @click.prevent="goToProducts">Productos</a></li>
        <li><i class="fas fa-chevron-right text-xs"></i></li>
        <li class="text-gray-900 font-medium">{{ currentProduct.name }}</li>
      </ol>
    </nav>

    <!-- Product Details Container -->
    <div class="bg-white rounded-xl shadow-lg overflow-hidden">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 p-8">
        <!-- Product Images -->
        <div class="space-y-4">
          <div class="aspect-square rounded-lg overflow-hidden bg-gray-100">
            <img
              :src="currentProduct.mainImage"
              :alt="currentProduct.name"
              class="w-full h-full object-cover object-top cursor-pointer"
              @click="openImageModal"
            />
          </div>
          <div class="grid grid-cols-4 gap-2">
            <div
              v-for="(image, index) in currentProduct.gallery"
              :key="index"
              class="aspect-square rounded-lg overflow-hidden bg-gray-100 cursor-pointer border-2"
              :class="{ 'border-indigo-500': selectedImageIndex === index, 'border-transparent': selectedImageIndex !== index }"
              @click="selectImage(index)"
            >
              <img
                :src="image"
                :alt="`${currentProduct.name} - Vista ${index + 1}`"
                class="w-full h-full object-cover object-top"
              />
            </div>
          </div>
        </div>

        <!-- Product Information -->
        <div class="space-y-6">
          <div>
            <h1 class="text-3xl font-bold text-gray-900">{{ currentProduct.name }}</h1>
            <p class="text-sm text-gray-500 mt-1">SKU: {{ currentProduct.sku }}</p>
          </div>

          <!-- Price -->
          <div class="flex items-center space-x-4">
            <span class="text-4xl font-bold text-indigo-600">${{ currentProduct.price }}</span>
            <span v-if="currentProduct.originalPrice" class="text-xl text-gray-500 line-through">${{ currentProduct.originalPrice }}</span>
            <span v-if="currentProduct.discount" class="bg-red-100 text-red-800 text-sm font-medium px-2.5 py-0.5 rounded">
              -{{ currentProduct.discount }}%
            </span>
          </div>

          <!-- Rating and Reviews -->
          <div class="flex items-center space-x-4">
            <div class="flex items-center">
              <div class="flex text-yellow-400">
                <i v-for="star in 5" :key="star" :class="star <= currentProduct.rating ? 'fas fa-star' : 'far fa-star'"></i>
              </div>
              <span class="ml-2 text-sm text-gray-600">({{ currentProduct.reviewCount }} reseñas)</span>
            </div>
            <span class="text-sm text-green-600 font-medium">En stock</span>
          </div>

          <!-- Description -->
          <div>
            <h3 class="text-lg font-semibold text-gray-900 mb-3">Descripción</h3>
            <p class="text-gray-600 leading-relaxed">{{ currentProduct.description }}</p>
          </div>

          <!-- Product Features -->
          <div>
            <h3 class="text-lg font-semibold text-gray-900 mb-3">Características</h3>
            <ul class="space-y-2">
              <li v-for="feature in currentProduct.features" :key="feature" class="flex items-center text-sm text-gray-600">
                <i class="fas fa-check text-green-500 mr-2"></i>
                {{ feature }}
              </li>
            </ul>
          </div>

          <!-- Quantity and Add to Cart -->
          <div class="space-y-4">
            <div class="flex items-center space-x-4">
              <label class="text-sm font-medium text-gray-900">Cantidad:</label>
              <div class="flex items-center border border-gray-300 rounded-lg">
                <button
                  @click="decreaseQuantity"
                  class="px-3 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-50 cursor-pointer"
                  :disabled="quantity <= 1"
                >
                  <i class="fas fa-minus text-sm"></i>
                </button>
                <span class="px-4 py-2 text-center min-w-[60px] border-x border-gray-300">{{ quantity }}</span>
                <button
                  @click="increaseQuantity"
                  class="px-3 py-2 text-gray-600 hover:text-gray-900 hover:bg-gray-50 cursor-pointer"
                >
                  <i class="fas fa-plus text-sm"></i>
                </button>
              </div>
            </div>
            <div class="flex space-x-4">
              <button
                @click="addToCart"
                class="flex-1 bg-indigo-600 text-white py-3 px-6 rounded-lg font-medium hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-200 cursor-pointer"
              >
                <i class="fas fa-shopping-cart mr-2"></i>
                Agregar al Carrito
              </button>
              <button
                @click="toggleWishlist"
                class="px-4 py-3 border border-gray-300 rounded-lg hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition duration-200 cursor-pointer"
                :class="{ 'text-red-500 border-red-300 bg-red-50': isInWishlist, 'text-gray-600': !isInWishlist }"
              >
                <i :class="isInWishlist ? 'fas fa-heart' : 'far fa-heart'"></i>
              </button>
            </div>
          </div>

          <!-- Additional Information -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-6 border-t border-gray-200">
            <div class="flex items-center text-sm text-gray-600">
              <i class="fas fa-truck text-indigo-500 mr-2"></i>
              Envío gratis en compras +$50
            </div>
            <div class="flex items-center text-sm text-gray-600">
              <i class="fas fa-undo text-indigo-500 mr-2"></i>
              Devoluciones en 30 días
            </div>
            <div class="flex items-center text-sm text-gray-600">
              <i class="fas fa-shield-alt text-indigo-500 mr-2"></i>
              Garantía de calidad
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Related Products -->
    <div class="mt-12">
      <h2 class="text-2xl font-bold text-gray-900 mb-6">Productos Relacionados</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div
          v-for="product in relatedProducts"
          :key="product.id"
          class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden cursor-pointer"
          @click="selectProduct(product)"
        >
          <div class="aspect-square overflow-hidden">
            <img
              :src="product.image"
              :alt="product.name"
              class="w-full h-full object-cover object-top hover:scale-105 transition-transform duration-300"
            />
          </div>
          <div class="p-4">
            <h3 class="font-medium text-gray-900 mb-1">{{ product.name }}</h3>
            <p class="text-sm text-gray-500 mb-2">{{ product.category }}</p>
            <div class="flex items-center justify-between">
              <span class="text-lg font-bold text-indigo-600">${{ product.price }}</span>
              <div class="flex text-yellow-400 text-sm">
                <i v-for="star in 5" :key="star" :class="star <= product.rating ? 'fas fa-star' : 'far fa-star'"></i>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Image Modal -->
    <div v-if="showImageModal" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50" @click="closeImageModal">
      <div class="max-w-4xl max-h-full p-4 relative">
        <img
          :src="currentProduct.mainImage"
          :alt="currentProduct.name"
          class="max-w-full max-h-full object-contain"
        />
        <button
          @click="closeImageModal"
          class="absolute top-4 right-4 text-white hover:text-gray-300 text-2xl cursor-pointer"
        >
          <i class="fas fa-times"></i>
        </button>
      </div>
    </div>

    <!-- Success Notification -->
    <div
      v-if="showNotification"
      class="fixed top-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 transform transition-transform duration-300"
    >
      <div class="flex items-center">
        <i class="fas fa-check-circle mr-2"></i>
        {{ notificationMessage }}
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProductDetailsContent',
  props: {
    product: {
      type: Object,
      required: true
    },
    relatedProducts: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      quantity: 1,
      selectedImageIndex: 0,
      showImageModal: false,
      showNotification: false,
      notificationMessage: '',
      isInWishlist: false
    };
  },
  computed: {
    currentProduct() {
      return this.product || this.getDefaultProduct();
    }
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
    selectImage(index) {
      this.selectedImageIndex = index;
      this.currentProduct.mainImage = this.currentProduct.gallery[index];
    },
    openImageModal() {
      this.showImageModal = true;
    },
    closeImageModal() {
      this.showImageModal = false;
    },
    increaseQuantity() {
      this.quantity++;
    },
    decreaseQuantity() {
      if (this.quantity > 1) {
        this.quantity--;
      }
    },
    addToCart() {
      const cartItem = {
        ...this.currentProduct,
        quantity: this.quantity
      };
      this.$emit('add-to-cart', cartItem);
      this.showSuccessNotification('Producto agregado al carrito');
    },
    toggleWishlist() {
      this.isInWishlist = !this.isInWishlist;
      const message = this.isInWishlist ? 'Agregado a favoritos' : 'Eliminado de favoritos';
      this.showSuccessNotification(message);
    },
    selectProduct(product) {
      this.$emit('select-product', product);
    },
    goToHome() {
      this.$router.push('/');
    },
    goToProducts() {
      this.$router.push('/productos');
    },
    showSuccessNotification(message) {
      this.notificationMessage = message;
      this.showNotification = true;
      setTimeout(() => {
        this.showNotification = false;
      }, 3000);
    }
  }
}
</script>

<style scoped>
input[type="number"]::-webkit-outer-spin-button,
input[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type="number"] {
  -moz-appearance: textfield;
}

.transition {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
</style>

