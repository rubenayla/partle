import { useState, ChangeEvent, FormEvent, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import Layout from '../components/Layout';
import api from '../api';

interface FormState {
  name: string;
  address: string;
  lat: number;
  lon: number;
}

export default function AddStore() {
  const navigate = useNavigate();
  const [form, setForm] = useState<FormState>({ name: '', address: '', lat: 0, lon: 0 });
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    const handle = (e: KeyboardEvent) => {
      if (e.key.toLowerCase() === 'h') navigate('/');
    };
    window.addEventListener('keydown', handle);
    return () => window.removeEventListener('keydown', handle);
  }, [navigate]);


  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await api.post('/v1/stores/', { ...form, type: 'physical' });
      navigate('/stores');
    } catch {
      alert('Could not create store');
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
            <h1 className="text-2xl font-semibold">Add store</h1>
          </header>
          <form onSubmit={handleSubmit} className="space-y-3 max-w-md">
            <input
              name="name"
              value={form.name}
              onChange={handleChange}
              placeholder="Name"
              className="border p-2 w-full"
            />
            <input
              name="address"
              value={form.address}
              onChange={handleChange}
              placeholder="Address"
              className="border p-2 w-full"
            />
            <input
              name="lat"
              type="number"
              step="any"
              value={form.lat}
              onChange={handleChange}
              placeholder="Latitude"
              className="border p-2 w-full"
            />
            <input
              name="lon"
              type="number"
              step="any"
              value={form.lon}
              onChange={handleChange}
              placeholder="Longitude"
              className="border p-2 w-full"
            />
            <button disabled={saving} className="bg-blue-600 text-white px-3 py-1 rounded">
              {saving ? 'Saving...' : 'Save'}
            </button>
          </form>
        </div>
      </Layout>
  );
}
