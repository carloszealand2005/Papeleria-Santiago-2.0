import Vue from 'vue';
import Vuex from 'vuex';
import api from '@/utils/api'; // Importamos la instancia de axios configurada

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    isLoggedIn: false,
    token: null, // Para almacenar el token de autenticación
    user: null, // Para almacenar la información del usuario logeado
  },
  mutations: {
    SET_AUTH_DATA(state, { isLoggedIn, user, token }) {
      state.isLoggedIn = isLoggedIn;
      state.user = user;
      state.token = token;
    },
  },
  actions: {
    async register({ commit }, credentials) {
      try {
        const response = await api.post('/autenticacion/registro/', credentials);
        const { token, username, email } = response.data;
        
        localStorage.setItem('user-token', token); // Guardamos el token en localStorage
        commit('SET_AUTH_DATA', { isLoggedIn: true, user: { username, email }, token });
        return response.data; // Devuelve los datos de registro incluyendo el token
      } catch (error) {
        console.error('Error en la acción de registro de Vuex:', error);
        throw error; // Relanza el error para que el componente que llama pueda manejarlo
      }
    },
    async login({ commit }, credentials) {
      try {
        const response = await api.post('/autenticacion/login/', credentials);
        const { token, username, email } = response.data;

        localStorage.setItem('user-token', token); // Guardamos el token en localStorage
        commit('SET_AUTH_DATA', { isLoggedIn: true, user: { username, email }, token });
        return response.data; // Devuelve los datos de login incluyendo el token
      } catch (error) {
        console.error('Error en la acción de login de Vuex:', error);
        throw error; // Relanza el error para que el componente que llama pueda manejarlo
      }
    },
    logout({ commit }) {
      localStorage.removeItem('user-token'); // Eliminamos el token de localStorage
      commit('SET_AUTH_DATA', { isLoggedIn: false, user: null, token: null });
    },
  },
  getters: {
    isAuthenticated: state => state.token !== null, // El usuario está autenticado si hay un token
    getToken: state => state.token,
    getUser: state => state.user,
  },
  modules: {
    // Aquí puedes modularizar tu store para aplicaciones más grandes
  },
});
