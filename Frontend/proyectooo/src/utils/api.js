import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api'; // La URL base de tu backend Django

const api = axios.create({
  baseURL: API_BASE_URL,
});

api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('user-token');
    if (token) {
      config.headers.Authorization = `Token ${token}`;
    }
    // Si enviamos FormData (upload), NO forzamos Content-Type.
    // El navegador debe setear multipart/form-data con su boundary automáticamente.
    if (typeof FormData !== 'undefined' && config.data instanceof FormData) {
      try {
        // AxiosHeaders / objeto plano
        delete config.headers['Content-Type'];
        delete config.headers['content-type'];
      } catch (e) {
        // noop
      }
    }
    return config;
  },
  error => {
    return Promise.reject(error);
  }
);

export default api;
