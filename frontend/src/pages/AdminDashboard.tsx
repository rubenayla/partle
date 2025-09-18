import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/index';

interface DashboardStats {
  counts: {
    users: number;
    products: number;
    stores: number;
    tags: number;
  };
  store_types: Array<{ type: string; count: number }>;
  top_creators: Array<{ email: string; username: string | null; product_count: number }>;
  top_tags: Array<{ name: string; count: number }>;
  recent_products: Array<{ name: string; price: number; store: string }>;
}

export default function AdminDashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    fetchDashboardStats();
  }, []);

  const fetchDashboardStats = async () => {
    try {
      const response = await api.get('/v1/admin/dashboard');
      setStats(response.data);
      setLoading(false);
    } catch (err: any) {
      if (err.response?.status === 403) {
        setError('Admin access required');
        setTimeout(() => navigate('/'), 2000);
      } else if (err.response?.status === 401) {
        setError('Please login');
        setTimeout(() => navigate('/'), 2000);
      } else {
        setError('Failed to load dashboard');
      }
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <div className="text-gray-600 dark:text-gray-400">Loading dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <div className="text-red-600">{error}</div>
      </div>
    );
  }

  if (!stats) return null;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Admin Dashboard</h1>

      {/* Main Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <StatCard title="Users" value={stats.counts.users} color="blue" />
        <StatCard title="Products" value={stats.counts.products} color="green" />
        <StatCard title="Stores" value={stats.counts.stores} color="purple" />
        <StatCard title="Tags" value={stats.counts.tags} color="orange" />
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        {/* Store Types */}
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow">
          <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Store Types</h2>
          <div className="space-y-3">
            {stats.store_types.map((type) => (
              <div key={type.type} className="flex justify-between items-center">
                <span className="text-gray-700 dark:text-gray-300 capitalize">{type.type}</span>
                <div className="flex items-center gap-2">
                  <div className="bg-gray-200 dark:bg-gray-700 rounded-full h-2 w-32">
                    <div
                      className="bg-blue-500 h-2 rounded-full"
                      style={{ width: `${(type.count / Math.max(...stats.store_types.map(t => t.count))) * 100}%` }}
                    />
                  </div>
                  <span className="text-sm font-medium text-gray-600 dark:text-gray-400 w-12 text-right">
                    {type.count}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Top Creators */}
        <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow">
          <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Top Contributors</h2>
          <div className="space-y-2">
            {stats.top_creators.map((creator, index) => (
              <div key={creator.email} className="flex items-center justify-between py-2 border-b dark:border-gray-700 last:border-0">
                <div className="flex items-center gap-3">
                  <span className="text-sm font-bold text-gray-500 w-6">#{index + 1}</span>
                  <div>
                    <div className="text-sm font-medium text-gray-900 dark:text-white">
                      {creator.username || creator.email.split('@')[0]}
                    </div>
                    <div className="text-xs text-gray-500 dark:text-gray-400">{creator.email}</div>
                  </div>
                </div>
                <span className="text-sm font-semibold text-blue-600 dark:text-blue-400">
                  {creator.product_count} products
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Popular Tags */}
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow">
        <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Popular Tags</h2>
        <div className="flex flex-wrap gap-2">
          {stats.top_tags.map((tag) => (
            <span
              key={tag.name}
              className="px-3 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-full text-sm"
            >
              {tag.name} <span className="text-gray-500 dark:text-gray-400">({tag.count})</span>
            </span>
          ))}
        </div>
      </div>

      {/* Recent Products */}
      <div className="bg-white dark:bg-gray-800 rounded-lg p-6 shadow">
        <h2 className="text-xl font-semibold mb-4 text-gray-900 dark:text-white">Recent Products</h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="text-left border-b dark:border-gray-700">
              <tr>
                <th className="pb-2 text-sm font-semibold text-gray-700 dark:text-gray-300">Product</th>
                <th className="pb-2 text-sm font-semibold text-gray-700 dark:text-gray-300">Store</th>
                <th className="pb-2 text-sm font-semibold text-gray-700 dark:text-gray-300 text-right">Price</th>
              </tr>
            </thead>
            <tbody>
              {stats.recent_products.map((product, index) => (
                <tr key={index} className="border-b dark:border-gray-700">
                  <td className="py-2 text-sm text-gray-900 dark:text-white">{product.name}</td>
                  <td className="py-2 text-sm text-gray-600 dark:text-gray-400">{product.store}</td>
                  <td className="py-2 text-sm text-gray-900 dark:text-white text-right">
                    ${product.price.toFixed(2)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

interface StatCardProps {
  title: string;
  value: number;
  color: 'blue' | 'green' | 'purple' | 'orange';
}

function StatCard({ title, value, color }: StatCardProps) {
  const colorClasses = {
    blue: 'bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200',
    green: 'bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200',
    purple: 'bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200',
    orange: 'bg-orange-100 dark:bg-orange-900 text-orange-800 dark:text-orange-200'
  };

  return (
    <div className={`rounded-lg p-6 ${colorClasses[color]}`}>
      <div className="text-sm font-medium opacity-80 mb-1">{title}</div>
      <div className="text-3xl font-bold">{value.toLocaleString()}</div>
    </div>
  );
}