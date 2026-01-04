<template>
  <!-- variant: cart (replica el diseño anterior del carrito) -->
  <div v-if="variant === 'cart'" class="space-y-6">
    <div
      v-for="item in items"
      :key="item.id"
      class="flex items-center space-x-4 p-4 border border-gray-200 rounded-lg"
    >
      <!-- Product Image -->
      <div class="w-24 h-24 bg-gray-100 rounded-lg overflow-hidden flex-shrink-0">
        <img
          :src="item.producto && item.producto.imagen_url"
          :alt="item.producto && item.producto.nombre"
          class="w-full h-full object-cover object-top"
        >
      </div>

      <!-- Product Details -->
      <div class="flex-1">
        <h3 class="font-semibold text-gray-900 mb-1">{{ item.producto && item.producto.nombre }}</h3>
        <p class="text-sm text-gray-600 mb-2">{{ item.producto && item.producto.descripcion }}</p>

        <!-- Conditional Discount Display -->
        <template v-if="hasDiscount(item)">
          <div class="flex items-center space-x-2">
            <p class="text-sm text-gray-500 line-through opacity-75">
              ${{ formatMoney(item.producto && item.producto.pvp) }}
            </p>
            <span class="text-sm font-semibold text-green-700">
              -{{ formatPercent(item.producto && item.producto.descuento_publico) }}%
            </span>
          </div>
          <p class="text-lg font-bold text-green-600">
            ${{ formatMoney(item.precio_unitario) }}
          </p>
        </template>
        <template v-else>
          <p class="text-lg font-bold text-gray-900">
            ${{ formatMoney(item.precio_unitario) }}
          </p>
        </template>
      </div>

      <!-- Quantity Controls (solo en modo editable) -->
      <div v-if="editable" class="flex items-center space-x-3">
        <button
          type="button"
          @click.prevent="decreaseQuantity(item)"
          class="w-8 h-8 bg-gray-100 hover:bg-gray-200 rounded-full flex items-center justify-center cursor-pointer !rounded-button whitespace-nowrap"
        >
          <i class="fas fa-minus text-xs text-gray-600"></i>
        </button>
        <span class="w-8 text-center font-medium">{{ item.cantidad }}</span>
        <button
          type="button"
          @click.prevent="increaseQuantity(item)"
          class="w-8 h-8 bg-gray-100 hover:bg-gray-200 rounded-full flex items-center justify-center cursor-pointer !rounded-button whitespace-nowrap"
        >
          <i class="fas fa-plus text-xs text-gray-600"></i>
        </button>
      </div>

      <!-- Total Price (subtotal_detalle_carrito si existe) -->
      <div class="text-right">
        <p class="font-bold text-lg text-gray-900">
          ${{ formatMoney(itemTotal(item)) }}
        </p>
      </div>

      <!-- Remove Button (solo en modo editable) -->
      <button
        v-if="editable"
        type="button"
        @click.prevent="removeItem(item)"
        class="text-red-500 hover:text-red-700 cursor-pointer !rounded-button whitespace-nowrap"
      >
        <i class="fas fa-trash text-lg"></i>
      </button>
    </div>
  </div>

  <!-- variant: checkout (mantiene el diseño actual del checkout) -->
  <div v-else class="space-y-4 mb-6">
    <div
      v-for="item in items"
      :key="item.id"
      class="flex items-center space-x-4 pb-4 border-b border-gray-100"
    >
      <img
        :src="item.producto && item.producto.imagen_url"
        :alt="item.producto && item.producto.nombre"
        class="w-16 h-16 object-cover rounded-lg"
      >

      <div class="flex-1">
        <h3 class="font-medium text-gray-900">{{ item.producto && item.producto.nombre }}</h3>
        <p class="text-sm text-gray-600">Cantidad: {{ item.cantidad }}</p>

        <template v-if="hasDiscount(item)">
          <div class="flex items-center space-x-2 mt-1">
            <span class="text-sm text-gray-500 line-through opacity-75">
              ${{ formatMoney(item.producto && item.producto.pvp) }}
            </span>
            <span class="text-sm font-semibold text-green-700">
              -{{ formatPercent(item.producto && item.producto.descuento_publico) }}%
            </span>
          </div>
          <div class="text-sm font-semibold text-green-700">
            ${{ formatMoney(item.producto && item.producto.precio_con_descuento_publico) }}
          </div>
        </template>
        <template v-else>
          <div class="text-sm font-semibold text-gray-900 mt-1">
            ${{ formatMoney(item.producto && item.producto.pvp) }}
          </div>
        </template>
      </div>

      <!-- En checkout, el valor por línea es subtotal_detalle_carrito (sin IVA), igual que en carrito -->
      <span class="font-semibold text-gray-900">
        ${{ formatMoney(item.subtotal_detalle_carrito) }}
      </span>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OrderItemsSummary',
  props: {
    // Detalles del carrito tal como vienen desde /api/mi-carrito/obtener/ (detalles_carrito)
    items: {
      type: Array,
      required: true
    },
    // Controla el diseño (no la lógica)
    variant: {
      type: String,
      default: 'checkout' // 'checkout' | 'cart'
    },
    // Si es true, muestra controles de cantidad y eliminar. (Para /carrito)
    editable: {
      type: Boolean,
      default: false
    }
  },
  methods: {
    hasDiscount(item) {
      const raw = item && item.producto && item.producto.descuento_publico;
      return parseFloat(raw || '0') > 0;
    },
    itemTotal(item) {
      // Usamos subtotal_detalle_carrito para el total del item si está disponible,
      // de lo contrario, calculamos con precio_unitario
      const subtotal = item && item.subtotal_detalle_carrito;
      if (subtotal !== undefined && subtotal !== null) return parseFloat(subtotal || '0');
      const unit = parseFloat((item && item.precio_unitario) || '0');
      const qty = (item && item.cantidad) || 0;
      return unit * qty;
    },
    increaseQuantity(item) {
      const sku = item && item.producto && item.producto.SKU;
      if (sku) this.$emit('increase-quantity', sku);
    },
    decreaseQuantity(item) {
      const sku = item && item.producto && item.producto.SKU;
      if (sku) this.$emit('decrease-quantity', sku);
    },
    removeItem(item) {
      const sku = item && item.producto && item.producto.SKU;
      if (sku) this.$emit('remove-item', sku);
    },
    formatMoney(value) {
      const n = parseFloat(value || '0');
      return Number.isFinite(n) ? n.toFixed(2) : '0.00';
    },
    formatPercent(value) {
      const n = parseFloat(value || '0');
      return Number.isFinite(n) ? n.toFixed(0) : '0';
    }
  }
}
</script>

<style scoped>
</style>


