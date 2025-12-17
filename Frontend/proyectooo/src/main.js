import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'; // Importamos el store de Vuex
import "./assets/tailwind.css";

Vue.config.productionTip = false

new Vue({
  router,
  store, // Añadimos el store a la instancia de Vue
  render: h => h(App),
}).$mount('#app')
