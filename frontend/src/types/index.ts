export interface Incidencia {
  id: number;
  fecha: string;
  troncal: string;
  codigo_ruta: string;
  ruta: string;
  bus: string;
  hora_programada: string;
  hora_real: string;
  incidencia_primaria: string;
  incidencia_secundaria: string;
  conductor: string;
  operador: string;
  observaciones: string;
  tipo_dia: string;
  turno: string;
  empresa: string;
}

export interface FiltrosConsulta {
  fecha_inicio?: string;
  fecha_fin?: string;
  troncal?: string;
  empresa?: string;
  tipo_incidencia?: string;
  turno?: string;
}

export interface EstadisticasDiarias {
  fecha: string;
  total_incidencias: number;
  por_turno: Array<{ turno: string; total: number }>;
  por_troncal: Array<{ troncal: string; total: number }>;
  por_empresa: Array<{ empresa: string; total: number }>;
}

export interface TendenciaMensual {
  año: number;
  tendencias: Array<{ mes: number; total: number }>;
}
export interface Usuario {
  id: number;
  email: string;
  nombre: string;
  apellido: string;
  empresa: string;
  rol: string;
  activo: boolean;
  fecha_creacion: string;
  ultimo_acceso?: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegistroRequest {
  email: string;
  password: string;
  nombre: string;
  apellido: string;
  empresa: string;
  rol?: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  usuario: Usuario;
}

export interface AuthContextType {
  usuario: Usuario | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  registro: (datos: RegistroRequest) => Promise<void>;
  logout: () => void;
  loading: boolean;
}
// Tipos para respuestas de API
export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}