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
  async login(credentials: { email: string; password: string }) {
    try {
      const response = await api.post('/auth/token/', credentials);
      if (response.data.access) {
        localStorage.setItem('token', response.data.access);
      }
      return response.data;
    } catch (error: any) {
      throw error.response?.data?.detail || 'Error al iniciar sesión';
    }
  },

  async register(userData: { name: string; email: string; password: string }) {
    try {
      const response = await api.post('/auth/register/', userData);
      return response.data;
    } catch (error: any) {
      throw error.response?.data?.detail || 'Error al registrar usuario';
    }
  },

  logout() {
    localStorage.removeItem('token');
  },

  getCurrentUser() {
    const token = localStorage.getItem('token');
    return !!token;
  }
};

export const vehiculoService = {
  async getVehiculos() {
    try {
      const response = await api.get('/vehiculos/');
      return response.data;
    } catch (error: any) {
      throw error.response?.data || error.message;
    }
  },

  async getVehiculo(id: number) {
    try {
      const response = await api.get(`/vehiculos/${id}/`);
      return response.data;
    } catch (error: any) {
      throw error.response?.data || error.message;
    }
  },

  async createVehiculo(vehiculoData: any) {
    try {
      const response = await api.post('/vehiculos/', vehiculoData);
      return response.data;
    } catch (error: any) {
      throw error.response?.data || error.message;
    }
  },

  async updateVehiculo(id: number, vehiculoData: any) {
    try {
      const response = await api.put(`/vehiculos/${id}/`, vehiculoData);
      return response.data;
    } catch (error: any) {
      throw error.response?.data || error.message;
    }
  },

  async deleteVehiculo(id: number) {
    try {
      await api.delete(`/vehiculos/${id}/`);
    } catch (error: any) {
      throw error.response?.data || error.message;
    }
  },
};

export default api; 