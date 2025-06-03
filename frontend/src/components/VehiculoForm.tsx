import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { vehiculoService } from '../services/api';
import { Vehiculo } from '../types';

interface VehiculoFormData {
  marca: string;
  modelo: string;
  anio: number;
  placa: string;
  estado: string;
}

const VehiculoForm: React.FC = () => {
  const navigate = useNavigate();
  const { id } = useParams<{ id: string }>();
  const [formData, setFormData] = useState<VehiculoFormData>({
    marca: '',
    modelo: '',
    anio: new Date().getFullYear(),
    placa: '',
    estado: 'Disponible',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (id) {
      loadVehiculo();
    }
  }, [id]);

  const loadVehiculo = async () => {
    try {
      const data = await vehiculoService.getVehiculo(parseInt(id!));
      setFormData({
        marca: data.marca,
        modelo: data.modelo,
        anio: data.anio,
        placa: data.placa,
        estado: data.estado,
      });
    } catch (err: any) {
      setError(err.message || 'Error al cargar el vehículo');
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: name === 'anio' ? parseInt(value) : value,
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (id) {
        await vehiculoService.updateVehiculo(parseInt(id), formData);
      } else {
        await vehiculoService.createVehiculo(formData);
      }
      navigate('/vehiculos');
    } catch (err: any) {
      setError(err.message || 'Error al guardar el vehículo');
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h2 className="text-2xl font-bold mb-6">
        {id ? 'Editar Vehículo' : 'Nuevo Vehículo'}
      </h2>
      <form onSubmit={handleSubmit} className="max-w-lg">
        {error && (
          <div className="rounded-md bg-red-50 p-4 mb-4">
            <div className="text-sm text-red-700">{error}</div>
          </div>
        )}

        <div className="mb-4">
          <label
            htmlFor="marca"
            className="block text-sm font-medium text-gray-700"
          >
            Marca
          </label>
          <input
            type="text"
            id="marca"
            name="marca"
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            value={formData.marca}
            onChange={handleChange}
          />
        </div>

        <div className="mb-4">
          <label
            htmlFor="modelo"
            className="block text-sm font-medium text-gray-700"
          >
            Modelo
          </label>
          <input
            type="text"
            id="modelo"
            name="modelo"
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            value={formData.modelo}
            onChange={handleChange}
          />
        </div>

        <div className="mb-4">
          <label
            htmlFor="anio"
            className="block text-sm font-medium text-gray-700"
          >
            Año
          </label>
          <input
            type="number"
            id="anio"
            name="anio"
            required
            min="1900"
            max={new Date().getFullYear() + 1}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            value={formData.anio}
            onChange={handleChange}
          />
        </div>

        <div className="mb-4">
          <label
            htmlFor="placa"
            className="block text-sm font-medium text-gray-700"
          >
            Placa
          </label>
          <input
            type="text"
            id="placa"
            name="placa"
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            value={formData.placa}
            onChange={handleChange}
          />
        </div>

        <div className="mb-4">
          <label
            htmlFor="estado"
            className="block text-sm font-medium text-gray-700"
          >
            Estado
          </label>
          <select
            id="estado"
            name="estado"
            required
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
            value={formData.estado}
            onChange={handleChange}
          >
            <option value="Disponible">Disponible</option>
            <option value="En Mantenimiento">En Mantenimiento</option>
            <option value="En Uso">En Uso</option>
            <option value="Retirado">Retirado</option>
          </select>
        </div>

        <div className="flex justify-end space-x-4">
          <button
            type="button"
            onClick={() => navigate('/vehiculos')}
            className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Cancelar
          </button>
          <button
            type="submit"
            disabled={loading}
            className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            {loading ? 'Guardando...' : 'Guardar'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default VehiculoForm; 