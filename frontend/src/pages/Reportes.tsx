import React, { useState, useEffect } from 'react';
import { Calendar, TrendingUp, BarChart3, PieChart } from 'lucide-react';
import { incidenciasAPI } from '../services/api';
import { EstadisticasDiarias, TendenciaMensual } from '../types';
import CustomBarChart from '../components/charts/BarChart';
import CustomLineChart from '../components/charts/LineChart';
import LoadingSpinner from '../components/common/LoadingSpinner';

const Reportes: React.FC = () => {
  const [fecha, setFecha] = useState(new Date().toISOString().split('T')[0]);
  const [año, setAño] = useState(new Date().getFullYear());
  const [estadisticas, setEstadisticas] = useState<EstadisticasDiarias | null>(null);
  const [tendencias, setTendencias] = useState<TendenciaMensual | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const cargarEstadisticasDiarias = async (fecha: string) => {
    setIsLoading(true);
    try {
      const data = await incidenciasAPI.getReporteDiario(fecha);
      setEstadisticas(data);
    } catch (error) {
      console.error('Error al cargar estadísticas:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const cargarTendenciasMensuales = async (año: number) => {
    try {
      const data = await incidenciasAPI.getTendenciasMensuales(año);
      setTendencias(data);
    } catch (error) {
      console.error('Error al cargar tendencias:', error);
    }
  };

  useEffect(() => {
    cargarEstadisticasDiarias(fecha);
    cargarTendenciasMensuales(año);
  }, [fecha, año]);

  const meses = [
    'Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun',
    'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'
  ];

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">Reportes y Análisis</h1>
        
        {/* Controles */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              <Calendar className="inline h-4 w-4 mr-1" />
              Fecha del Reporte
            </label>
            <input
              type="date"
              value={fecha}
              onChange={(e) => setFecha(e.target.value)}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              <TrendingUp className="inline h-4 w-4 mr-1" />
              Año para Tendencias
            </label>
            <select
              value={año}
              onChange={(e) => setAño(Number(e.target.value))}
              className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              {[2023, 2024, 2025].map(year => (
                <option key={year} value={year}>{year}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {isLoading && <LoadingSpinner />}

      {/* Estadísticas Diarias */}
      {estadisticas && !isLoading && (
        <div className="space-y-6">
          {/* Resumen General */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="bg-white rounded-lg shadow-sm border p-6 text-center">
              <BarChart3 className="mx-auto h-8 w-8 text-blue-600 mb-2" />
              <div className="text-2xl font-bold text-gray-900">{estadisticas.total_incidencias}</div>
              <div className="text-sm text-gray-500">Total Incidencias</div>
            </div>
            
            <div className="bg-white rounded-lg shadow-sm border p-6 text-center">
              <PieChart className="mx-auto h-8 w-8 text-green-600 mb-2" />
              <div className="text-2xl font-bold text-gray-900">
                {estadisticas.por_turno.find(t => t.turno === 'Mañana')?.total || 0}
              </div>
              <div className="text-sm text-gray-500">Turno Mañana</div>
            </div>
            
            <div className="bg-white rounded-lg shadow-sm border p-6 text-center">
              <PieChart className="mx-auto h-8 w-8 text-yellow-600 mb-2" />
              <div className="text-2xl font-bold text-gray-900">
                {estadisticas.por_turno.find(t => t.turno === 'Tarde')?.total || 0}
              </div>
              <div className="text-sm text-gray-500">Turno Tarde</div>
            </div>
            
            <div className="bg-white rounded-lg shadow-sm border p-6 text-center">
              <PieChart className="mx-auto h-8 w-8 text-purple-600 mb-2" />
              <div className="text-2xl font-bold text-gray-900">
                {estadisticas.por_turno.find(t => t.turno === 'Noche')?.total || 0}
              </div>
              <div className="text-sm text-gray-500">Turno Noche</div>
            </div>
          </div>

          {/* Gráficos */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <CustomBarChart
              title="Incidencias por Troncal"
              data={estadisticas.por_troncal.map(item => ({
                name: `Troncal ${item.troncal}`,
                value: item.total
              }))}
              color="#3b82f6"
            />
            
            <CustomBarChart
              title="Incidencias por Turno"
              data={estadisticas.por_turno.map(item => ({
                name: item.turno,
                value: item.total
              }))}
              color="#10b981"
            />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <CustomBarChart
              title="Incidencias por Empresa"
              data={estadisticas.por_empresa.map(item => ({
                name: item.empresa,
                value: item.total
              }))}
              color="#8b5cf6"
            />
          </div>
        </div>
      )}

      {/* Tendencias Mensuales */}
      {tendencias && (
        <div className="bg-white rounded-lg shadow-sm border p-6">
          <h2 className="text-xl font-semibold text-gray-900 mb-6">
            Tendencias Mensuales - {tendencias.año}
          </h2>
          
          <CustomLineChart
            title="Evolución de Incidencias por Mes"
            data={tendencias.tendencias.map(t => ({
              name: meses[t.mes - 1],
              value: t.total
            }))}
            color="#f59e0b"
          />
        </div>
      )}

      {!estadisticas && !isLoading && (
        <div className="bg-white rounded-lg shadow-sm border p-8 text-center">
          <BarChart3 className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No hay datos</h3>
          <p className="text-gray-500">
            Selecciona una fecha para ver los reportes
          </p>
        </div>
      )}
    </div>
  );
};

export default Reportes;