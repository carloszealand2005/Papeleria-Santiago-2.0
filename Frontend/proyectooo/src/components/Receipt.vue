<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Botón para volver al inicio -->
    <div class="max-w-7xl mx-auto px-4 pt-4">
      <button 
        @click="goToHome"
        class="text-blue-600 hover:text-blue-700 font-medium transition-colors cursor-pointer mb-4"
      >
        <i class="fas fa-arrow-left mr-2"></i>Volver al inicio
      </button>
    </div>
    
    <!-- Receipt Container -->
    <div class="max-w-7xl mx-auto py-8 px-4 space-y-4">
      <div class="bg-white shadow-lg rounded-lg overflow-hidden">
        <div class="p-6 border-b">
          <h1 class="text-2xl font-bold text-gray-900">Gracias por tu compra</h1>
          <p class="text-gray-600 mt-1">
            Tu pedido se ha concretado exitosamente.
            <span v-if="pedidoId">Pedido #{{ pedidoId }}</span>
          </p>
          <p v-if="expiresInSeconds" class="text-sm text-gray-500 mt-2">
            El enlace del PDF expira en {{ expiresInSeconds }} segundos. Si expira, puedes regenerarlo.
          </p>
        </div>

        <div class="p-6 space-y-4">
          <div
            v-if="!isAuthenticated"
            class="p-4 bg-yellow-50 border border-yellow-200 text-yellow-900 rounded-lg"
          >
            Necesitas estar registrado e iniciar sesión para ver los comprobantes de tus compras.
          </div>
          <div v-if="isLoading" class="p-4 bg-blue-50 border border-blue-200 text-blue-800 rounded-lg">
            Cargando comprobante...
          </div>
          <div v-if="errorMessage" class="p-4 bg-red-50 border border-red-200 text-red-800 rounded-lg">
            {{ errorMessage }}
          </div>

          <div class="flex flex-col sm:flex-row gap-3">
            <button
              v-if="pedidoId"
              type="button"
              @click="goToTracking"
              class="inline-flex items-center justify-center px-5 py-3 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg transition-colors cursor-pointer"
              :disabled="isLoading || !isAuthenticated"
              :class="{ 'opacity-60 cursor-not-allowed': isLoading || !isAuthenticated }"
            >
              <i class="fas fa-truck mr-2" aria-hidden="true"></i>Ver seguimiento del pedido
            </button>
            <a
              v-if="pdfUrlDownload"
              :href="pdfUrlDownload"
              class="inline-flex items-center justify-center px-5 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors cursor-pointer"
              :class="{ 'opacity-60 pointer-events-none': !isAuthenticated }"
            >
              <i class="fas fa-download mr-2"></i>Descargar PDF
            </a>
            <button
              v-if="pedidoId"
              type="button"
              @click="regeneratePdfLink"
              class="inline-flex items-center justify-center px-5 py-3 border border-gray-300 hover:bg-gray-50 text-gray-800 rounded-lg transition-colors cursor-pointer"
              :disabled="isLoading || !isAuthenticated"
              :class="{ 'opacity-60 cursor-not-allowed': isLoading || !isAuthenticated }"
            >
              <i class="fas fa-sync-alt mr-2"></i>Regenerar enlace
            </button>
          </div>

          <div v-if="pdfUrl && isAuthenticated" class="w-full bg-gray-50 border rounded-lg overflow-hidden">
            <iframe
              :src="pdfUrl"
              title="Comprobante en PDF"
              class="w-full"
              style="height: 80vh;"
            ></iframe>
          </div>

          <div v-else-if="!isLoading && isAuthenticated" class="text-gray-700">
            No se encontró un enlace de comprobante para mostrar.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/utils/api';
import { mapGetters } from 'vuex';

export default {
  name: 'ReceiptPage',
  computed: {
    ...mapGetters(['isAuthenticated']),
  },
  data() {
    return {
      pedidoId: '',
      pdfUrl: '',
      pdfUrlDownload: '',
      // Solo para UX (el backend devuelve expires_in_seconds en el GET link)
      expiresInSeconds: 0,
      isLoading: false,
      errorMessage: ''
    };
  },
  created() {
    this.hydrateFromSession();

    // Si no tenemos pdfUrl pero sí pedidoId, intentamos regenerar el link
    if (!this.pdfUrl && this.pedidoId && this.isAuthenticated) {
      this.regeneratePdfLink();
    }
  },
  methods: {
    goToHome() {
      this.$router.push('/');
    },
    goToTracking() {
      // Ir directo a "Mis entregas" (tracking) dentro de /mi-cuenta
      this.$router.push({ path: '/mi-cuenta', query: { section: 'deliveries' } });
    },
    hydrateFromSession() {
      try {
        const pedidoId = sessionStorage.getItem('receipt_pedido_id') || '';
        const pdfUrl = sessionStorage.getItem('receipt_pdf_url') || '';
        const pdfUrlDownload = sessionStorage.getItem('receipt_pdf_url_download') || '';
        const expiresAtMsStr = sessionStorage.getItem('receipt_pdf_expires_at_ms') || '';

        this.pedidoId = pedidoId;
        this.pdfUrl = pdfUrl;
        this.pdfUrlDownload = pdfUrlDownload;

        // Convertimos expiresAt → expiresInSeconds aproximado para mostrar algo útil
        const expiresAtMs = expiresAtMsStr ? parseInt(expiresAtMsStr, 10) : 0;
        if (expiresAtMs) {
          const diffMs = expiresAtMs - Date.now();
          this.expiresInSeconds = diffMs > 0 ? Math.ceil(diffMs / 1000) : 0;
        } else {
          this.expiresInSeconds = 0;
        }
      } catch (e) {
        console.error('Error hidratando datos de factura:', e);
      }
    },
    async regeneratePdfLink() {
      if (!this.pedidoId) return;
      if (!this.isAuthenticated) {
        this.errorMessage = 'Necesitas iniciar sesión para ver el comprobante.';
        return;
      }
      if (this.isLoading) return;

      this.isLoading = true;
      this.errorMessage = '';

      try {
        const linkRes = await api.get(`/mis-pedidos/${this.pedidoId}/comprobante/link/`);
        const pdfUrl = linkRes?.data?.pdf_url || '';
        const pdfUrlDownload = linkRes?.data?.pdf_url_download || '';
        const expiresInSeconds = linkRes?.data?.expires_in_seconds || 0;

        if (!pdfUrl || !pdfUrlDownload) {
          throw new Error('No se recibieron enlaces del comprobante.');
        }

        this.pdfUrl = pdfUrl;
        this.pdfUrlDownload = pdfUrlDownload;
        this.expiresInSeconds = expiresInSeconds;

        const now = Date.now();
        const expiresAtMs = expiresInSeconds ? now + (expiresInSeconds * 1000) : 0;

        sessionStorage.setItem('receipt_pdf_url', pdfUrl);
        sessionStorage.setItem('receipt_pdf_url_download', pdfUrlDownload);
        sessionStorage.setItem('receipt_pdf_expires_at_ms', String(expiresAtMs));
      } catch (error) {
        console.error('Error al regenerar el enlace del comprobante:', error);
        this.errorMessage = 'No se pudo cargar el comprobante. Por favor intenta regenerar el enlace.';
      } finally {
        this.isLoading = false;
      }
    }
  }
}
</script>

<style scoped>
/* Print styles */
@media print {
  body {
    margin: 0;
    padding: 0;
  }
  .max-w-7xl {
    max-width: 100%;
    margin: 0;
    padding: 0;
  }
  .bg-gray-100 {
    background: white !important;
  }
  .shadow-lg {
    box-shadow: none !important;
  }
  button {
    display: none !important;
  }
}

/* Receipt specific styles */
.receipt-container {
  background: white;
}

/* Table styles for better readability */
table {
  border-collapse: collapse;
}

table th,
table td {
  border: 1px solid #e5e5e5;
}

/* Hover effects for better UX */
tr:hover {
  background-color: #f9f9f9;
}

/* Responsive design */
@media (max-width: 768px) {
  .grid-cols-2 {
    grid-template-columns: 1fr;
  }

  .text-3xl {
    font-size: 1.5rem;
  }
  
  .text-2xl {
    font-size: 1.25rem;
  }

  .space-x-4 {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .space-x-4 > * {
    margin-right: 0 !important;
    margin-bottom: 0.5rem;
  }

  .overflow-x-auto {
    overflow-x: scroll;
  }
  
  table {
    min-width: 600px;
  }
}
</style>

