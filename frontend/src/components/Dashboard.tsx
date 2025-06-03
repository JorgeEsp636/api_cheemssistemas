import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { vehiculoService, authService } from '../services/api';

interface Vehiculo {
  id: number;
  marca: string;
  modelo: string;
  anio: number;
  placa: string;
  estado: string;
}

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [vehiculos, setVehiculos] = useState<Vehiculo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!authService.getCurrentUser()) {
      navigate('/login');
      return;
    }
    fetchVehiculos();
  }, [navigate]);

  const fetchVehiculos = async () => {
    try {
      const data = await vehiculoService.getVehiculos();
      setVehiculos(data);
      setLoading(false);
    } catch (err: any) {
      setError(err.message || 'Error al cargar vehículos');
      setLoading(false);
    }
  };

  const handleLogout = () => {
    authService.logout();
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-xl">Cargando...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-semibold">Dashboard</h1>
            </div>
            <div className="flex items-center">
              <button
                onClick={handleLogout}
                className="ml-4 px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700"
              >
                Cerrar Sesión
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {error && (
          <div className="mb-4 rounded-md bg-red-50 p-4">
            <div className="text-sm text-red-700">{error}</div>
          </div>
        )}

        <div className="px-4 py-6 sm:px-0">
          <div className="border-4 border-dashed border-gray-200 rounded-lg p-4">
            <h2 className="text-lg font-medium mb-4">Vehículos</h2>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {vehiculos.map((vehiculo) => (
                <div
                  key={vehiculo.id}
                  className="bg-white overflow-hidden shadow rounded-lg"
                >
                  <div className="px-4 py-5 sm:p-6">
                    <h3 className="text-lg font-medium text-gray-900">
                      {vehiculo.marca} {vehiculo.modelo}
                    </h3>
                    <div className="mt-2 text-sm text-gray-500">
                      <p>Año: {vehiculo.anio}</p>
                      <p>Placa: {vehiculo.placa}</p>
                      <p>Estado: {vehiculo.estado}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Dashboard; 