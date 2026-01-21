<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Toast -->
    <div
      v-if="toast.visible"
      class="fixed top-4 right-4 z-50 px-5 py-3 rounded-lg shadow-lg border transition-all"
      :class="toast.type === 'success'
        ? 'bg-green-600 text-white border-green-700'
        : 'bg-red-600 text-white border-red-700'"
    >
      {{ toast.message }}
    </div>

    <div v-if="isAuthenticated" class="max-w-7xl mx-auto px-6 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <!-- Sidebar -->
        <aside class="lg:col-span-4 xl:col-span-3">
          <div class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div class="p-6 border-b border-gray-100">
              <div class="flex items-center gap-4">
                <div class="w-16 h-16 rounded-full bg-gray-100 border border-gray-200 flex items-center justify-center overflow-hidden">
                  <!-- Placeholder avatar (reemplazable por foto real) -->
                  <img
                    v-if="avatarUrl"
                    :src="avatarUrl"
                    alt="Foto de perfil"
                    class="w-full h-full object-cover"
                  />
                  <i v-else class="fas fa-user text-gray-400 text-2xl"></i>
                </div>
                <div class="min-w-0">
                  <div class="text-lg font-semibold text-gray-900 truncate">
                    {{ displayName }}
                  </div>
                  <div class="text-sm text-gray-600">
                    {{ customerTypeLabel }}
                  </div>
                </div>
              </div>
            </div>

            <nav class="p-2">
              <button
                type="button"
                class="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-colors"
                :class="activeSection === 'profile'
                  ? 'bg-blue-50 text-blue-700'
                  : 'text-gray-700 hover:bg-gray-50'"
                @click="activeSection = 'profile'"
              >
                <i class="fas fa-id-card w-5 text-center"></i>
                <span class="font-medium">Perfil</span>
              </button>
              <button
                type="button"
                class="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-colors"
                :class="activeSection === 'deliveries'
                  ? 'bg-blue-50 text-blue-700'
                  : 'text-gray-700 hover:bg-gray-50'"
                @click="activeSection = 'deliveries'"
              >
                <i class="fas fa-truck w-5 text-center"></i>
                <span class="font-medium">Mis entregas</span>
              </button>
              <button
                type="button"
                class="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-colors"
                :class="activeSection === 'orders'
                  ? 'bg-blue-50 text-blue-700'
                  : 'text-gray-700 hover:bg-gray-50'"
                @click="activeSection = 'orders'"
              >
                <i class="fas fa-receipt w-5 text-center"></i>
                <span class="font-medium">Pedidos</span>
              </button>
              <button
                type="button"
                class="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-left transition-colors text-gray-700 hover:bg-gray-50"
                @click="handleLogoutClick"
              >
                <i class="fas fa-sign-out-alt w-5 text-center"></i>
                <span class="font-medium">Cerrar sesión</span>
              </button>
            </nav>
          </div>
        </aside>

        <!-- Content -->
        <section class="lg:col-span-8 xl:col-span-9">
          <!-- Profile -->
          <div v-if="activeSection === 'profile'" class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div class="p-6 border-b border-gray-100">
              <h2 class="text-xl font-semibold text-gray-900">Mi perfil</h2>
              <p class="text-sm text-gray-600 mt-1">
                Actualiza tu información de contacto.
              </p>
            </div>

            <div class="p-6 space-y-4">
              <div v-if="isProfileLoading" class="p-4 bg-blue-50 border border-blue-200 text-blue-800 rounded-lg">
                Cargando tu información...
              </div>
              <div v-if="profileError" class="p-4 bg-red-50 border border-red-200 text-red-800 rounded-lg">
                {{ profileError }}
              </div>

              <div
                v-for="field in editableFields"
                :key="field.key"
                class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-4 rounded-lg border border-gray-200"
              >
                <div class="min-w-0">
                  <div class="text-sm font-medium text-gray-700">{{ field.label }}</div>
                  <div v-if="!editing[field.key]" class="text-gray-900 mt-1 break-words">
                    {{ profile[field.key] || '—' }}
                  </div>
                  <div v-else class="mt-2">
                    <input
                      v-model="draft[field.key]"
                      :type="field.type || 'text'"
                      class="w-full sm:w-96 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      :placeholder="field.placeholder"
                      :inputmode="field.key === 'cedula' ? 'numeric' : undefined"
                      :pattern="field.key === 'cedula' ? '\\\\d*' : undefined"
                      :maxlength="field.key === 'cedula' ? 10 : undefined"
                      @keydown="handleCedulaKeydown($event, field.key)"
                      @paste="handleCedulaPaste($event, field.key)"
                      @input="handleDraftInput(field.key)"
                    />
                    <div v-if="fieldErrors[field.key]" class="text-red-500 text-xs mt-1">
                      {{ fieldErrors[field.key] }}
                    </div>
                    <div v-if="fieldHelp[field.key]" class="text-xs text-gray-500 mt-1">
                      {{ fieldHelp[field.key] }}
                    </div>
                  </div>
                </div>

                <div class="flex items-center gap-2 shrink-0">
                  <button
                    v-if="!editing[field.key]"
                    class="px-4 py-2 border border-gray-300 hover:bg-gray-50 text-gray-800 rounded-lg transition-colors cursor-pointer"
                    @click="startEdit(field.key)"
                  >
                    <i class="fas fa-edit mr-2"></i>Editar
                  </button>

                  <template v-else>
                    <button
                      class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors cursor-pointer"
                      @click="saveField(field.key)"
                      :disabled="saving[field.key] || hasFieldError(field.key)"
                      :class="{ 'opacity-60 cursor-not-allowed': saving[field.key] || hasFieldError(field.key) }"
                    >
                      <i class="fas fa-save mr-2"></i>Guardar
                    </button>
                    <button
                      class="px-4 py-2 border border-gray-300 hover:bg-gray-50 text-gray-800 rounded-lg transition-colors cursor-pointer"
                      @click="cancelEdit(field.key)"
                      :disabled="saving[field.key]"
                      :class="{ 'opacity-60 cursor-not-allowed': saving[field.key] }"
                    >
                      Cancelar
                    </button>
                  </template>
                </div>
              </div>

              <div class="text-xs text-gray-500">
                Nota: los cambios se guardan campo por campo.
              </div>
            </div>
          </div>

          <!-- Deliveries -->
          <div v-else-if="activeSection === 'deliveries'" class="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div class="p-6 border-b border-gray-100">
              <h2 class="text-xl font-semibold text-gray-900">Mis entregas</h2>
              <p class="text-sm text-gray-600 mt-1">
                Consulta el estado de entrega, empresa transportista y número de guía.
              </p>
            </div>

            <div class="p-6 space-y-8">
              <div v-if="isDeliveriesLoading" class="p-4 bg-blue-50 border border-blue-200 text-blue-800 rounded-lg">
                Cargando entregas...
              </div>
              <div v-else-if="deliveriesError" class="p-4 bg-red-50 border border-red-200 text-red-800 rounded-lg">
                {{ deliveriesError }}
              </div>

              <template v-else>
                <!-- En proceso -->
                <div>
                  <div class="flex items-center justify-between gap-3 mb-3">
                    <h3 class="text-lg font-semibold text-gray-900">Entregas pendientes</h3>
                    <span class="text-xs font-semibold px-2 py-1 rounded-full bg-gray-100 text-gray-700">
                      {{ pendingDeliveries.length }}
                    </span>
                  </div>

                  <div v-if="pendingDeliveries.length === 0" class="text-gray-700 text-sm">
                    No tienes entregas en curso.
                  </div>

                  <div v-else class="space-y-3">
                    <button
                      v-for="d in pendingDeliveries"
                      :key="`pending-${d.id}`"
                      type="button"
                      class="w-full text-left p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
                      @click="goToOrderFromDelivery(d)"
                      :title="`Ver pedido #${d.id}`"
                    >
                      <div class="flex items-start justify-between gap-3">
                        <div class="min-w-0">
                          <div class="text-sm font-semibold text-gray-900">
                            Pedido #{{ d.id }}
                          </div>
                          <div class="text-xs text-gray-600 mt-1">
                            {{ d.date }}
                          </div>
                        </div>
                        <span
                          class="text-xs font-semibold px-2 py-1 rounded-full"
                          :class="deliveryStatusChipClass(d.deliveryStatus)"
                        >
                          {{ d.deliveryStatus || 'En proceso' }}
                        </span>
                      </div>

                      <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-2 mt-3 text-xs text-gray-700">
                        <div class="flex justify-between gap-3">
                          <span class="text-gray-500">Total</span>
                          <span class="font-semibold text-gray-900">{{ formatMoney(d.total) }}</span>
                        </div>
                        <div class="flex justify-between gap-3">
                          <span class="text-gray-500">Empresa</span>
                          <span class="font-medium">{{ d.carrierCompany || 'Sin asignar' }}</span>
                        </div>
                        <div class="flex justify-between gap-3">
                          <span class="text-gray-500">Guía</span>
                          <span class="font-medium">{{ d.trackingNumber || 'Sin asignar' }}</span>
                        </div>
                        <div class="text-gray-600 sm:col-span-2">
                          <span class="text-gray-500">Envío:</span>
                          <span class="ml-1">{{ d.shippingSummary || '—' }}</span>
                        </div>
                      </div>

                      <div class="mt-3 text-xs text-blue-700 font-medium inline-flex items-center gap-2">
                        Ver pedido
                        <i class="fas fa-arrow-right text-xs" aria-hidden="true"></i>
                      </div>
                    </button>
                  </div>
                </div>

                <!-- Entregados -->
                <div>
                  <div class="flex items-center justify-between gap-3 mb-3">
                    <h3 class="text-lg font-semibold text-gray-900">Entregas completadas</h3>
                    <span class="text-xs font-semibold px-2 py-1 rounded-full bg-gray-100 text-gray-700">
                      {{ completedDeliveries.length }}
                    </span>
                  </div>

                  <div v-if="completedDeliveries.length === 0" class="text-gray-700 text-sm">
                    Aún no tienes entregas completadas.
                  </div>

                  <div v-else class="space-y-3">
                    <button
                      v-for="d in completedDeliveries"
                      :key="`completed-${d.id}`"
                      type="button"
                      class="w-full text-left p-4 rounded-lg border border-gray-200 hover:bg-gray-50 transition-colors"
                      @click="goToOrderFromDelivery(d)"
                      :title="`Ver pedido #${d.id}`"
                    >
                      <div class="flex items-start justify-between gap-3">
                        <div class="min-w-0">
                          <div class="text-sm font-semibold text-gray-900">
                            Pedido #{{ d.id }}
                          </div>
                          <div class="text-xs text-gray-600 mt-1">
                            {{ d.date }}
                          </div>
                        </div>
                        <span
                          class="text-xs font-semibold px-2 py-1 rounded-full"
                          :class="deliveryStatusChipClass(d.deliveryStatus)"
                        >
                          {{ d.deliveryStatus || 'Entregado' }}
                        </span>
                      </div>

                      <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-2 mt-3 text-xs text-gray-700">
                        <div class="flex justify-between gap-3">
                          <span class="text-gray-500">Total</span>
                          <span class="font-semibold text-gray-900">{{ formatMoney(d.total) }}</span>
                        </div>
                        <div class="flex justify-between gap-3">
                          <span class="text-gray-500">Empresa</span>
                          <span class="font-medium">{{ d.carrierCompany || 'Sin asignar' }}</span>
                        </div>
                        <div class="flex justify-between gap-3">
                          <span class="text-gray-500">Guía</span>
                          <span class="font-medium">{{ d.trackingNumber || 'Sin asignar' }}</span>
                        </div>
                        <div class="text-gray-600 sm:col-span-2">
                          <span class="text-gray-500">Envío:</span>
                          <span class="ml-1">{{ d.shippingSummary || '—' }}</span>
                        </div>
                      </div>

                      <div class="mt-3 text-xs text-blue-700 font-medium inline-flex items-center gap-2">
                        Ver pedido
                        <i class="fas fa-arrow-right text-xs" aria-hidden="true"></i>
                      </div>
                    </button>
                  </div>
                </div>
              </template>
            </div>
          </div>

          <!-- Orders -->
          <div v-else-if="activeSection === 'orders'" class="grid grid-cols-1 xl:grid-cols-12 gap-6">
            <!-- Orders list -->
            <div class="xl:col-span-5 bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
              <div class="p-6 border-b border-gray-100">
                <h2 class="text-xl font-semibold text-gray-900">Mis pedidos</h2>
                <p class="text-sm text-gray-600 mt-1">
                  Aquí verás tus compras anteriores y sus comprobantes.
                </p>

                <div class="mt-4">
                  <button
                    type="button"
                    class="inline-flex items-center justify-center px-4 py-2 border border-gray-300 hover:bg-gray-50 text-gray-800 rounded-lg transition-colors cursor-pointer"
                    @click="refreshOrders"
                    :disabled="isOrdersLoading"
                    :class="{ 'opacity-60 cursor-not-allowed': isOrdersLoading }"
                  >
                    🔄 Actualizar Facturas/Estado
                  </button>
                </div>
              </div>

              <div class="divide-y divide-gray-100">
                <div v-if="isOrdersLoading" class="p-6">
                  <div class="p-4 bg-blue-50 border border-blue-200 text-blue-800 rounded-lg">
                    Cargando pedidos...
                  </div>
                </div>
                <div v-else-if="ordersError" class="p-6">
                  <div class="p-4 bg-red-50 border border-red-200 text-red-800 rounded-lg">
                    {{ ordersError }}
                  </div>
                </div>
                <div v-else-if="!orders || orders.length === 0" class="p-6 text-gray-700">
                  Aún no tienes pedidos.
                </div>
                <button
                  v-for="order in orders"
                  :key="order.id"
                  class="w-full text-left p-4 hover:bg-gray-50 transition-colors"
                  :class="selectedOrder && selectedOrder.id === order.id ? 'bg-blue-50' : ''"
                  @click="selectOrder(order)"
                >
                  <div class="flex items-start justify-between gap-3">
                    <div class="min-w-0">
                      <div class="text-sm font-semibold text-gray-900">
                        Pedido #{{ order.id }}
                      </div>
                      <div class="text-xs text-gray-600 mt-1">
                        {{ order.date }}
                      </div>
                    </div>
                    <span
                      class="text-xs font-semibold px-2 py-1 rounded-full"
                      :class="order.status === 'Pagado'
                        ? 'bg-green-100 text-green-700'
                        : (order.status === 'Cancelado'
                          ? 'bg-red-100 text-red-700'
                          : ((order.status === 'En revisión' || order.status === 'Pendiente') ? 'bg-amber-100 text-amber-800' : 'bg-gray-100 text-gray-700'))"
                    >
                      {{ (order.status === 'En revisión' || order.status === 'Pendiente')
                        ? 'Validando Pago'
                        : (order.status === 'Cancelado' ? 'Rechazado' : order.status) }}
                    </span>
                  </div>

                  <div class="mt-3 text-xs text-gray-700 flex items-center justify-between gap-3">
                    <div>
                      <span class="text-gray-500">Método:</span>
                      <span class="ml-1 font-medium">
                        {{ order.metodo_pago === 'Transferencia bancaria' ? 'Transferencia Bancaria' : 'Tarjeta Débito/Crédito' }}
                      </span>
                    </div>
                    <a
                      v-if="order.metodo_pago === 'Transferencia bancaria' && order.comprobante_transferencia_url"
                      :href="order.comprobante_transferencia_url"
                      target="_blank"
                      rel="noopener"
                      class="text-blue-700 hover:text-blue-800 font-medium"
                      @click.stop
                    >
                      Ver Comprobante
                    </a>
                  </div>

                  <div class="grid grid-cols-2 gap-x-4 gap-y-1 mt-3 text-xs text-gray-700">
                    <div class="flex justify-between">
                      <span class="text-gray-500">Subtotal</span>
                      <span class="font-medium">{{ formatMoney(order.subtotal) }}</span>
                    </div>
                    <div class="flex justify-between">
                      <span class="text-gray-500">Descuento</span>
                      <span class="font-medium">-{{ formatMoney(order.discount) }}</span>
                    </div>
                    <div class="flex justify-between">
                      <span class="text-gray-500">IVA</span>
                      <span class="font-medium">{{ formatMoney(order.iva) }}</span>
                    </div>
                    <div class="flex justify-between">
                      <span class="text-gray-500">Total</span>
                      <span class="font-semibold text-gray-900">{{ formatMoney(order.total) }}</span>
                    </div>
                  </div>
                </button>
              </div>
            </div>

            <!-- Invoice preview -->
            <div class="xl:col-span-7 bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
              <div class="p-6 border-b border-gray-100 flex items-center justify-between gap-3">
                <div>
                  <h3 class="text-lg font-semibold text-gray-900">Factura</h3>
                  <p class="text-sm text-gray-600 mt-1">
                    Vista previa del comprobante en PDF.
                  </p>
                </div>
                <div class="flex items-center gap-2">
                  <a
                    v-if="selectedOrderPdfUrlDownload && selectedOrder && selectedOrder.status === 'Pagado'"
                    :href="selectedOrderPdfUrlDownload"
                    class="inline-flex items-center justify-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors cursor-pointer"
                  >
                    <i class="fas fa-download mr-2"></i>Descargar
                  </a>
                  <button
                    v-if="selectedOrder && selectedOrder.status === 'Pagado'"
                    class="inline-flex items-center justify-center px-4 py-2 border border-gray-300 hover:bg-gray-50 text-gray-800 rounded-lg transition-colors cursor-pointer"
                    @click="regenerateSelectedOrderPdf"
                    :disabled="isInvoiceLoading"
                    :class="{ 'opacity-60 cursor-not-allowed': isInvoiceLoading }"
                  >
                    <i class="fas fa-sync-alt mr-2"></i>Actualizar link
                  </button>
                </div>
              </div>

              <div class="p-6">
                <div v-if="!selectedOrder" class="text-gray-700">
                  Selecciona un pedido para ver su factura.
                </div>

                <div v-else>
                  <div v-if="isInvoiceLoading" class="p-4 bg-blue-50 border border-blue-200 text-blue-800 rounded-lg">
                    Cargando comprobante...
                  </div>
                  <div v-if="invoiceError" class="p-4 bg-red-50 border border-red-200 text-red-800 rounded-lg mt-4">
                    {{ invoiceError }}
                  </div>

                  <div
                    v-if="selectedOrder && selectedOrder.status === 'Cancelado'"
                    class="p-4 bg-red-50 border border-red-200 text-red-900 rounded-lg mt-4"
                  >
                    <div class="font-semibold">Tu comprobante fue rechazado.</div>
                    <div class="text-sm text-red-900 mt-1">
                      <template v-if="selectedOrder.motivo_cancelacion">
                        Motivo: <span class="font-medium">{{ selectedOrder.motivo_cancelacion }}</span>
                      </template>
                      <template v-else>
                        Si crees que fue un error, puedes reenviar el comprobante para revisión.
                      </template>
                    </div>

                    <div
                      v-if="selectedOrder.metodo_pago === 'Transferencia bancaria'"
                      class="mt-4 bg-white rounded-lg border border-red-200 p-4"
                    >
                      <div class="text-sm font-semibold text-gray-900">Reenviar comprobante (Transferencia bancaria)</div>
                      <div class="mt-2 space-y-1 text-sm text-gray-700">
                        <div><span class="font-semibold">Banco:</span> Banco de Loja</div>
                        <div><span class="font-semibold">N. Cuenta:</span> 2902563522</div>
                        <div><span class="font-semibold">Tipo de cuenta:</span> Cuenta de ahorros</div>
                        <div><span class="font-semibold">Nombre:</span> Aarón Robles</div>
                      </div>

                      <div class="mt-4">
                        <label for="resubmit-transfer-proof" class="block text-sm font-medium text-gray-700 mb-2">
                          Subir comprobante (solo imágenes)
                        </label>
                        <input
                          id="resubmit-transfer-proof"
                          ref="resubmitTransferProofInput"
                          name="comprobante_transferencia"
                          type="file"
                          accept="image/*"
                          class="block w-full text-sm text-gray-500
                            file:mr-4 file:py-2 file:px-4
                            file:rounded-full file:border-0
                            file:text-sm file:font-semibold
                            file:bg-blue-50 file:text-blue-700
                            hover:file:bg-blue-100"
                          @change="handleResubmitTransferProof"
                        />
                        <div v-if="resubmitTransferProofPreviewUrl" class="mt-3">
                          <div class="text-xs text-gray-500 mb-2">Vista previa</div>
                          <img
                            :src="resubmitTransferProofPreviewUrl"
                            alt="Vista previa del comprobante"
                            class="w-full max-w-md rounded-lg border border-gray-200 object-contain bg-gray-50"
                            style="max-height: 240px;"
                          />
                        </div>
                        <p v-if="resubmitTransferProofFile" class="mt-2 text-sm text-gray-600">
                          Archivo seleccionado: {{ resubmitTransferProofFile.name }}
                        </p>
                        <p v-if="resubmitTransferProofError" class="mt-1 text-xs text-red-600">
                          {{ resubmitTransferProofError }}
                        </p>

                        <div class="mt-4 flex flex-col sm:flex-row gap-3">
                          <button
                            type="button"
                            class="inline-flex items-center justify-center px-5 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors cursor-pointer"
                            :disabled="isResubmittingTransferProof"
                            :class="{ 'opacity-60 cursor-not-allowed': isResubmittingTransferProof }"
                            @click="submitResubmittedTransferProof"
                          >
                            <i v-if="isResubmittingTransferProof" class="fas fa-spinner fa-spin mr-2" aria-hidden="true"></i>
                            <i v-else class="fas fa-upload mr-2" aria-hidden="true"></i>
                            Reenviar comprobante
                          </button>
                          <button
                            type="button"
                            class="inline-flex items-center justify-center px-5 py-3 border border-gray-300 hover:bg-gray-50 text-gray-800 rounded-lg transition-colors cursor-pointer"
                            :disabled="isResubmittingTransferProof"
                            :class="{ 'opacity-60 cursor-not-allowed': isResubmittingTransferProof }"
                            @click="refreshOrders"
                          >
                            <i class="fas fa-sync-alt mr-2" aria-hidden="true"></i>
                            Actualizar estado
                          </button>
                        </div>

                        <div class="text-xs text-gray-500 mt-2">
                          Nota: revisaremos el comprobante y te notificaremos por correo cuando cambie el estado del pedido.
                        </div>
                      </div>
                    </div>
                  </div>

                  <div
                    v-else-if="selectedOrder && (selectedOrder.status === 'En revisión' || selectedOrder.status === 'Pendiente')"
                    class="p-4 bg-amber-50 border border-amber-200 text-amber-900 rounded-lg mt-4"
                  >
                    Tu pedido está pendiente de verificación. Estamos validando tu pago y, cuando se confirme, podrás ver y descargar tu factura aquí.
                    Te notificaremos por correo electrónico una vez esté listo.

                    <div
                      v-if="selectedOrder.metodo_pago === 'Transferencia bancaria'"
                      class="mt-4 bg-white rounded-lg border border-amber-200 p-4"
                    >
                      <div class="text-sm font-semibold text-gray-900">Reenviar comprobante (Transferencia bancaria)</div>
                      <div class="text-xs text-gray-600 mt-1">
                        Si necesitas reenviar una foto más clara, puedes subir un nuevo comprobante aquí.
                      </div>

                      <div class="mt-3 space-y-1 text-sm text-gray-700">
                        <div><span class="font-semibold">Banco:</span> Banco de Loja</div>
                        <div><span class="font-semibold">N. Cuenta:</span> 2902563522</div>
                        <div><span class="font-semibold">Tipo de cuenta:</span> Cuenta de ahorros</div>
                        <div><span class="font-semibold">Nombre:</span> Aarón Robles</div>
                      </div>

                      <div class="mt-4">
                        <label for="resubmit-transfer-proof" class="block text-sm font-medium text-gray-700 mb-2">
                          Subir comprobante (solo imágenes)
                        </label>
                        <input
                          id="resubmit-transfer-proof"
                          ref="resubmitTransferProofInput"
                          name="comprobante_transferencia"
                          type="file"
                          accept="image/*"
                          class="block w-full text-sm text-gray-500
                            file:mr-4 file:py-2 file:px-4
                            file:rounded-full file:border-0
                            file:text-sm file:font-semibold
                            file:bg-blue-50 file:text-blue-700
                            hover:file:bg-blue-100"
                          @change="handleResubmitTransferProof"
                        />

                        <div v-if="resubmitTransferProofPreviewUrl" class="mt-3">
                          <div class="text-xs text-gray-500 mb-2">Vista previa</div>
                          <img
                            :src="resubmitTransferProofPreviewUrl"
                            alt="Vista previa del comprobante"
                            class="w-full max-w-md rounded-lg border border-gray-200 object-contain bg-gray-50"
                            style="max-height: 240px;"
                          />
                        </div>

                        <p v-if="resubmitTransferProofFile" class="mt-2 text-sm text-gray-600">
                          Archivo seleccionado: {{ resubmitTransferProofFile.name }}
                        </p>
                        <p v-if="resubmitTransferProofError" class="mt-1 text-xs text-red-600">
                          {{ resubmitTransferProofError }}
                        </p>

                        <div class="mt-4 flex flex-col sm:flex-row gap-3">
                          <button
                            type="button"
                            class="inline-flex items-center justify-center px-5 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors cursor-pointer"
                            :disabled="isResubmittingTransferProof"
                            :class="{ 'opacity-60 cursor-not-allowed': isResubmittingTransferProof }"
                            @click="submitResubmittedTransferProof"
                          >
                            <i v-if="isResubmittingTransferProof" class="fas fa-spinner fa-spin mr-2" aria-hidden="true"></i>
                            <i v-else class="fas fa-upload mr-2" aria-hidden="true"></i>
                            Reenviar comprobante
                          </button>
                          <button
                            type="button"
                            class="inline-flex items-center justify-center px-5 py-3 border border-gray-300 hover:bg-gray-50 text-gray-800 rounded-lg transition-colors cursor-pointer"
                            :disabled="isResubmittingTransferProof"
                            :class="{ 'opacity-60 cursor-not-allowed': isResubmittingTransferProof }"
                            @click="refreshOrders"
                          >
                            <i class="fas fa-sync-alt mr-2" aria-hidden="true"></i>
                            Actualizar estado
                          </button>
                        </div>

                        <div class="text-xs text-gray-500 mt-2">
                          Nota: revisaremos el comprobante y te notificaremos por correo cuando cambie el estado del pedido.
                        </div>
                      </div>
                    </div>
                  </div>

                  <div v-else-if="selectedOrderPdfUrl" class="w-full bg-gray-50 border rounded-lg overflow-hidden mt-4">
                    <iframe
                      :src="selectedOrderPdfUrl"
                      title="Comprobante del pedido"
                      class="w-full"
                      style="height: 75vh;"
                    ></iframe>
                  </div>

                  <div v-else-if="!isInvoiceLoading" class="text-gray-700 mt-4">
                    <template v-if="selectedOrder && selectedOrder.status !== 'Pagado'">
                      La factura aún no está disponible para este pedido. Cuando el pago se confirme, aparecerá aquí.
                    </template>
                    <template v-else>
                      No pudimos cargar la factura en este momento. Intenta presionar “Actualizar link” o vuelve a intentarlo más tarde.
                    </template>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>
    </div>

    <!-- Si no está autenticado, no mostramos datos de perfil/pedidos (evita ver información previa) -->
    <div v-else class="max-w-7xl mx-auto px-6 py-16">
      <div class="text-gray-600 text-sm">
        Debes iniciar sesión para ver tu cuenta.
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/utils/api';
import { mapGetters, mapActions } from 'vuex';
import { getProfileFieldError, onlyDigits as onlyDigitsProfile } from '@/utils/profileValidators';

export default {
  name: 'MyAccountPage',
  computed: {
    ...mapGetters(['getUser', 'isAuthenticated']),
    displayName() {
      return this.profile.nombre || this.getUser?.username || 'Mi cuenta';
    },
    customerTypeLabel() {
      // Backend: tipo_cliente puede venir como "Persona" o "Empresa".
      // En UI: Persona => Natural, Empresa (o Mayorista) => Mayorista.
      const raw = String(this.profile.tipo_cliente || '').toLowerCase();
      if (raw.includes('empresa') || raw.includes('mayorista')) return 'Mayorista';
      return 'Natural';
    },
    canResubmitTransferProof() {
      const status = this.selectedOrder?.status;
      const metodo = this.selectedOrder?.metodo_pago;
      return (
        Boolean(this.selectedOrder?.id) &&
        metodo === 'Transferencia bancaria' &&
        (status === 'Cancelado' || status === 'Pendiente' || status === 'En revisión')
      );
    },
  },
  data() {
    return {
      activeSection: 'profile',
      avatarUrl: '', // placeholder (luego puedes setear la foto real)
      toast: {
        visible: false,
        message: '',
        type: 'success'
      },
      profile: {
        // No editables (backend)
        id: null,
        nombre: '',
        tipo_cliente: '',
        // Editables
        cedula: '',
        telefono: '',
        email: '',
        ciudad: '',
        direccion: '',
      },
      editableFields: [
        { key: 'cedula', label: 'Cédula', placeholder: 'Ej: 1710020030' },
        { key: 'telefono', label: 'Teléfono', placeholder: 'Ej: 3001234567' },
        { key: 'email', label: 'Email', type: 'email', placeholder: 'Ej: cliente@email.com' },
        { key: 'ciudad', label: 'Ciudad', placeholder: 'Ej: Medellín' },
        { key: 'direccion', label: 'Dirección', placeholder: 'Ej: Calle 10 # 20-30' },
      ],
      fieldHelp: {
        cedula: 'Solo números.',
        telefono: 'Incluye indicativo si aplica.',
      },
      editing: {},
      draft: {},
      saving: {},
      fieldErrors: {},
      isProfileLoading: false,
      profileError: '',

      // Pedidos (backend)
      orders: [],
      isOrdersLoading: false,
      ordersError: '',
      ordersLoaded: false,
      selectedOrder: null,
      selectedOrderPdfUrl: '',
      selectedOrderPdfUrlDownload: '',
      isInvoiceLoading: false,
      invoiceError: '',
      // Re-subir comprobante (solo para Transferencia bancaria cuando está Cancelado/Rechazado)
      resubmitTransferProofFile: null,
      resubmitTransferProofError: '',
      isResubmittingTransferProof: false,
      resubmitTransferProofPreviewUrl: '',

      // Entregas (tracking)
      pendingDeliveries: [],
      completedDeliveries: [],
      isDeliveriesLoading: false,
      deliveriesError: '',
      deliveriesLoaded: false,
    };
  },
  created() {
    if (this.isAuthenticated) {
      this.fetchProfile();
      // No cargamos pedidos de entrada para evitar llamadas innecesarias;
      // se cargan al abrir la pestaña Pedidos.
      this.applySectionFromRoute();
    } else {
      // Asegura que no quede data anterior si alguien abre /mi-cuenta sin auth.
      this.resetPrivateState();
    }
  },
  watch: {
    isAuthenticated(newVal) {
      if (!newVal) {
        this.resetPrivateState();
      } else {
        // Si vuelve a autenticarse y hay query de sección, la aplicamos
        this.applySectionFromRoute();
      }
    },
    '$route.query.section'() {
      // Permite deep-link directo a una sección (ej: /mi-cuenta?section=deliveries)
      this.applySectionFromRoute();
    },
    activeSection(newVal) {
      if (newVal === 'orders' && this.isAuthenticated && !this.ordersLoaded) {
        this.fetchOrders();
      }
      if (newVal === 'deliveries' && this.isAuthenticated && !this.deliveriesLoaded) {
        this.fetchDeliveries();
      }
    }
  },
  methods: {
    ...mapActions(['logout']),
    showToast(message, type = 'success') {
      this.toast.message = message;
      this.toast.type = type;
      this.toast.visible = true;
      setTimeout(() => {
        this.toast.visible = false;
      }, 1500);
    },
    resetPrivateState() {
      // Limpia cualquier dato sensible para evitar que se vea al volver/pegar la URL sin sesión
      this.activeSection = 'profile';

      this.profile = {
        id: null,
        nombre: '',
        tipo_cliente: '',
        cedula: '',
        telefono: '',
        email: '',
        ciudad: '',
        direccion: '',
      };

      this.profileError = '';
      this.isProfileLoading = false;

      this.editing = {};
      this.draft = {};
      this.saving = {};

      this.orders = [];
      this.isOrdersLoading = false;
      this.ordersError = '';
      this.ordersLoaded = false;

      this.selectedOrder = null;
      this.selectedOrderPdfUrl = '';
      this.selectedOrderPdfUrlDownload = '';
      this.isInvoiceLoading = false;
      this.invoiceError = '';
      this.resubmitTransferProofFile = null;
      this.resubmitTransferProofError = '';
      this.isResubmittingTransferProof = false;
      // Liberar URL de preview si existía
      if (this.resubmitTransferProofPreviewUrl) {
        try { URL.revokeObjectURL(this.resubmitTransferProofPreviewUrl); } catch (e) { /* noop */ }
      }
      this.resubmitTransferProofPreviewUrl = '';

      this.pendingDeliveries = [];
      this.completedDeliveries = [];
      this.isDeliveriesLoading = false;
      this.deliveriesError = '';
      this.deliveriesLoaded = false;
    },
    applySectionFromRoute() {
      if (!this.isAuthenticated) return;
      const section = String(this.$route?.query?.section || '').toLowerCase();
      if (section === 'deliveries') this.activeSection = 'deliveries';
      if (section === 'orders') this.activeSection = 'orders';
      if (section === 'profile') this.activeSection = 'profile';
    },
    deliveryStatusChipClass(status) {
      const raw = String(status || '').toLowerCase();
      if (raw.includes('entregado')) return 'bg-green-100 text-green-700';
      if (raw.includes('proceso') || raw.includes('pendiente')) return 'bg-amber-100 text-amber-800';
      return 'bg-blue-100 text-blue-700';
    },
    normalizeShippingSummary(o) {
      const city = String(o?.ciudad_envio || '').trim();
      const address = String(o?.direccion_envio || '').trim();
      const house = String(o?.numero_casa_envio || '').trim();

      const parts = [];
      if (city) parts.push(city);
      if (address && house) parts.push(`${address} · ${house}`);
      else if (address) parts.push(address);
      else if (house) parts.push(house);

      return parts.join(' — ');
    },
    mapDeliveryOrder(o) {
      return {
        id: o?.id,
        date: o?.fecha_pedido || '',
        total: Number.parseFloat(o?.total ?? 0) || 0,
        deliveryStatus: o?.estado_entrega || '',
        carrierCompany: o?.transportista_empresa || '',
        trackingNumber: o?.transportista_numero_guia || '',
        shippingSummary: this.normalizeShippingSummary(o),
      };
    },
    async fetchDeliveries() {
      if (this.isDeliveriesLoading) return;
      this.isDeliveriesLoading = true;
      this.deliveriesError = '';
      try {
        const [pendingRes, completedRes] = await Promise.all([
          api.get('/mis-pedidos/?entrega=en_proceso'),
          api.get('/mis-pedidos/?entrega=entregados'),
        ]);

        const pendingList = Array.isArray(pendingRes?.data) ? pendingRes.data : [];
        const completedList = Array.isArray(completedRes?.data) ? completedRes.data : [];

        this.pendingDeliveries = pendingList.map(this.mapDeliveryOrder);
        this.completedDeliveries = completedList.map(this.mapDeliveryOrder);
        this.deliveriesLoaded = true;
      } catch (e) {
        console.error('Error cargando entregas:', e);
        this.deliveriesError = 'No se pudieron cargar tus entregas. Por favor intenta nuevamente.';
      } finally {
        this.isDeliveriesLoading = false;
      }
    },
    async goToOrderFromDelivery(delivery) {
      const orderId = delivery?.id;
      if (!orderId) return;

      // Cambia a la sección de Pedidos y selecciona el pedido
      this.activeSection = 'orders';

      // Asegura que exista listado (para resaltar en UI si aparece)
      if (this.isAuthenticated && !this.ordersLoaded) {
        await this.fetchOrders();
      }

      const found = Array.isArray(this.orders) ? this.orders.find(o => o.id === orderId) : null;
      const orderForSelection = found || { id: orderId, date: delivery?.date || '', status: '', subtotal: 0, discount: 0, iva: 0, total: delivery?.total || 0 };
      await this.selectOrder(orderForSelection);
    },
    async fetchProfile() {
      if (this.isProfileLoading) return;
      this.isProfileLoading = true;
      this.profileError = '';
      try {
        const res = await api.get('/mi-perfil/');
        const data = res?.data || {};

        // Rellenar campos. Si viene null, usar ''.
        this.profile.id = data.id ?? null;
        this.profile.nombre = data.nombre ?? '';
        this.profile.tipo_cliente = data.tipo_cliente ?? '';
        this.profile.cedula = data.cedula ?? '';
        this.profile.telefono = data.telefono ?? '';
        this.profile.email = data.email ?? '';
        this.profile.ciudad = data.ciudad ?? '';
        this.profile.direccion = data.direccion ?? '';
      } catch (e) {
        console.error('Error cargando mi perfil:', e);
        this.profileError = 'No se pudo cargar tu perfil. Por favor intenta nuevamente.';
      } finally {
        this.isProfileLoading = false;
      }
    },
    async fetchOrders() {
      if (this.isOrdersLoading) return;
      this.isOrdersLoading = true;
      this.ordersError = '';
      try {
        const res = await api.get('/mis-pedidos/');
        const list = Array.isArray(res?.data) ? res.data : [];

        this.orders = list.map(o => ({
          id: o.id,
          date: o.fecha_pedido || '',
          status: o.estado_pedido || '',
          metodo_pago: o.metodo_pago || 'Tarjeta',
          comprobante_transferencia_url: o.comprobante_transferencia_url || '',
          motivo_cancelacion: o.motivo_cancelacion || '',
          subtotal: Number.parseFloat(o.subtotal ?? 0) || 0,
          discount: Number.parseFloat(o.descuento ?? 0) || 0,
          iva: Number.parseFloat(o.iva ?? 0) || 0,
          total: Number.parseFloat(o.total ?? 0) || 0,
        }));
        this.ordersLoaded = true;
      } catch (e) {
        console.error('Error cargando pedidos:', e);
        this.ordersError = 'No se pudieron cargar tus pedidos. Por favor intenta nuevamente.';
      } finally {
        this.isOrdersLoading = false;
      }
    },
    async refreshOrders() {
      // Botón de refresco manual para ver cambios (ej: admin aprobó transferencia)
      this.ordersLoaded = false;
      await this.fetchOrders();

      // Si hay un pedido seleccionado, refrescamos su versión (y el panel de factura)
      if (this.selectedOrder?.id) {
        const updated = Array.isArray(this.orders) ? this.orders.find(o => o.id === this.selectedOrder.id) : null;
        if (updated) {
          this.selectedOrder = updated;
        }
        // Si está pagado, intentamos refrescar link; si está en revisión, limpiamos links
        if (this.selectedOrder?.status === 'Pagado') {
          await this.regenerateSelectedOrderPdf();
        } else {
          this.selectedOrderPdfUrl = '';
          this.selectedOrderPdfUrlDownload = '';
        }
      }
    },
    formatMoney(value) {
      const number = Number(value || 0);
      try {
        return new Intl.NumberFormat('es-CO', { style: 'currency', currency: 'COP' }).format(number);
      } catch (e) {
        return `$${number.toFixed(0)}`;
      }
    },
    startEdit(key) {
      this.$set(this.editing, key, true);
      this.$set(this.draft, key, this.profile[key] || '');
      // Inicializa el error del campo al entrar en modo edición
      this.$set(this.fieldErrors, key, '');
      this.validateDraftField(key);
    },
    cancelEdit(key) {
      this.$set(this.editing, key, false);
      this.$set(this.draft, key, this.profile[key] || '');
      this.$set(this.fieldErrors, key, '');
    },
    normalizeDraftValue(key, value) {
      // Normalización mínima para enviar al backend (mantiene la UI libre de "magia")
      if (key === 'cedula' || key === 'telefono') return onlyDigitsProfile(value);
      if (key === 'email') return String(value ?? '').trim();
      return value;
    },
    validateDraftField(key) {
      const rawValue = this.draft?.[key];
      const error = getProfileFieldError(key, rawValue);
      this.$set(this.fieldErrors, key, error);
      return !error;
    },
    hasFieldError(key) {
      return Boolean(this.fieldErrors?.[key]);
    },
    handleDraftInput(key) {
      // Reglas "estrictas" pedidas:
      // - Teléfono: solo números
      // - Cédula: solo números y máximo 10 dígitos
      if (key === 'cedula') {
        const cleaned = String(this.draft?.[key] ?? '').replace(/[^0-9]/g, '').slice(0, 10);
        this.$set(this.draft, key, cleaned);
      }
      if (key === 'telefono') {
        const cleaned = onlyDigitsProfile(this.draft?.[key]);
        this.$set(this.draft, key, cleaned);
      }
      if (key === 'email') {
        // No recortamos espacios internos, solo trim general
        this.$set(this.draft, key, String(this.draft?.[key] ?? '').trim());
      }
      this.validateDraftField(key);
    },
    handleCedulaKeydown(event, key) {
      if (key !== 'cedula') return;

      // Permitir teclas de control/navegación
      const allowedKeys = new Set([
        'Backspace',
        'Delete',
        'Tab',
        'ArrowLeft',
        'ArrowRight',
        'ArrowUp',
        'ArrowDown',
        'Home',
        'End',
      ]);
      if (allowedKeys.has(event.key)) return;

      // Permitir atajos comunes (copiar/pegar/cortar/seleccionar todo/deshacer/rehacer)
      if (event.ctrlKey || event.metaKey) {
        const k = String(event.key || '').toLowerCase();
        if (['a', 'c', 'v', 'x', 'z', 'y'].includes(k)) return;
      }

      // Bloquear cualquier tecla que no sea un dígito
      if (!/^\d$/.test(event.key)) {
        event.preventDefault();
      }
    },
    handleCedulaPaste(event, key) {
      if (key !== 'cedula') return;
      event.preventDefault();

      const text = event.clipboardData?.getData('text') ?? '';
      const pastedDigits = String(text).replace(/[^0-9]/g, '');

      const current = String(this.draft?.cedula ?? '');
      const merged = `${current}${pastedDigits}`.replace(/[^0-9]/g, '').slice(0, 10);
      this.$set(this.draft, 'cedula', merged);

      this.validateDraftField('cedula');
    },
    async saveField(key) {
      // Validación estricta antes de permitir "Guardar"
      const isValid = this.validateDraftField(key);
      if (!isValid) return;

      this.$set(this.saving, key, true);
      try {
        // PATCH por campo: enviamos solo la llave editada
        const normalized = this.normalizeDraftValue(key, this.draft[key]);
        await api.patch('/mi-perfil/', { [key]: normalized });

        this.$set(this.profile, key, normalized);
        this.$set(this.editing, key, false);
      } catch (e) {
        console.error('Error guardando campo de perfil:', e);
        this.profileError = 'No se pudo guardar el cambio. Por favor intenta nuevamente.';
      } finally {
        this.$set(this.saving, key, false);
      }
    },
    handleLogoutClick() {
      // Cierra sesión: borra token (localStorage) + resetea estado auth (Vuex)
      this.logout();
      this.resetPrivateState();
      this.showToast('La sesión se ha cerrado', 'success');
      setTimeout(() => {
        this.$router.push('/');
      }, 900);
    },
    async selectOrder(order) {
      this.selectedOrder = order;
      this.selectedOrderPdfUrl = '';
      this.selectedOrderPdfUrlDownload = '';
      this.invoiceError = '';
      // Reset del formulario de re-subida al cambiar de pedido
      this.resubmitTransferProofFile = null;
      this.resubmitTransferProofError = '';
      if (this.resubmitTransferProofPreviewUrl) {
        try { URL.revokeObjectURL(this.resubmitTransferProofPreviewUrl); } catch (e) { /* noop */ }
      }
      this.resubmitTransferProofPreviewUrl = '';

      // Cargar el comprobante del pedido seleccionado
      await this.regenerateSelectedOrderPdf();
    },
    handleResubmitTransferProof(event) {
      const file = event?.target?.files?.[0];
      this.resubmitTransferProofError = '';

      if (!file) {
        this.resubmitTransferProofFile = null;
        if (this.resubmitTransferProofPreviewUrl) {
          try { URL.revokeObjectURL(this.resubmitTransferProofPreviewUrl); } catch (e) { /* noop */ }
        }
        this.resubmitTransferProofPreviewUrl = '';
        return;
      }

      if (!file.type || !String(file.type).startsWith('image/')) {
        this.resubmitTransferProofFile = null;
        this.resubmitTransferProofError = 'Solo se permiten archivos de imagen.';
        if (this.resubmitTransferProofPreviewUrl) {
          try { URL.revokeObjectURL(this.resubmitTransferProofPreviewUrl); } catch (e) { /* noop */ }
        }
        this.resubmitTransferProofPreviewUrl = '';
        return;
      }

      this.resubmitTransferProofFile = file;
      if (this.resubmitTransferProofPreviewUrl) {
        try { URL.revokeObjectURL(this.resubmitTransferProofPreviewUrl); } catch (e) { /* noop */ }
      }
      this.resubmitTransferProofPreviewUrl = URL.createObjectURL(file);
    },
    async submitResubmittedTransferProof() {
      if (!this.selectedOrder?.id) {
        this.showToast('Selecciona un pedido antes de reenviar el comprobante.', 'error');
        return;
      }
      if (this.isResubmittingTransferProof) {
        this.showToast('Ya se esta reenviando el comprobante. Espera un momento.', 'error');
        return;
      }
      if (!this.resubmitTransferProofFile) {
        this.showToast('Selecciona una imagen antes de reenviar el comprobante.', 'error');
        return;
      }
      if (this.resubmitTransferProofError) {
        this.showToast(this.resubmitTransferProofError, 'error');
        return;
      }
      if (!this.isAuthenticated) {
        this.showToast('Debes iniciar sesión para reenviar el comprobante.', 'error');
        return;
      }

      this.isResubmittingTransferProof = true;
      try {
        const form = new FormData();
        // Campo oficial: comprobante_transferencia (backend también acepta comprobante/archivo por compatibilidad)
        form.append('comprobante_transferencia', this.resubmitTransferProofFile);
        form.append('comprobante', this.resubmitTransferProofFile);
        form.append('archivo', this.resubmitTransferProofFile);

        console.info('[MyAccount] Reenviando comprobante', {
          pedidoId: this.selectedOrder.id,
          fileName: this.resubmitTransferProofFile?.name,
          fileType: this.resubmitTransferProofFile?.type,
          fileSize: this.resubmitTransferProofFile?.size,
        });

        await api.post(`/mis-pedidos/${this.selectedOrder.id}/comprobante-transferencia/`, form, {
          headers: { 'Content-Type': 'multipart/form-data' },
        });

        this.resubmitTransferProofFile = null;
        this.resubmitTransferProofError = '';
        if (this.resubmitTransferProofPreviewUrl) {
          try { URL.revokeObjectURL(this.resubmitTransferProofPreviewUrl); } catch (e) { /* noop */ }
        }
        this.resubmitTransferProofPreviewUrl = '';
        this.showToast('Comprobante enviado. Lo revisaremos y te notificaremos por correo.', 'success');

        // Refresca listado y panel para reflejar el nuevo estado (ej: vuelve a "Pendiente/En revisión")
        await this.refreshOrders();
      } catch (e) {
        console.error('Error re-subiendo comprobante de transferencia:', e);
        const statusCode = e?.response?.status;
        const backendError = e?.response?.data?.error;
        const message = backendError
          ? String(backendError)
          : statusCode
            ? `No se pudo reenviar el comprobante (HTTP ${statusCode}).`
            : 'No se pudo reenviar el comprobante. Por favor intenta nuevamente.';
        this.showToast(message, 'error');
      } finally {
        this.isResubmittingTransferProof = false;
      }
    },
    resubmitPanelBorderClass() {
      const status = this.selectedOrder?.status;
      if (status === 'Cancelado') return 'border-red-200';
      if (status === 'Pendiente' || status === 'En revisión') return 'border-amber-200';
      return 'border-gray-200';
    },
    async regenerateSelectedOrderPdf() {
      if (!this.selectedOrder?.id) return;
      if (!this.isAuthenticated) {
        this.invoiceError = 'Debes iniciar sesión para ver el comprobante.';
        return;
      }
      if (this.selectedOrder?.status !== 'Pagado') {
        // No es un error: la factura se genera cuando el pago esté confirmado.
        this.selectedOrderPdfUrl = '';
        this.selectedOrderPdfUrlDownload = '';
        this.invoiceError = '';
        return;
      }
      if (this.isInvoiceLoading) return;

      this.isInvoiceLoading = true;
      this.invoiceError = '';
      try {
        const linkRes = await api.get(`/mis-pedidos/${this.selectedOrder.id}/comprobante/link/`);
        this.selectedOrderPdfUrl = linkRes?.data?.pdf_url || '';
        this.selectedOrderPdfUrlDownload = linkRes?.data?.pdf_url_download || '';
        if (!this.selectedOrderPdfUrl || !this.selectedOrderPdfUrlDownload) {
          throw new Error('No se recibieron links del comprobante.');
        }
      } catch (e) {
        console.error('Error cargando comprobante del pedido:', e);
        this.invoiceError = 'No se pudo cargar el comprobante de este pedido.';
      } finally {
        this.isInvoiceLoading = false;
      }
    },
  },
};
</script>

<style scoped>
</style>
