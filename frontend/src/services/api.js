import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar el token de autenticación
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export const authService = {
  login: async (credentials) => {
    try {
      const response = await api.post('/auth/login/', credentials);
      if (response.data.token) {
        localStorage.setItem('token', response.data.token);
      }
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  logout: () => {
    localStorage.removeItem('token');
  },

  isAuthenticated: () => {
    return !!localStorage.getItem('token');
  },

  register: async (userData) => {
    try {
      const response = await api.post('/auth/register/', userData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },
};

export const vehiculoService = {
  getVehiculos: async () => {
    try {
      const response = await api.get('/vehiculos/');
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  createVehiculo: async (vehiculoData) => {
    try {
      const response = await api.post('/vehiculos/', vehiculoData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  updateVehiculo: async (id, vehiculoData) => {
    try {
      const response = await api.put(`/vehiculos/${id}/`, vehiculoData);
      return response.data;
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },

  deleteVehiculo: async (id) => {
    try {
      await api.delete(`/vehiculos/${id}/`);
    } catch (error) {
      throw error.response?.data || error.message;
    }
  },
};

export default api; 