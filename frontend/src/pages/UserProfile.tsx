import { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { Store, Package, User, ArrowLeft } from 'lucide-react';
import api from '../api';
import ProductCard from '../components/ProductCard';
import StoreCard from '../components/StoreCard';

interface UserInfo {
  id: number;
  email: string;
  username: string | null;
}

interface Product {
  id: number;
  name: string;
  price: number | null;
  currency: string | null;
  description: string | null;
  image_url: string | null;
  store_id: number | null;
  store?: { id: number; name: string };
  creator?: { id: number; email: string; username?: string };
  created_at: string;
  updated_at: string;
}

interface StoreData {
  id: number;
  name: string;
  type: 'physical' | 'online' | 'chain';
  address: string | null;
  homepage: string | null;
  lat: number | null;
  lon: number | null;
  owner_id: number | null;
}

export default function UserProfile() {
  const { userId } = useParams<{ userId: string }>();
  const navigate = useNavigate();
  const [user, setUser] = useState<UserInfo | null>(null);
  const [stores, setStores] = useState<StoreData[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [activeTab, setActiveTab] = useState<'stores' | 'products'>('stores');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!userId) return;

    const fetchUserData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Fetch user info
        const userResponse = await api.get(`/v1/auth/user/${userId}`);
        setUser(userResponse.data);

        // Fetch user's stores
        const storesResponse = await api.get(`/v1/stores/user/${userId}`);
        setStores(storesResponse.data);

        // Fetch user's products
        const productsResponse = await api.get(`/v1/products/user/${userId}`);
        setProducts(productsResponse.data);
      } catch (err: any) {
        console.error('Error fetching user data:', err);
        if (err.response?.status === 404) {
          setError('User not found');
        } else {
          setError('Failed to load user profile');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchUserData();
  }, [userId]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-secondary">Loading user profile...</div>
      </div>
    );
  }

  if (error || !user) {
    return (
      <div className="text-center py-8">
        <p className="text-red-500 mb-4">{error || 'User not found'}</p>
        <Link to="/" className="text-accent hover:underline">
          Return to home
        </Link>
      </div>
    );
  }

  const displayName = user.username || user.email.split('@')[0];

  return (
    <>
      <header className="mb-6">
        <div className="flex items-center gap-2 mb-4">
          <button
            onClick={() => navigate(-1)}
            className="p-1 rounded hover:bg-surface-hover"
            title="Go back"
          >
            <ArrowLeft className="h-5 w-5" />
          </button>
          <h1 className="text-2xl font-semibold">User Profile</h1>
        </div>

        <div className="bg-surface rounded-lg p-6 shadow-md border border-gray-300 dark:border-gray-600">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 bg-accent/10 rounded-full flex items-center justify-center">
              <User className="h-8 w-8 text-accent" />
            </div>
            <div>
              <h2 className="text-xl font-semibold">{displayName}</h2>
              {user.username && (
                <p className="text-sm text-secondary">{user.email}</p>
              )}
            </div>
          </div>
        </div>
      </header>

      <div className="mb-6">
        <div className="flex gap-4 border-b border-gray-300 dark:border-gray-600">
          <button
            className={`pb-2 px-1 font-medium transition-colors ${
              activeTab === 'stores'
                ? 'text-accent border-b-2 border-accent'
                : 'text-secondary hover:text-foreground'
            }`}
            onClick={() => setActiveTab('stores')}
          >
            <div className="flex items-center gap-2">
              <Store className="h-4 w-4" />
              <span>Stores ({stores.length})</span>
            </div>
          </button>
          <button
            className={`pb-2 px-1 font-medium transition-colors ${
              activeTab === 'products'
                ? 'text-accent border-b-2 border-accent'
                : 'text-secondary hover:text-foreground'
            }`}
            onClick={() => setActiveTab('products')}
          >
            <div className="flex items-center gap-2">
              <Package className="h-4 w-4" />
              <span>Products ({products.length})</span>
            </div>
          </button>
        </div>
      </div>

      <div className="space-y-4">
        {activeTab === 'stores' ? (
          stores.length > 0 ? (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {stores.map((store) => (
                <StoreCard key={store.id} store={store} />
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-secondary">
              <Store className="h-12 w-12 mx-auto mb-3 opacity-50" />
              <p>No stores created yet</p>
            </div>
          )
        ) : (
          products.length > 0 ? (
            <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
              {products.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          ) : (
            <div className="text-center py-8 text-secondary">
              <Package className="h-12 w-12 mx-auto mb-3 opacity-50" />
              <p>No products added yet</p>
            </div>
          )
        )}
      </div>
    </>
  );
}