/**
 * @fileoverview My Products page component - displays products created by the current user
 * @module pages/MyProducts
 */
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api';
import { currentUser } from '../api/auth';
import { Product, User } from '../types';
import ListView from './ListView';

/**
 * MyProducts Component - Displays all products created by the current user
 * 
 * Features:
 * - Loads and displays products created by the authenticated user
 * - Shows product cards with edit/delete capabilities
 * - Loading states and error handling
 * - Empty state when no products exist
 * 
 * @returns JSX element containing the user's products list
 * 
 * @example
 * ```tsx
 * <Route path="/products/my" element={<MyProducts />} />
 * ```
 */
export default function MyProducts() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [user, setUser] = useState<User | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    /**
     * Fetch current user and their products
     */
    const fetchUserProducts = async (): Promise<void> => {
      try {
        // Get current user
        const currentUserData = await currentUser();
        setUser(currentUserData);

        // Fetch only the current user's products using the dedicated endpoint
        const response = await api.get('/v1/products/my');
        
        setProducts(response.data as Product[]);
      } catch (err: any) {
        console.error('Failed to fetch user products:', err);
        if (err.response?.status === 401) {
          // User not authenticated, redirect to home
          navigate('/');
        } else {
          setError('Failed to load your products. Please try again.');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchUserProducts();
  }, [navigate]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-600 dark:text-gray-400">Loading your products...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-red-500 dark:text-red-400">{error}</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 mt-[72px] pt-4">
      <div className="max-w-screen-2xl mx-auto px-4">
        <div className="mb-6">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            My Products
          </h1>
          {user?.username && (
            <p className="text-gray-600 dark:text-gray-400">
              Products created by @{user.username}
            </p>
          )}
        </div>

        {products.length === 0 ? (
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 text-center">
            <p className="text-gray-600 dark:text-gray-400 mb-4">
              You haven't created any products yet.
            </p>
            <button
              onClick={() => navigate('/products/new')}
              className="px-6 py-2 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg font-medium transition-colors"
            >
              Add Your First Product
            </button>
          </div>
        ) : (
          <ListView items={products} />
        )}
      </div>
    </div>
  );
}