<template>
  <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-8">
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
      <!-- Left: Sort -->
      <div class="flex items-center space-x-4">
        <span class="font-semibold text-gray-900">Ordenar por:</span>
        <button
          v-for="option in sortOptions"
          :key="option.value"
          @click="selectSort(option.value)"
          :class="sortBy === option.value ? 'text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'"
          :style="sortBy === option.value ? `background-color: ${buttonColor};` : ''"
          class="px-4 py-2 rounded-lg text-sm font-medium transition-colors !rounded-button whitespace-nowrap"
        >
          {{ option.label }}
        </button>
      </div>

      <!-- Right: Price range -->
      <div class="flex flex-col sm:flex-row sm:items-center gap-4">
        <div class="min-w-[280px]">
          <div class="flex items-center justify-between text-sm text-gray-600 mb-2">
            <span>Precio</span>
            <span class="font-medium text-gray-900">
              ${{ minPriceDisplay }} - ${{ maxPriceDisplay }}
            </span>
          </div>

          <!-- Slider doble (visual): una sola barra con dos extremos -->
          <div class="range-wrap">
            <div class="range-track"></div>
            <div class="range-fill" :style="rangeFillStyle"></div>
            <input
              v-model.number="minPrice"
              type="range"
              :min="minLimit"
              :max="maxLimit"
              :step="step"
              @input="normalizeRange('min')"
              class="range-input range-input--min"
              :style="{ zIndex: minThumbZ }"
              aria-label="Precio mínimo"
            >
            <input
              v-model.number="maxPrice"
              type="range"
              :min="minLimit"
              :max="maxLimit"
              :step="step"
              @input="normalizeRange('max')"
              class="range-input range-input--max"
              :style="{ zIndex: maxThumbZ }"
              aria-label="Precio máximo"
            >
          </div>

          <div class="flex justify-between text-xs text-gray-500 mt-1">
            <span>${{ minLimitDisplay }}</span>
            <span>${{ maxLimitDisplay }}</span>
          </div>
        </div>

        <button
          class="px-4 py-2 rounded-lg text-sm font-medium text-white transition-colors !rounded-button whitespace-nowrap"
          :style="`background-color: ${buttonColor};`"
          @click="applyPriceFilter"
        >
          Aplicar
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OrderFilter',
  props: {
    sortBy: {
      type: String,
      default: 'relevance'
    },
    buttonColor: {
      type: String,
      default: '#1F2937'
    },
    minLimit: {
      type: Number,
      default: 0.30
    },
    maxLimit: {
      type: Number,
      default: 200
    },
    step: {
      type: Number,
      default: 0.10
    }
  },
  data() {
    return {
      minPrice: this.minLimit,
      maxPrice: this.maxLimit,
      sortOptions: [
        { value: 'relevance', label: 'Mayor relevancia' },
        { value: 'discount', label: 'Mayor descuento' },
        { value: 'name', label: 'Alfabéticamente' },
      ],
    }
  },
  computed: {
    minPriceDisplay() {
      return Number(this.minPrice || 0).toFixed(2);
    },
    maxPriceDisplay() {
      return Number(this.maxPrice || 0).toFixed(2);
    },
    minLimitDisplay() {
      return Number(this.minLimit || 0).toFixed(2);
    },
    maxLimitDisplay() {
      return Number(this.maxLimit || 0).toFixed(2);
    },
    rangeFillStyle() {
      const denom = (this.maxLimit - this.minLimit) || 1;
      const min = Math.min(Math.max(Number(this.minPrice), this.minLimit), this.maxLimit);
      const max = Math.min(Math.max(Number(this.maxPrice), this.minLimit), this.maxLimit);
      const minPct = ((min - this.minLimit) / denom) * 100;
      const maxPct = ((max - this.minLimit) / denom) * 100;

      return {
        left: `${minPct}%`,
        right: `${100 - maxPct}%`,
        backgroundColor: this.buttonColor,
      };
    },
    minThumbZ() {
      // Si los thumbs están muy cerca, priorizamos el min para que sea fácil de arrastrar
      return Number(this.minPrice) >= Number(this.maxPrice) - Number(this.step) ? 6 : 4;
    },
    maxThumbZ() {
      return 5;
    }
  },
  methods: {
    selectSort(value) {
      this.$emit('sort-changed', value);
    },
    normalizeRange(source) {
      const min = Number(this.minPrice);
      const max = Number(this.maxPrice);

      if (source === 'min' && min > max) {
        this.maxPrice = min;
      }
      if (source === 'max' && max < min) {
        this.minPrice = max;
      }
    },
    applyPriceFilter() {
      this.normalizeRange('min');
      this.$emit('apply-price', { min: this.minPrice, max: this.maxPrice });
    }
  }
}
</script>

<style scoped>
.range-wrap {
  position: relative;
  width: 100%;
  height: 18px;
  display: flex;
  align-items: center;
}

.range-track {
  position: absolute;
  left: 0;
  right: 0;
  height: 6px;
  border-radius: 9999px;
  background: #e5e7eb; /* gray-200 */
}

.range-fill {
  position: absolute;
  height: 6px;
  border-radius: 9999px;
}

.range-input {
  position: absolute;
  left: 0;
  right: 0;
  width: 100%;
  height: 18px;
  background: transparent;
  -webkit-appearance: none;
  appearance: none;
  pointer-events: none; /* Permitimos drag solo en el thumb */
}

.range-input::-webkit-slider-runnable-track {
  height: 6px;
  background: transparent;
}

.range-input::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 9999px;
  background: #111827; /* gray-900 */
  border: 2px solid #ffffff;
  box-shadow: 0 1px 2px rgba(0,0,0,0.15);
  pointer-events: auto;
  cursor: pointer;
}

.range-input::-moz-range-track {
  height: 6px;
  background: transparent;
}

.range-input::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 9999px;
  background: #111827; /* gray-900 */
  border: 2px solid #ffffff;
  box-shadow: 0 1px 2px rgba(0,0,0,0.15);
  pointer-events: auto;
  cursor: pointer;
}
</style>


