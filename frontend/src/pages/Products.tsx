/**
 * @fileoverview Products page component for managing store products
 * @module pages/Products
 */
import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../api/index';
import { Product } from '../types';

/**
 * Form data interface for new product creation
 */
interface ProductForm {
  name: string;
  spec: string;
  price: number;
  url: string;
  description: string;
}

/**
 * Products Page Component - Store-specific product management
 * 
 * Displays all products for a specific store and provides functionality
 * for store owners to add new products. Features a modal form for
 * product creation.
 * 
 * Features:
 * - Store-specific product listing
 * - Product creation modal with form
 * - Image display with error handling
 * - Responsive product grid layout
 * - Navigation back to stores list
 * - Real-time product list updates
 * 
 * @returns JSX element containing the products page
 * 
 * @example
 * ```tsx
 * // Used in routing for store-specific product pages
 * <Route path="/stores/:id/products" element={<Products />} />
 * ```
 */
export default function Products(): JSX.Element {
  const { id } = useParams<{ id: string }>(); // store id
  const [products, setProducts] = useState<Product[]>([]);
  const [open, setOpen] = useState<boolean>(false);
  const [form, setForm] = useState<ProductForm>({
    name: '',
    spec: '',
    price: 0,
    url: '',
    description: '',
  });

  useEffect(() => {
    if (id) {
      api.get(`/v1/products/store/${id}`).then((res) => {
        setProducts(res.data as Product[]);
      });
    }
  }, [id]);

  /**
   * Handle form input changes
   */
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>): void => {
    const { name, value } = e.target;
    setForm(prev => ({ 
      ...prev, 
      [name]: name === 'price' ? Number(value) : value 
    }));
  };

  /**
   * Handle form submission to create new product
   */
  const handleSave = async (e: React.FormEvent): Promise<void> => {
    e.preventDefault();
    if (!id) return;
    
    try {
      const { data } = await api.post('/v1/products/', { 
        ...form, 
        store_id: Number(id) 
      });
      setProducts(prev => [...prev, data as Product]);
      setOpen(false);
      setForm({ name: '', spec: '', price: 0, url: '', description: '' });
    } catch (error) {
      console.error('Error creating product:', error);
      alert('Failed to create product. Please try again.');
    }
  };

  return (
    <main className="w-full max-w-screen-2xl mx-auto px-4">
      <header className="flex justify-between mb-4">
        <h1 className="text-2xl font-semibold">Products</h1>
        <Link to="/stores" className="text-blue-600 hover:underline">
          ← Back
        </Link>
      </header>

      <button
        onClick={() => setOpen(true)}
        className="bg-transparent text-foreground hover:bg-background border border-gray-300 dark:border-gray-600 px-3 py-1 rounded mb-4"
      >
        + Add product
      </button>

      {products.length === 0 && <p>No products yet.</p>}
      
      <ul className="space-y-2">
        {products.map((product) => (
          <li key={product.id} className="border p-3 rounded">
            <div className="flex items-center gap-4">
              {product.image_url && (
                <img
                  src={product.image_url}
                  alt={product.name}
                  className="w-16 h-16 object-cover rounded"
                  onError={(e) => {
                    (e.target as HTMLImageElement).style.display = 'none';
                  }}
                />
              )}
              <div>
                <Link
                  to={`/products/${product.id}`}
                  className="text-blue-600 hover:underline"
                >
                  <strong>{product.name}</strong>
                </Link>
                {' — '}
                {product.description || '–'}
                {' — '}
                €{product.price ?? '?'}
              </div>
            </div>
          </li>
        ))}
      </ul>

      {/* Product Creation Modal */}
      {open && (
        <form
          onSubmit={handleSave}
          className="fixed inset-0 bg-black/40 flex items-center justify-center"
        >
          <div className="bg-white dark:bg-gray-800 p-6 rounded shadow space-y-3 w-96">
            <h2 className="text-lg font-medium">New product</h2>

            <input
              name="name"
              value={form.name}
              onChange={handleChange}
              placeholder="Name"
              className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:border-blue-500"
              required
            />
            <input
              name="spec"
              value={form.spec}
              onChange={handleChange}
              placeholder="Spec"
              className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:border-blue-500"
            />
            <input
              name="price"
              type="number"
              step="any"
              value={form.price}
              onChange={handleChange}
              placeholder="Price"
              className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:border-blue-500"
            />
            <input
              name="url"
              value={form.url}
              onChange={handleChange}
              placeholder="URL (optional)"
              className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:border-blue-500"
            />
            <textarea
              name="description"
              value={form.description}
              onChange={handleChange}
              placeholder="Description"
              className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:outline-none focus:border-blue-500 h-24 resize-none"
            />

            <div className="flex gap-2 justify-end">
              <button 
                type="button" 
                onClick={() => setOpen(false)}
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
