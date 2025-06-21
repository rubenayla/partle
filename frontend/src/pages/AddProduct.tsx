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
    store_id: '',
  });
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    api.get('/v1/stores/').then(res => setStores(res.data));
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
      await api.post('/v1/products', { ...form, store_id: form.store_id || null });
      navigate('/');
    } catch {
      alert('Could not create product');
    } finally {
      setSaving(false);
    }
  };

  return (
    <Layout>
      <div className="w-full max-w-screen-2xl mx-auto px-4">
        <header className="flex items-center gap-2 mb-4">
            <button
              type="button"
              onClick={() => navigate('/')}
              title="Back to home (H)"
              className="p-1 rounded hover:bg-background"
            >
              <ArrowLeft className="h-5 w-5" />
            </button>
            <h1 className="text-2xl font-semibold">Add product</h1>
          </header>

          <form onSubmit={save} className="space-y-3 max-w-md">
            <input
              name="name"
              value={form.name}
              onChange={change}
              placeholder="Name"
              className="input border p-2 w-full"
            />
            <input
              name="spec"
              value={form.spec}
              onChange={change}
              placeholder="Spec"
              className="input border p-2 w-full"
            />
            <input
              name="price"
              type="number"
              step="any"
              value={form.price}
              onChange={change}
              placeholder="Price"
              className="input border p-2 w-full"
            />
            <input
              name="url"
              value={form.url}
              onChange={change}
              placeholder="URL (optional)"
              className="input border p-2 w-full"
            />
            <textarea
              name="description"
              value={form.description}
              onChange={change}
              placeholder="Description"
              className="input h-24 border p-2 w-full"
            />
            <select name="store_id" value={form.store_id} onChange={change} className="border p-2 w-full">
              <option value="">Select store (optional)</option>
              {stores.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name}
                </option>
              ))}
            </select>
            <button disabled={saving} className="bg-blue-600 text-white px-3 py-1 rounded">
              {saving ? 'Saving...' : 'Save'}
            </button>
          </form>
        </div>
      </Layout>
  );
}
