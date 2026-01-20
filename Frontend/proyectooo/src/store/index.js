import Vue from 'vue';
import Vuex from 'vuex';
import api from '@/utils/api'; // Importamos la instancia de axios configurada

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    isLoggedIn: false,
    token: null, // Para almacenar el token de autenticación
    user: null, // Para almacenar la información del usuario logeado
    cartItemCount: 0, // Nuevo estado para el conteo de ítems del carrito
    pendingVerificationEmail: localStorage.getItem('pending-verification-email') || null,
  },
  mutations: {
    SET_AUTH_DATA(state, { isLoggedIn, user, token }) {
      state.isLoggedIn = isLoggedIn;
      state.user = user;
      state.token = token;
    },
    SET_CART_ITEM_COUNT(state, count) {
      state.cartItemCount = count;
    },
    SET_PENDING_VERIFICATION_EMAIL(state, email) {
      state.pendingVerificationEmail = email;
    },
  },
  actions: {
    async register({ commit }, credentials) {
      try {
        // Registro en 2 pasos: inicia preregistro + envía OTP (no crea usuario real aquí)
        const payload = {
          email: credentials.email,
          first_name: credentials.username, // reutilizamos el "fullName" actual
          password: credentials.password,
          // Estos campos no existen aún en el formulario actual; quedan opcionales.
          celular: credentials.celular || '',
          ciudad: credentials.ciudad || '',
          // El backend diferencia Persona/Empresa por este campo
          tipo_cliente: credentials.tipo_cliente || 'Persona',
          // Solo aplica para Empresa (mayorista): URL del documento para validación
          ...(credentials.url_validacion ? { url_validacion: credentials.url_validacion } : {}),
        };
        const response = await api.post('/auth/init-register/', payload);

        const email = response.data?.email || payload.email;
        if (email) {
          localStorage.setItem('pending-verification-email', email);
          commit('SET_PENDING_VERIFICATION_EMAIL', email);
        }

        return response.data;
      } catch (error) {
        console.error('Error en la acción de registro de Vuex:', error);
        throw error; // Relanza el error para que el componente que llama pueda manejarlo
      }
    },
    async verifyOtp({ commit }, payload) {
      try {
        const response = await api.post('/auth/verify-otp/', payload);
        const { token, username, email } = response.data;

        // En el caso Empresa, el backend responde 200 OK pero SIN token (cuenta en revisión)
        if (token) {
          localStorage.setItem('user-token', token);
          // Persistimos info mínima del usuario para poder mostrar el nombre tras recargar.
          localStorage.setItem('user-data', JSON.stringify({ username, email }));
          commit('SET_AUTH_DATA', { isLoggedIn: true, user: { username, email }, token });
        } else {
          // Aseguramos estado "no logueado"
          localStorage.removeItem('user-token');
          localStorage.removeItem('user-data');
          commit('SET_AUTH_DATA', { isLoggedIn: false, user: null, token: null });
        }
        localStorage.removeItem('pending-verification-email');
        commit('SET_PENDING_VERIFICATION_EMAIL', null);

        return response.data;
      } catch (error) {
        console.error('Error en verifyOtp:', error);
        throw error;
      }
    },
    async resendOtp({ commit }, payload) {
      try {
        const response = await api.post('/auth/resend-otp/', payload);
        const email = response.data?.email || payload.email;
        if (email) {
          localStorage.setItem('pending-verification-email', email);
          commit('SET_PENDING_VERIFICATION_EMAIL', email);
        }
        return response.data;
      } catch (error) {
        console.error('Error en resendOtp:', error);
        throw error;
      }
    },
    async login({ commit }, credentials) {
      try {
        const response = await api.post('/autenticacion/login/', credentials);
        const { token, username, email } = response.data;

        localStorage.setItem('user-token', token); // Guardamos el token en localStorage
        // Guardamos también datos del usuario para persistir el nombre en UI tras recargar.
        localStorage.setItem('user-data', JSON.stringify({ username, email }));
        commit('SET_AUTH_DATA', { isLoggedIn: true, user: { username, email }, token });
        return response.data; // Devuelve los datos de login incluyendo el token
      } catch (error) {
        console.error('Error en la acción de login de Vuex:', error);
        throw error; // Relanza el error para que el componente que llama pueda manejarlo
      }
    },
    logout({ commit }) {
      localStorage.removeItem('user-token'); // Eliminamos el token de localStorage
      localStorage.removeItem('user-data');
      localStorage.removeItem('pending-verification-email');
      commit('SET_AUTH_DATA', { isLoggedIn: false, user: null, token: null });
      commit('SET_CART_ITEM_COUNT', 0); // También reseteamos el conteo del carrito al cerrar sesión
      commit('SET_PENDING_VERIFICATION_EMAIL', null);
    },
  },
  getters: {
    isAuthenticated: state => state.token !== null, // El usuario está autenticado si hay un token
    getToken: state => state.token,
    getUser: state => state.user,
    cartItemCount: state => state.cartItemCount, // Getter para el conteo de ítems del carrito
    pendingVerificationEmail: state => state.pendingVerificationEmail,
  },
  modules: {
    // Aquí puedes modularizar tu store para aplicaciones más grandes
  },
});
