import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const incidenciasAPI = {
  // Subir archivo Excel
  uploadFile: async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await api.post('/upload/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Obtener incidencias con filtros
  getIncidencias: async (filtros: any) => {
    const params = new URLSearchParams();
    Object.entries(filtros).forEach(([key, value]) => {
      if (value) params.append(key, value as string);
    });
    
    const response = await api.get(`/queries/incidencias?${params}`);
    return response.data;
  },

  // Reportes
  getReporteDiario: async (fecha: string) => {
    const response = await api.get(`/reports/diario?fecha=${fecha}`);
    return response.data;
  },

  getTendenciaSemanal: async (fechaFin?: string) => {
    const params = fechaFin ? `?fecha_fin=${fechaFin}` : '';
    const response = await api.get(`/reports/tendencia/semanal${params}`);
    return response.data;
  },

  getTendenciasMensuales: async (año: number) => {
    const response = await api.get(`/queries/tendencias/mensuales?año=${año}`);
    return response.data;
  },

  getTopIncidencias: async (limite: number = 10) => {
    const response = await api.get(`/reports/top-incidencias?limite=${limite}`);
    return response.data;
  },

  getComparativo: async (fecha1: string, fecha2: string) => {
    const response = await api.get(`/reports/comparativo?fecha1=${fecha1}&fecha2=${fecha2}`);
    return response.data;
  },
};

export default api;