import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import VehiculoList from './components/VehiculoList';
import VehiculoForm from './components/VehiculoForm';
import Navbar from './components/Navbar';
import { authService } from './services/api';

const PrivateRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const isAuthenticated = authService.getCurrentUser();
  return isAuthenticated ? <>{children}</> : <Navigate to="/login" />;
};

const App: React.FC = () => {
  return (
    <Router>
      <div className="min-h-screen bg-gray-100">
        <Navbar />
        <main className="py-10">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route
              path="/vehiculos"
              element={
                <PrivateRoute>
                  <VehiculoList />
                </PrivateRoute>
              }
            />
            <Route
              path="/vehiculos/nuevo"
              element={
                <PrivateRoute>
                  <VehiculoForm />
                </PrivateRoute>
              }
            />
            <Route
              path="/vehiculos/:id/editar"
              element={
                <PrivateRoute>
                  <VehiculoForm />
                </PrivateRoute>
              }
            />
            <Route path="/" element={<Navigate to="/vehiculos" />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
};

export default App; 