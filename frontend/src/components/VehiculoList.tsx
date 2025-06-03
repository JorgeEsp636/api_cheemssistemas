import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { vehiculoService } from '../services/api';
import { Vehiculo } from '../types';

const VehiculoList: React.FC = () => {
  const navigate = useNavigate();
  const [vehiculos, setVehiculos] = useState<Vehiculo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadVehiculos();
  }, []);

  const loadVehiculos = async () => {
    try {
      const data = await vehiculoService.getVehiculos();
      setVehiculos(data);
      setLoading(false);
    } catch (err: any) {
      setError(err.message || 'Error al cargar vehículos');
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('¿Está seguro de que desea eliminar este vehículo?')) {
      try {
        await vehiculoService.deleteVehiculo(id);
        setVehiculos(vehiculos.filter((v) => v.id !== id));
      } catch (err: any) {
        setError(err.message || 'Error al eliminar el vehículo');
      }
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-md bg-red-50 p-4">
        <div className="text-sm text-red-700">{error}</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">Lista de Vehículos</h2>
        <button
          onClick={() => navigate('/vehiculos/nuevo')}
          className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
        >
          Nuevo Vehículo
        </button>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {vehiculos.map((vehiculo) => (
          <div
            key={vehiculo.id}
            className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow"
          >
            <h3 className="text-xl font-semibold mb-2">{vehiculo.marca}</h3>
            <p className="text-gray-600 mb-2">Modelo: {vehiculo.modelo}</p>
            <p className="text-gray-600 mb-2">Año: {vehiculo.anio}</p>
            <p className="text-gray-600 mb-2">Placa: {vehiculo.placa}</p>
            <p className="text-gray-600 mb-4">Estado: {vehiculo.estado}</p>
            <div className="flex justify-end space-x-2">
              <button
                onClick={() => navigate(`/vehiculos/${vehiculo.id}/editar`)}
                className="px-3 py-1 text-sm text-indigo-600 hover:text-indigo-800"
              >
                Editar
              </button>
              <button
                onClick={() => handleDelete(vehiculo.id)}
                className="px-3 py-1 text-sm text-red-600 hover:text-red-800"
              >
                Eliminar
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default VehiculoList; 