import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'; // Importamos el store de Vuex
import "./assets/tailwind.css";

Vue.config.productionTip = false

new Vue({
  router,
  store, // Añadimos el store a la instancia de Vue
  beforeCreate() {
    // Intentar restaurar el estado de autenticación desde localStorage al iniciar la aplicación
    const token = localStorage.getItem('user-token');
    if (token) {
      // Aquí, idealmente, deberías validar el token con tu backend para obtener los datos del usuario
      // Por ahora, asumimos que si hay un token, el usuario está logeado (simplificado)
      this.$store.commit('SET_AUTH_DATA', { isLoggedIn: true, user: null, token: token });
      // Si tu token contiene información codificada del usuario, podrías decodificarla aquí
      // y pasarla a 'user'
    }
  },
  render: h => h(App),
}).$mount('#app')
