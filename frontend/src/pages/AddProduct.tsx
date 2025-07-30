import { useEffect, useState, ChangeEvent, FormEvent } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import Layout from '../components/Layout';
import api from '../api';

interface Store { id: number; name: string; }
interface FormState {
  name: string;
  spec: string;
  price: number;
  url: string;
  description: string;
  image_url: string;
  store_id: string;
}

export default function AddProduct() {
  const navigate = useNavigate();
  const [stores, setStores] = useState<Store[]>([]);
  const [form, setForm] = useState<FormState>({
    name: '',
    spec: '',
    price: 0,
    url: '',
    description: '',
    image_url: '',
    store_id: '',
  });
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    api.get('/api/v1/stores/').then(res => setStores(res.data));
  }, []);

  useEffect(() => {
    const handle = (e: KeyboardEvent) => {
      if (e.key.toLowerCase() === 'h') navigate('/');
    };
    window.addEventListener('keydown', handle);
    return () => window.removeEventListener('keydown', handle);
  }, [navigate]);

  const change = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const save = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await api.post('/api/v1/products', { ...form, store_id: form.store_id || null });
      navigate('/');
    } catch {
      alert('Could not create product');
    } finally {
      setSaving(false);
    }
  };

  return (
    <Layout>
      <header className="flex items-center gap-2 mb-6">
        <button
          type="button"
          onClick={() => navigate('/')}
          title="Back to home (H)"
          className="p-1 rounded hover:bg-surface-hover"
        >
          <ArrowLeft className="h-5 w-5" />
        </button>
        <h1 className="text-2xl font-semibold">Add product</h1>
      </header>
      
      <div className="max-w-4xl mx-auto">
        <div className="bg-surface rounded-xl shadow-lg border border-gray-300 dark:border-gray-600 p-8">
            <form onSubmit={save} className="space-y-6">
              {/* Primary Information Section */}
              <div className="space-y-4">
                <h2 className="text-lg font-medium text-foreground border-b border-gray-300 dark:border-gray-600 pb-2">
                  Product Information
                </h2>
                
                <div className="space-y-4">
                  <div>
                    <label htmlFor="name" className="block text-sm font-medium text-secondary mb-1">
                      Product Name *
                    </label>
                    <input
                      id="name"
                      name="name"
                      value={form.name}
                      onChange={change}
                      placeholder="Enter product name"
                      className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-background focus:ring-2 focus:ring-accent focus:border-transparent transition-colors"
                      required
                    />
                  </div>

                  <div>
                    <label htmlFor="description" className="block text-sm font-medium text-secondary mb-1">
                      Description
                    </label>
                    <textarea
                      id="description"
                      name="description"
                      value={form.description}
                      onChange={change}
                      placeholder="Describe the product..."
                      rows={4}
                      className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-background focus:ring-2 focus:ring-accent focus:border-transparent transition-colors resize-none"
                    />
                  </div>

                  <div>
                    <label htmlFor="url" className="block text-sm font-medium text-secondary mb-1">
                      Product URL
                    </label>
                    <input
                      id="url"
                      name="url"
                      type="url"
                      value={form.url}
                      onChange={change}
                      placeholder="https://example.com/product"
                      className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-background focus:ring-2 focus:ring-accent focus:border-transparent transition-colors"
                    />
                  </div>
                </div>
              </div>

              {/* Media Section */}
              <div className="space-y-4">
                <h2 className="text-lg font-medium text-foreground border-b border-gray-300 dark:border-gray-600 pb-2">
                  Media
                </h2>
                
                <div>
                  <label htmlFor="image_url" className="block text-sm font-medium text-secondary mb-1">
                    Image URL
                  </label>
                  <input
                    id="image_url"
                    name="image_url"
                    type="url"
                    value={form.image_url}
                    onChange={change}
                    placeholder="https://example.com/image.jpg"
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-background focus:ring-2 focus:ring-accent focus:border-transparent transition-colors"
                  />
                  {form.image_url && (
                    <div className="mt-3">
                      <img 
                        src={form.image_url} 
                        alt="Product preview" 
                        className="w-32 h-32 object-cover rounded-lg border border-gray-200 dark:border-gray-700"
                        onError={(e) => {
                          e.currentTarget.style.display = 'none';
                        }}
                      />
                    </div>
                  )}
                </div>
              </div>

              {/* Store Selection */}
              <div className="space-y-4">
                <h2 className="text-lg font-medium text-foreground border-b border-gray-300 dark:border-gray-600 pb-2">
                  Store Information
                </h2>
                
                <div>
                  <label htmlFor="store_id" className="block text-sm font-medium text-secondary mb-1">
                    Store
                  </label>
                  <select
                    id="store_id"
                    name="store_id"
                    value={form.store_id}
                    onChange={change}
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-background focus:ring-2 focus:ring-accent focus:border-transparent transition-colors"
                  >
                    <option value="">Select a store (optional)</option>
                    {stores.map((s) => (
                      <option key={s.id} value={s.id}>
                        {s.name}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Additional Details Section */}
              <div className="space-y-4">
                <h2 className="text-lg font-medium text-foreground border-b border-gray-300 dark:border-gray-600 pb-2">
                  Additional Details
                </h2>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="spec" className="block text-sm font-medium text-secondary mb-1">
                      Specifications
                    </label>
                    <input
                      id="spec"
                      name="spec"
                      value={form.spec}
                      onChange={change}
                      placeholder="Product specifications"
                      className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-background focus:ring-2 focus:ring-accent focus:border-transparent transition-colors"
                    />
                  </div>

                  <div>
                    <label htmlFor="price" className="block text-sm font-medium text-secondary mb-1">
                      Price
                    </label>
                    <div className="relative">
                      <span className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-500 dark:text-gray-400">$</span>
                      <input
                        id="price"
                        name="price"
                        type="number"
                        step="0.01"
                        min="0"
                        value={form.price}
                        onChange={change}
                        placeholder="0.00"
                        className="w-full pl-8 pr-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-background focus:ring-2 focus:ring-accent focus:border-transparent transition-colors"
                      />
                    </div>
                  </div>
                </div>
              </div>

              {/* Submit Button */}
              <div className="pt-6 border-t border-gray-300 dark:border-gray-600">
                <div className="flex gap-3 justify-end">
                  <button
                    type="button"
                    onClick={() => navigate('/')}
                    className="px-6 py-3 border border-gray-300 dark:border-gray-600 text-secondary rounded-lg hover:bg-surface-hover transition-colors"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={saving || !form.name.trim()}
                    className="px-6 py-3 bg-accent text-white rounded-lg hover:bg-accent-hover disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-medium"
                  >
                    {saving ? 'Saving…' : 'Add Product'}
                  </button>
                </div>
              </div>
            </form>
        </div>
      </div>
    </Layout>
  );
}