import React, { useState, useEffect } from 'react';
import { Search, Filter, Download } from 'lucide-react';
import { incidenciasAPI } from '../services/api';
import { Incidencia, FiltrosConsulta } from '../types';
import LoadingSpinner from '../components/common/LoadingSpinner';

const Consultas: React.FC = () => {
  const [filtros, setFiltros] = useState<FiltrosConsulta>({});
  const [incidencias, setIncidencias] = useState<Incidencia[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [total, setTotal] = useState(0);
  const [tiposIncidencia, setTiposIncidencia] = useState<string[]>([]);

  // Cargar tipos de incidencia disponibles
  useEffect(() => {
    const cargarTiposIncidencia = async () => {
      try {
        const resultado = await incidenciasAPI.getTopIncidencias(20);
        const tipos = resultado.top_incidencias.map(item => item.tipo);
        setTiposIncidencia(tipos);
      } catch (error) {
        console.error('Error al cargar tipos de incidencia:', error);
      }
    };

    cargarTiposIncidencia();
  }, []);

  const handleFiltroChange = (key: keyof FiltrosConsulta, value: string) => {
    setFiltros(prev => ({ ...prev, [key]: value }));
  };

  const handleBuscar = async () => {
    setIsLoading(true);
    try {
      const resultado = await incidenciasAPI.getIncidencias(filtros);
      setIncidencias(resultado.incidencias);
      setTotal(resultado.total);
    } catch (error) {
      console.error('Error al buscar incidencias:', error);
      alert('Error al buscar incidencias');
    } finally {
      setIsLoading(false);
    }
  };

  const formatearFecha = (fechaString: string) => {
    if (!fechaString) return 'No definida';
    
    try {
      // Si ya está en formato legible, devolver tal cual
      if (fechaString.includes('-') && fechaString.includes(':')) {
        const fecha = new Date(fechaString);
        if (!isNaN(fecha.getTime())) {
          return fecha.toLocaleDateString('es-ES');
        }
      }
      return fechaString;
    } catch {
      return fechaString;
    }
  };

  const handleExportar = () => {
    // Función para exportar a CSV
    const headers = ['Fecha', 'Troncal', 'Ruta', 'Bus', 'Incidencia Primaria', 'Turno', 'Empresa'];
    const csvContent = [
      headers.join(','),
      ...incidencias.map(inc => [
        inc.Fecha ? formatearFecha(inc.Fecha) : '',
        inc.Troncal || '',
        inc.Ruta || '',
        inc.Bus || '',
        inc.Incidencia_primaria || '',
        inc.turno || '',
        inc.empresa || ''
      ].join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `incidencias-${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const limpiarFiltros = () => {
    setFiltros({});
    setIncidencias([]);
    setTotal(0);
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Consultar Incidencias</h1>
        
        {/* Filtros - AHORA CON 5 COLUMNAS */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Fecha Inicio
            </label>
            <input
              type="date"
              value={filtros.fecha_inicio || ''}
              onChange={(e) => handleFiltroChange('fecha_inicio', e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Fecha Fin
            </label>
            <input
              type="date"
              value={filtros.fecha_fin || ''}
              onChange={(e) => handleFiltroChange('fecha_fin', e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Troncal
            </label>
            <select
              value={filtros.troncal || ''}
              onChange={(e) => handleFiltroChange('troncal', e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Todos</option>
              <option value="1">Troncal 1</option>
              <option value="2">Troncal 2</option>
              <option value="3">Troncal 3</option>
              <option value="4">Troncal 4</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Empresa
            </label>
            <select
              value={filtros.empresa || ''}
              onChange={(e) => handleFiltroChange('empresa', e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Todas</option>
              <option value="STG">STG</option>
            </select>
          </div>

          {/* NUEVO FILTRO: TIPO DE INCIDENCIA */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Tipo de Incidencia
            </label>
            <select
              value={filtros.tipo_incidencia || ''}
              onChange={(e) => handleFiltroChange('tipo_incidencia', e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">Todos</option>
              {tiposIncidencia.map((tipo) => (
                <option key={tipo} value={tipo}>
                  {tipo.length > 30 ? `${tipo.substring(0, 30)}...` : tipo}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Botones de Acción */}
        <div className="flex space-x-4">
          <button
            onClick={handleBuscar}
            disabled={isLoading}
            className="flex items-center space-x-2 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 disabled:bg-gray-400 transition-colors"
          >
            <Search className="h-4 w-4" />
            <span>{isLoading ? 'Buscando...' : 'Buscar'}</span>
          </button>
          
          <button
            onClick={limpiarFiltros}
            className="flex items-center space-x-2 bg-gray-500 text-white px-6 py-2 rounded-lg hover:bg-gray-600 transition-colors"
          >
            <Filter className="h-4 w-4" />
            <span>Limpiar</span>
          </button>
          
          {incidencias.length > 0 && (
            <button
              onClick={handleExportar}
              className="flex items-center space-x-2 bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition-colors"
            >
              <Download className="h-4 w-4" />
              <span>Exportar CSV</span>
            </button>
          )}
        </div>

        {/* Mostrar filtros activos */}
        {Object.keys(filtros).length > 0 && (
          <div className="mt-4 p-3 bg-blue-50 rounded-lg">
            <h3 className="text-sm font-medium text-blue-800 mb-2">Filtros activos:</h3>
            <div className="flex flex-wrap gap-2">
              {filtros.fecha_inicio && (
                <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                  Desde: {filtros.fecha_inicio}
                </span>
              )}
              {filtros.fecha_fin && (
                <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                  Hasta: {filtros.fecha_fin}
                </span>
              )}
              {filtros.troncal && (
                <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                  Troncal: {filtros.troncal}
                </span>
              )}
              {filtros.empresa && (
                <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                  Empresa: {filtros.empresa}
                </span>
              )}
              {filtros.tipo_incidencia && (
                <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">
                  Incidencia: {filtros.tipo_incidencia}
                </span>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Resultados */}
      {isLoading && <LoadingSpinner />}
      
      {!isLoading && incidencias.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border">
          <div className="p-4 border-b">
            <h2 className="text-lg font-semibold text-gray-900">
              Resultados: {total} incidencias encontradas
            </h2>
          </div>
          
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Fecha
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Troncal
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Ruta
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Incidencia
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Turno
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {incidencias.slice(0, 50).map((incidencia, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {formatearFecha(incidencia.Fecha)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {incidencia.Troncal}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {incidencia.Ruta}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-900">
                      {incidencia.Incidencia_primaria}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                      {incidencia.turno}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          {total > 50 && (
            <div className="p-4 border-t text-sm text-gray-500">
              Mostrando 50 de {total} incidencias
            </div>
          )}
        </div>
      )}

      {!isLoading && incidencias.length === 0 && total === 0 && (
        <div className="bg-white rounded-lg shadow-sm border p-8 text-center">
          <Filter className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No hay resultados</h3>
          <p className="text-gray-500">
            Utiliza los filtros para buscar incidencias operativas
          </p>
        </div>
      )}
    </div>
  );
};

export default Consultas;