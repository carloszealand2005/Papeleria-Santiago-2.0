<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Botón para volver al inicio -->
    <div class="max-w-4xl mx-auto px-4 pt-4">
      <button 
        @click="goToHome"
        class="text-blue-600 hover:text-blue-700 font-medium transition-colors cursor-pointer mb-4"
      >
        <i class="fas fa-arrow-left mr-2"></i>Volver al inicio
      </button>
    </div>
    
    <!-- Receipt Container -->
    <div class="max-w-4xl mx-auto py-8 px-4">
      <!-- Receipt Card -->
      <div class="bg-white shadow-lg">
        <ReceiptHeader />
        
        <ReceiptDetails 
          :invoiceData="invoiceData"
          :customerData="customerData"
        />
        
        <div class="p-8">
          <ReceiptProducts :orderItems="orderItems" />
          
          <ReceiptTotals :totals="totals" />
          
          <ReceiptPaymentInfo 
            :paymentInfo="paymentInfo"
            :deliveryInfo="deliveryInfo"
          />
        </div>
        
        <ReceiptFooter />
      </div>
      
      <!-- Action Buttons -->
      <ReceiptActions 
        @print="handlePrint"
        @download-pdf="handleDownloadPDF"
        @send-email="handleSendEmail"
      />
    </div>
  </div>
</template>

<script>
import ReceiptHeader from './ReceiptHeader.vue';
import ReceiptDetails from './ReceiptDetails.vue';
import ReceiptProducts from './ReceiptProducts.vue';
import ReceiptTotals from './ReceiptTotals.vue';
import ReceiptPaymentInfo from './ReceiptPaymentInfo.vue';
import ReceiptFooter from './ReceiptFooter.vue';
import ReceiptActions from './ReceiptActions.vue';

export default {
  name: 'ReceiptPage',
  components: {
    ReceiptHeader,
    ReceiptDetails,
    ReceiptProducts,
    ReceiptTotals,
    ReceiptPaymentInfo,
    ReceiptFooter,
    ReceiptActions
  },
  inject: ['receiptData'],
  computed: {
    invoiceData() {
      return this.receiptData?.invoiceData || {
        number: 'FAC-B-20251126',
        date: new Date().toLocaleDateString('es-CO')
      };
    },
    customerData() {
      return this.receiptData?.customerData || {
        name: 'Cliente',
        id: '1.059.885.432',
        email: 'cliente@email.com',
        address: 'No especificada'
      };
    },
    orderItems() {
      return this.receiptData?.orderItems || [];
    },
    totals() {
      return this.receiptData?.totals || {
        subtotal: 0,
        discount: 0,
        tax: 0,
        total: 0
      };
    },
    paymentInfo() {
      return this.receiptData?.paymentInfo || {
        method: 'Tarjeta de Crédito',
        status: 'Pagado',
        reference: 'TXN-789456123'
      };
    },
    deliveryInfo() {
      return this.receiptData?.deliveryInfo || {
        type: 'Domicilio',
        date: new Date().toLocaleDateString('es-CO'),
        address: 'No especificada'
      };
    }
  },
  methods: {
    goToHome() {
      this.$router.push('/');
    },
    handlePrint() {
      // La lógica de impresión ya está en ReceiptActions
      this.showNotification('Imprimiendo comprobante...');
    },
    handleDownloadPDF() {
      this.showNotification('Descargando comprobante en PDF...');
    },
    handleSendEmail() {
      this.showNotification('Comprobante enviado por email');
    },
    showNotification(message) {
      // Crear una notificación temporal
      const notification = document.createElement('div');
      notification.className = 'fixed top-4 right-4 bg-gray-800 text-white px-6 py-3 rounded-lg shadow-lg z-50 transition-all';
      notification.textContent = message;

      document.body.appendChild(notification);

      setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
          if (document.body.contains(notification)) {
            document.body.removeChild(notification);
          }
        }, 300);
      }, 3000);
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
  .max-w-4xl {
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

