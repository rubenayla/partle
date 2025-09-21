import { useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Upload, FileText, Image, Download, AlertCircle, CheckCircle } from 'lucide-react';
import { getAuthToken } from '../utils/auth';

interface ImportResult {
  success: boolean;
  store_id: number;
  total_rows: number;
  products_created: number;
  products_failed: number;
  created_details: Array<{row: number, name: string, price: number}>;
  failed_details: Array<{row: number, name: string, error: string}>;
  images_processed: number;
}

export default function BulkImport() {
  const { storeId } = useParams<{ storeId: string }>();
  const navigate = useNavigate();
  const [productsFile, setProductsFile] = useState<File | null>(null);
  const [imagesZip, setImagesZip] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ImportResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const productsInputRef = useRef<HTMLInputElement>(null);
  const imagesInputRef = useRef<HTMLInputElement>(null);

  const handleProductsFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      const ext = file.name.toLowerCase();
      if (ext.endsWith('.csv') || ext.endsWith('.xlsx') || ext.endsWith('.xls')) {
        setProductsFile(file);
        setError(null);
      } else {
        setError('Please select a CSV or Excel file');
        setProductsFile(null);
      }
    }
  };

  const handleImagesFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      if (file.name.toLowerCase().endsWith('.zip')) {
        setImagesZip(file);
        setError(null);
      } else {
        setError('Please select a ZIP file for images');
        setImagesZip(null);
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!productsFile) {
      setError('Please select a products file');
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('products_file', productsFile);
    if (imagesZip) {
      formData.append('images_zip', imagesZip);
    }

    try {
      const token = getAuthToken();
      const response = await fetch(
        `${import.meta.env.VITE_API_BASE}/v1/stores/${storeId}/bulk-import`,
        {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
          body: formData,
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        if (errorData.detail?.errors) {
          setError(errorData.detail.errors.join('\n'));
        } else {
          setError(errorData.detail || 'Import failed');
        }
        return;
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const downloadTemplate = async (format: 'csv' | 'xlsx') => {
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_BASE}/v1/import-template?format=${format}`
      );
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `product_import_template.${format}`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError('Failed to download template');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="bg-white rounded-lg shadow-sm p-6">
          <h1 className="text-2xl font-bold text-gray-900 mb-6">Bulk Import Products</h1>

          {/* Instructions */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
            <h3 className="font-semibold text-blue-900 mb-2">How to Import Products</h3>
            <ol className="list-decimal list-inside space-y-1 text-sm text-blue-800">
              <li>Download a template file (CSV or Excel)</li>
              <li>Fill in your product details (name and price are required)</li>
              <li>Optionally, prepare a ZIP file with product images</li>
              <li>Upload both files and click Import</li>
            </ol>
            <div className="mt-4 flex gap-4">
              <button
                onClick={() => downloadTemplate('csv')}
                className="inline-flex items-center px-3 py-1 border border-blue-300 rounded-md text-sm font-medium text-blue-700 bg-white hover:bg-blue-50"
              >
                <Download className="h-4 w-4 mr-2" />
                Download CSV Template
              </button>
              <button
                onClick={() => downloadTemplate('xlsx')}
                className="inline-flex items-center px-3 py-1 border border-blue-300 rounded-md text-sm font-medium text-blue-700 bg-white hover:bg-blue-50"
              >
                <Download className="h-4 w-4 mr-2" />
                Download Excel Template
              </button>
            </div>
          </div>

          {/* Upload Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Products File Upload */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Products File (Required)
              </label>
              <div
                onClick={() => productsInputRef.current?.click()}
                className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center cursor-pointer hover:border-gray-400 transition-colors"
              >
                <input
                  ref={productsInputRef}
                  type="file"
                  accept=".csv,.xlsx,.xls"
                  onChange={handleProductsFileChange}
                  className="hidden"
                />
                {productsFile ? (
                  <div className="flex items-center justify-center text-green-600">
                    <FileText className="h-8 w-8 mr-2" />
                    <span className="font-medium">{productsFile.name}</span>
                  </div>
                ) : (
                  <div>
                    <FileText className="h-12 w-12 mx-auto text-gray-400 mb-2" />
                    <p className="text-sm text-gray-600">
                      Click to select CSV or Excel file
                    </p>
                  </div>
                )}
              </div>
            </div>

            {/* Images ZIP Upload */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Product Images (Optional)
              </label>
              <div
                onClick={() => imagesInputRef.current?.click()}
                className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center cursor-pointer hover:border-gray-400 transition-colors"
              >
                <input
                  ref={imagesInputRef}
                  type="file"
                  accept=".zip"
                  onChange={handleImagesFileChange}
                  className="hidden"
                />
                {imagesZip ? (
                  <div className="flex items-center justify-center text-green-600">
                    <Image className="h-8 w-8 mr-2" />
                    <span className="font-medium">{imagesZip.name}</span>
                  </div>
                ) : (
                  <div>
                    <Image className="h-12 w-12 mx-auto text-gray-400 mb-2" />
                    <p className="text-sm text-gray-600">
                      Click to select ZIP file with images
                    </p>
                  </div>
                )}
              </div>
            </div>

            {/* Error Display */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <div className="flex">
                  <AlertCircle className="h-5 w-5 text-red-400 mr-2 flex-shrink-0" />
                  <p className="text-sm text-red-800 whitespace-pre-line">{error}</p>
                </div>
              </div>
            )}

            {/* Submit Buttons */}
            <div className="flex gap-4">
              <button
                type="submit"
                disabled={loading || !productsFile}
                className={`flex-1 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white
                  ${loading || !productsFile
                    ? 'bg-gray-400 cursor-not-allowed'
                    : 'bg-blue-600 hover:bg-blue-700'}
                  focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500`}
              >
                {loading ? (
                  <span className="flex items-center justify-center">
                    <Upload className="animate-spin h-4 w-4 mr-2" />
                    Importing...
                  </span>
                ) : (
                  'Import Products'
                )}
              </button>
              <button
                type="button"
                onClick={() => navigate(`/stores/${storeId}`)}
                className="px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                Cancel
              </button>
            </div>
          </form>

          {/* Results Display */}
          {result && (
            <div className="mt-8 border-t pt-6">
              <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
                <div className="flex items-center">
                  <CheckCircle className="h-5 w-5 text-green-400 mr-2" />
                  <h3 className="font-semibold text-green-900">Import Completed!</h3>
                </div>
                <div className="mt-2 text-sm text-green-800">
                  <p>✅ {result.products_created} products imported successfully</p>
                  {result.images_processed > 0 && (
                    <p>🖼️ {result.images_processed} images processed</p>
                  )}
                  {result.products_failed > 0 && (
                    <p>⚠️ {result.products_failed} products failed to import</p>
                  )}
                </div>
              </div>

              {/* Failed Items */}
              {result.failed_details && result.failed_details.length > 0 && (
                <div className="mt-4">
                  <h4 className="font-medium text-gray-900 mb-2">Failed Imports:</h4>
                  <div className="bg-gray-50 rounded-lg p-3 max-h-48 overflow-auto">
                    {result.failed_details.map((item, idx) => (
                      <div key={idx} className="text-sm text-red-600 mb-1">
                        Row {item.row}: {item.name} - {item.error}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="mt-6 flex gap-4">
                <button
                  onClick={() => {
                    setResult(null);
                    setProductsFile(null);
                    setImagesZip(null);
                    if (productsInputRef.current) productsInputRef.current.value = '';
                    if (imagesInputRef.current) imagesInputRef.current.value = '';
                  }}
                  className="flex-1 py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                >
                  Import More Products
                </button>
                <button
                  onClick={() => navigate(`/stores/${storeId}`)}
                  className="flex-1 py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700"
                >
                  View Store
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}