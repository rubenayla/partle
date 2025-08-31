/**
 * @fileoverview Stores page component for managing stores
 * @module pages/Stores
 */
import { useEffect, useState } from 'react';
import api from '../api/index';
import { Link } from 'react-router-dom';
import { Store } from '../types';

/**
 * Form data interface for new store creation
 */
interface StoreForm {
  name: string;
  address: string;
  lat: number;
  lon: number;
}

/**
 * Stores Page Component - Store management interface
 * 
 * Displays all stores and provides functionality for creating new stores.
 * Features a modal form for store creation with location coordinates.
 * 
 * Features:
 * - Store listing with addresses
 * - Store creation modal with form
 * - Navigation to store-specific products
 * - Responsive layout
 * - Real-time store list updates
 * - Coordinate input for store locations
 * 
 * @returns JSX element containing the stores page
 * 
 * @example
 * ```tsx
 * // Used in main routing
 * <Route path="/stores" element={<Stores />} />
 * ```
 */
export default function Stores(): JSX.Element {
  const [stores, setStores] = useState<Store[]>([]);
  const [openForm, setOpenForm] = useState<boolean>(false);
  const [form, setForm] = useState<StoreForm>({ 
    name: '', 
    address: '', 
    lat: 0, 
    lon: 0 
  });

  useEffect(() => {
    api.get('/v1/stores/').then(res => {
      setStores(res.data as Store[]);
    }).catch(error => {
      console.error('Error fetching stores:', error);
    });
  }, []);

  /**
   * Handle form input changes
   */
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>): void => {
    const { name, value } = e.target;
    setForm(prev => ({ 
      ...prev, 
      [name]: name === 'lat' || name === 'lon' ? Number(value) : value 
    }));
  };

  /**
   * Handle form submission to create new store
   */
  const createStore = async (e: React.FormEvent): Promise<void> => {
    e.preventDefault();
    try {
      const { data } = await api.post('/v1/stores/', form);
      setStores(prev => [...prev, data as Store]);
      setOpenForm(false);
      setForm({ name: '', address: '', lat: 0, lon: 0 });
    } catch (error) {
      console.error('Error creating store:', error);
      alert('Failed to create store. Please try again.');
    }
  };

  return (
    <main className="w-full max-w-screen-2xl mx-auto px-4">
      <header className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-semibold">Stores</h1>
        <button 
          onClick={() => setOpenForm(true)} 
          className="bg-transparent text-foreground hover:bg-background border border-gray-300 dark:border-gray-600 px-3 py-1 rounded"
        >
          + Add store
        </button>
      </header>

      {stores.length === 0 && <p>No stores yet.</p>}
      
      <ul className="space-y-2">
        {stores.map(store => (
          <li key={store.id} className="border p-3 rounded">
            <Link 
              to={`/stores/${store.id}/products`} 
              className="text-blue-600 hover:underline"
            >
              <strong>{store.name}</strong>
            </Link>
            <div className="text-sm text-gray-600 dark:text-gray-400">
              {store.address}
            </div>
          </li>
        ))}
      </ul>

      {/* Store Creation Modal */}
      {openForm && (
        <form
          onSubmit={createStore}
          className="fixed inset-0 bg-black/40 flex items-center justify-center"
        >
          <div className="bg-white dark:bg-gray-800 p-6 rounded shadow space-y-3 w-80">
            <h2 className="text-lg font-medium">New store</h2>

            <input 
              name="name" 
              placeholder="Name" 
              value={form.name} 
              onChange={handleChange} 
              className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:border-blue-500" 
              required
            />
            <input 
              name="address" 
              placeholder="Address" 
              value={form.address} 
              onChange={handleChange} 
              className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:border-blue-500" 
            />
            <input 
              name="lat" 
              type="number" 
              step="any" 
              placeholder="Latitude" 
              value={form.lat} 
              onChange={handleChange} 
              className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:border-blue-500" 
            />
            <input 
              name="lon" 
              type="number" 
              step="any" 
              placeholder="Longitude" 
              value={form.lon} 
              onChange={handleChange} 
              className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:border-blue-500" 
            />

            <div className="flex gap-2 justify-end">
              <button 
                type="button" 
                onClick={() => setOpenForm(false)} 
                className="px-3 py-1 text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200"
              >
                Cancel
              </button>
              <button 
                type="submit"
                className="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700"
                disabled={!form.name.trim()}
              >
                Save
              </button>
            </div>
          </div>
        </form>
      )}
    </main>
  );
}
