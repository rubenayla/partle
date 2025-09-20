/**
 * @fileoverview UserProducts Component - View all products uploaded by a specific user
 * @module pages/UserProducts
 */
import { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../api';
import ListView from './ListView';
import { useInfiniteScroll } from '../hooks/useInfiniteScroll';
import type { Product } from '../types';
import { Helmet } from 'react-helmet-async';

/**
 * UserProducts Component - Display all products uploaded by a specific user
 *
 * Shows a paginated list of products that a user has contributed to the platform.
 * Includes user information and total product count.
 *
 * @returns JSX element containing the user's products page
 */
export default function UserProducts(): JSX.Element {
  const { id } = useParams<{ id: string }>();
  const [products, setProducts] = useState<Product[]>([]);
  const [userInfo, setUserInfo] = useState<{ username?: string; email?: string } | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [hasMore, setHasMore] = useState<boolean>(true);
  const [offset, setOffset] = useState<number>(0);

  // Fetch user info and initial products
  useEffect(() => {
    if (!id) return;

    const fetchData = async () => {
      setLoading(true);
      try {
        // Get products by user
        const response = await api.get(`/v1/products/user/${id}`, {
          params: { limit: 20, offset: 0 }
        });

        const productsData = response.data as Product[];
        setProducts(productsData);
        setHasMore(productsData.length === 20);

        // Extract user info from the first product's creator
        if (productsData.length > 0 && productsData[0].creator) {
          setUserInfo({
            username: productsData[0].creator.username || undefined,
            email: undefined // We don't expose email in the API
          });
        }

        setOffset(20);
      } catch (error) {
        console.error('Error fetching user products:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  // Load more products when scrolling
  const loadMore = async () => {
    if (!id || !hasMore) return;

    try {
      const response = await api.get(`/v1/products/user/${id}`, {
        params: { limit: 20, offset }
      });

      const newProducts = response.data as Product[];
      setProducts(prev => [...prev, ...newProducts]);
      setHasMore(newProducts.length === 20);
      setOffset(prev => prev + 20);
    } catch (error) {
      console.error('Error loading more products:', error);
      setHasMore(false);
    }
  };

  useInfiniteScroll(loadMore, hasMore);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="text-gray-600 dark:text-gray-400">Loading user products...</div>
      </div>
    );
  }

  if (!products.length) {
    return (
      <div className="text-center py-12">
        <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          No products found
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          This user hasn't uploaded any products yet.
        </p>
        <Link
          to="/"
          className="inline-block mt-6 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          Browse All Products
        </Link>
      </div>
    );
  }

  const username = userInfo?.username || `User #${id}`;
  const pageTitle = `Products by ${username}`;

  return (
    <>
      <Helmet>
        <title>{pageTitle} - Partle</title>
        <meta name="description" content={`Browse products uploaded by ${username} on Partle`} />
      </Helmet>

      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          {pageTitle}
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Showing {products.length} product{products.length !== 1 ? 's' : ''} uploaded by this user
        </p>
      </div>

      <ListView items={products} />

      {hasMore && (
        <div className="flex justify-center mt-8">
          <div className="text-gray-600 dark:text-gray-400">Loading more...</div>
        </div>
      )}
    </>
  );
}