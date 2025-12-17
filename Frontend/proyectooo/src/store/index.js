import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    isLoggedIn: false, // Por defecto, el usuario no está logeado
    // Puedes añadir más estado aquí, como la información del usuario logeado
    // user: null,
  },
  mutations: {
    SET_LOGIN_STATUS(state, status) {
      state.isLoggedIn = status;
    },
    // SET_USER(state, user) {
    //   state.user = user;
    // },
  },
  actions: {
    // Aquí puedes definir acciones asíncronas, como el login o logout
    // login({ commit }, credentials) {
    //   // Lógica para llamar a la API de login
    //   // commit('SET_LOGIN_STATUS', true);
    //   // commit('SET_USER', userData);
    // },
    // logout({ commit }) {
    //   // Lógica para limpiar la sesión
    //   // commit('SET_LOGIN_STATUS', false);
    //   // commit('SET_USER', null);
    // },
  },
  getters: {
    isAuthenticated: state => state.isLoggedIn,
    // getUser: state => state.user,
  },
  modules: {
    // Aquí puedes modularizar tu store para aplicaciones más grandes
  },
});

