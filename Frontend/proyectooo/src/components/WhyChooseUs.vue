<template>
  <section class="py-20 bg-slate-900 text-white">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="text-center mb-16">
        <h2 class="text-4xl font-bold mb-4">¿Por qué elegir Santiago?</h2>
        <p class="text-xl text-slate-300">Más de 35 años siendo tu papelería de confianza</p>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
        <div 
          v-for="benefit in benefits" 
          :key="benefit.id"
          class="text-center group"
        >
          <div 
            :class="benefit.bgClass"
            class="w-20 h-20 rounded-2xl flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform"
          >
            <i :class="benefit.icon" class="text-3xl text-white"></i>
          </div>
          <h3 class="text-xl font-bold mb-3">{{ benefit.title }}</h3>
          <p class="text-slate-400">{{ benefit.description }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'WhyChooseUs',
  data() {
    return {
      benefits: [
        {
          id: 1,
          title: 'Envío Gratuito',
          description: 'En compras superiores a $50.000 en toda Colombia',
          icon: 'fas fa-truck',
          bgClass: 'bg-gradient-to-br from-blue-500 to-blue-600'
        },
        {
          id: 2,
          title: 'Calidad Premium',
          description: 'Productos de las mejores marcas internacionales',
          icon: 'fas fa-medal',
          bgClass: 'bg-gradient-to-br from-yellow-400 to-yellow-500'
        },
        {
          id: 3,
          title: 'Entrega Rápida',
          description: 'Recibe tus pedidos en máximo 3 días hábiles',
          icon: 'fas fa-clock',
          bgClass: 'bg-gradient-to-br from-green-500 to-green-600'
        },
        {
          id: 4,
          title: 'Soporte Experto',
          description: 'Asesoría personalizada de lunes a sábado',
          icon: 'fas fa-headset',
          bgClass: 'bg-gradient-to-br from-purple-500 to-purple-600'
        }
      ]
    }
  }
}
</script>

<style scoped>
</style>