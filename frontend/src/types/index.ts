export interface User {
  id: number;
  username: string;
  email: string;
}

export interface Vehiculo {
  id: number;
  marca: string;
  modelo: string;
  anio: number;
  placa: string;
  estado: string;
  created_at: string;
  updated_at: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData {
  name: string;
  email: string;
  password: string;
}

export interface AuthResponse {
  access: string;
  refresh: string;
} 