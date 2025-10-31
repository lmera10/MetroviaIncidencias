import React from 'react';
import { Link } from 'react-router-dom';
import { Upload, Search, BarChart3, TrendingUp } from 'lucide-react';

const Home: React.FC = () => {
  const features = [
    {
      icon: Upload,
      title: 'Cargar Datos',
      description: 'Importa archivos Excel con incidencias operativas',
      link: '/upload',
      color: 'blue'
    },
    {
      icon: Search,
      title: 'Consultas Avanzadas',
      description: 'Busca y filtra incidencias por múltiples criterios',
      link: '/consultas',
      color: 'green'
    },
    {
      icon: BarChart3,
      title: 'Reportes',
      description: 'Genera reportes detallados y análisis estadísticos',
      link: '/reportes',
      color: 'purple'
    },
    {
      icon: TrendingUp,
      title: 'Tendencias',
      description: 'Visualiza tendencias y comportamientos históricos',
      link: '/reportes',
      color: 'orange'
    }
  ];

  return (
    <div className="space-y-8">
      {/* Hero Section */}
      <div className="bg-white rounded-lg shadow-sm border p-8 text-center">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Sistema de Incidencias Operativas
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Monitorea, analiza y reporta las incidencias operativas del Sistema Metrovía 
          en tiempo real con herramientas avanzadas de visualización.
        </p>
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {features.map((feature) => {
          const Icon = feature.icon;
          const colorClasses = {
            blue: 'bg-blue-50 text-blue-600',
            green: 'bg-green-50 text-green-600',
            purple: 'bg-purple-50 text-purple-600',
            orange: 'bg-orange-50 text-orange-600'
          };

          return (
            <Link
              key={feature.title}
              to={feature.link}
              className="bg-white rounded-lg shadow-sm border p-6 hover:shadow-md transition-shadow"
            >
              <div className={`w-12 h-12 rounded-lg ${colorClasses[feature.color as keyof typeof colorClasses]} flex items-center justify-center mb-4`}>
                <Icon className="h-6 w-6" />
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600 text-sm">
                {feature.description}
              </p>
            </Link>
          );
        })}
      </div>
    </div>
  );
};

export default Home;