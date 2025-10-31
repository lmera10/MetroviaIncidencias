import React, { useState } from 'react';
import { Upload as UploadIcon, FileText, CheckCircle, AlertCircle } from 'lucide-react';
import { incidenciasAPI } from '../services/api';
import LoadingSpinner from '../components/common/LoadingSpinner';

const Upload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<{ success: boolean; message: string } | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      if (selectedFile.type.includes('excel') || selectedFile.type.includes('spreadsheet') || 
          selectedFile.name.endsWith('.xlsx') || selectedFile.name.endsWith('.xls')) {
        setFile(selectedFile);
        setUploadResult(null);
      } else {
        alert('Por favor, selecciona un archivo Excel válido (.xlsx o .xls)');
      }
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setIsUploading(true);
    try {
      const result = await incidenciasAPI.uploadFile(file);
      setUploadResult({
        success: true,
        message: `✅ ${result.message} - ${result.incidencias_importadas} incidencias importadas`
      });
      setFile(null);
      // Reset file input
      const fileInput = document.getElementById('file-input') as HTMLInputElement;
      if (fileInput) fileInput.value = '';
    } catch (error: any) {
      setUploadResult({
        success: false,
        message: `❌ Error: ${error.response?.data?.detail || 'Error al subir el archivo'}`
      });
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="bg-white rounded-lg shadow-sm border p-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Cargar Incidencias</h1>
        <p className="text-gray-600 mb-6">
          Sube un archivo Excel con las incidencias operativas del Sistema Metrovía
        </p>

        {/* Upload Area */}
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center mb-6">
          <input
            id="file-input"
            type="file"
            accept=".xlsx,.xls"
            onChange={handleFileChange}
            className="hidden"
          />
          
          {!file ? (
            <label htmlFor="file-input" className="cursor-pointer">
              <UploadIcon className="mx-auto h-12 w-12 text-gray-400 mb-4" />
              <p className="text-gray-600 mb-2">
                <span className="font-semibold">Haz clic para seleccionar</span> o arrastra tu archivo
              </p>
              <p className="text-sm text-gray-500">Archivos Excel (.xlsx, .xls)</p>
            </label>
          ) : (
            <div className="flex items-center justify-center space-x-3">
              <FileText className="h-8 w-8 text-blue-600" />
              <div className="text-left">
                <p className="font-semibold text-gray-900">{file.name}</p>
                <p className="text-sm text-gray-500">
                  {(file.size / 1024 / 1024).toFixed(2)} MB
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Upload Button */}
        <button
          onClick={handleUpload}
          disabled={!file || isUploading}
          className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
        >
          {isUploading ? 'Subiendo...' : 'Subir Archivo'}
        </button>

        {/* Upload Result */}
        {uploadResult && (
          <div className={`mt-4 p-4 rounded-lg flex items-center space-x-3 ${
            uploadResult.success ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'
          }`}>
            {uploadResult.success ? (
              <CheckCircle className="h-5 w-5" />
            ) : (
              <AlertCircle className="h-5 w-5" />
            )}
            <span>{uploadResult.message}</span>
          </div>
        )}

        {/* Loading Spinner */}
        {isUploading && <LoadingSpinner />}
      </div>

      {/* Instructions */}
      <div className="bg-blue-50 rounded-lg p-6 mt-6">
        <h3 className="font-semibold text-blue-900 mb-2">Formato Requerido</h3>
        <ul className="text-blue-800 text-sm space-y-1">
          <li>• El archivo debe ser en formato Excel (.xlsx o .xls)</li>
          <li>• Debe contener las columnas: Fecha, Troncal, Ruta, Bus, Incidencia Primaria, etc.</li>
          <li>• La primera fila debe contener los encabezados de columna</li>
          <li>• Los datos deben seguir el formato estándar de exportación del sistema</li>
        </ul>
      </div>
    </div>
  );
};

export default Upload;