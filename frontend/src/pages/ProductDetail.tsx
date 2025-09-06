/**
 * @fileoverview ProductDetail page component for viewing and editing product information
 * @module pages/ProductDetail
 */
import { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import api from '../api/index';
import { Helmet } from 'react-helmet-async';
import { useAuth } from '../hooks/useAuth';
import type { Product, Store, User } from '../types';
import { getProductImageSrc, hasProductImage } from '../utils/imageUtils';
import { trackProductView, trackExternalLink, trackStoreVisit } from '../utils/analytics';

/**
 * Form data interface for product editing
 */
interface EditForm {
  name: string;
  description: string;
  price: string;
  currency: string;
  url: string;
  image_url: string;
}

/**
 * Structured data schema for SEO (Schema.org Product)
 */
interface ProductSchema {
  '@context': string;
  '@type': string;
  name: string;
  description: string;
  image: string;
  url: string;
  offers: {
    '@type': string;
    priceCurrency: string;
    price: number | null;
    itemCondition: string;
    availability: string;
    seller: {
      '@type': string;
      name: string;
    };
  };
}

/**
 * ProductDetail Component - Detailed product view and editing interface
 * 
 * Comprehensive product page with viewing, editing capabilities, and SEO optimization.
 * Supports owner-based editing permissions and structured data for search engines.
 * 
 * Features:
 * - Product information display with images and metadata
 * - Inline editing for product owners
 * - SEO optimization with structured data (Schema.org)
 * - Store information integration
 * - Responsive design with loading states
 * - Owner-based permission system
 * - Image error handling
 * - External link security
 * 
 * @returns JSX element containing the product detail page
 * 
 * @example
 * ```tsx
 * // Used in routing for individual product pages
 * <Route path="/products/:id" element={<ProductDetail />} />
 * ```
 */
export default function ProductDetail(): JSX.Element {
  console.log('ProductDetail: Component mounting');
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user, isLoading: authLoading } = useAuth();
  console.log('ProductDetail: useParams ID:', id, 'authLoading:', authLoading, 'user:', user?.email || 'not logged in');
  
  const [product, setProduct] = useState<Product | null>(null);
  const [store, setStore] = useState<Store | null>(null);
  const [isEditing, setIsEditing] = useState<boolean>(false);
  const [editForm, setEditForm] = useState<EditForm>({
    name: '',
    description: '',
    price: '',
    url: '',
    image_url: ''
  });
  const [isSaving, setIsSaving] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string>('');
  const [successMessage, setSuccessMessage] = useState<string>('');

  useEffect(() => {
    console.log('ProductDetail: Loading product with ID:', id);
    if (!id) {
      console.error('ProductDetail: No product ID provided');
      return;
    }
    
    // Scroll to top when component loads
    window.scrollTo({ top: 0, left: 0, behavior: 'instant' });
    
    api.get(`/v1/products/${id}/`)
      .then((res) => {
        const productData: Product = res.data;
        console.log('ProductDetail: Successfully loaded product:', productData.name);
        setProduct(productData);
        setEditForm({
          name: productData.name || '',
          description: productData.description || '',
          price: productData.price?.toString() || '',
          currency: productData.currency || '€',
          url: productData.url || '',
          image_url: productData.image_url || ''
        });

        // Track product view for analytics
        trackProductView({
          id: productData.id,
          name: productData.name,
          price: productData.price || undefined
        });
        
        if (productData.store_id) {
          api.get(`/v1/stores/${productData.store_id}/`).then((resp) => {
            setStore(resp.data as Store);
          });
        }
      })
      .catch((error: any) => {
        console.error('ProductDetail: Error fetching product:', error);
        if (error.response?.status === 404) {
          console.error('ProductDetail: Product not found, ID:', id);
        }
      });
  }, [id]);

  /**
   * Handle saving product edits
   */
  const handleSave = async (): Promise<void> => {
    if (!id) return;
    
    // Clear previous messages
    setErrorMessage('');
    setSuccessMessage('');
    
    // Basic validation
    if (!editForm.name.trim()) {
      setErrorMessage('Product name is required');
      return;
    }
    
    if (editForm.price && (isNaN(parseFloat(editForm.price)) || parseFloat(editForm.price) < 0)) {
      setErrorMessage('Please enter a valid price');
      return;
    }
    
    if (editForm.url && !isValidUrl(editForm.url)) {
      setErrorMessage('Please enter a valid URL');
      return;
    }
    
    if (editForm.image_url && !isValidUrl(editForm.image_url)) {
      setErrorMessage('Please enter a valid image URL');
      return;
    }
    
    setIsSaving(true);
    try {
      const updateData: Partial<Product> = {
        name: editForm.name.trim(),
        description: editForm.description?.trim() || undefined,
        price: editForm.price ? parseFloat(editForm.price) : undefined,
        currency: editForm.currency?.trim() || '€',
        url: editForm.url?.trim() || undefined,
        image_url: editForm.image_url?.trim() || undefined
      };
      
      const response = await api.patch(`/v1/products/${id}/`, updateData);
      setProduct(response.data as Product);
      setIsEditing(false);
      setSuccessMessage('Product updated successfully!');
      
      // Clear success message after 3 seconds
      setTimeout(() => setSuccessMessage(''), 3000);
    } catch (error: any) {
      console.error('Failed to update product:', error);
      if (error.response?.status === 403) {
        setErrorMessage('You can only edit products you created');
      } else if (error.response?.status === 404) {
        setErrorMessage('Product not found');
      } else if (error.response?.data?.detail) {
        setErrorMessage(error.response.data.detail);
      } else {
        setErrorMessage('Failed to update product. Please try again.');
      }
    } finally {
      setIsSaving(false);
    }
  };

  /**
   * Handle canceling edit mode
   */
  const handleCancel = (): void => {
    if (!product) return;
    
    setEditForm({
      name: product.name || '',
      description: product.description || '',
      price: product.price?.toString() || '',
      url: product.url || '',
      image_url: product.image_url || ''
    });
    setIsEditing(false);
    setErrorMessage('');
    setSuccessMessage('');
    // Scroll to top when exiting edit mode
    setTimeout(() => window.scrollTo({ top: 0, left: 0, behavior: 'smooth' }), 100);
  };

  /**
   * Handle input changes in edit form
   */
  const handleInputChange = (field: keyof EditForm, value: string): void => {
    setEditForm(prev => ({ ...prev, [field]: value }));
  };

  /**
   * Validate URL format
   */
  const isValidUrl = (url: string): boolean => {
    if (!url.trim()) return true; // Empty URLs are valid (optional field)
    try {
      new URL(url);
      return true;
    } catch {
      return false;
    }
  };

  // Check if current user is the product owner
  const isOwner = user && product && user.id === product.creator_id;

  if (!product) return <p>Loading…</p>;
  if (authLoading) return <p>Loading…</p>;

  // Structured data for SEO
  const productSchema: ProductSchema = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    description: product.description || product.name,
    image: getProductImageSrc(product) || product.image_url || '',
    url: `https://partle.rubenayla.xyz/products/${product.id}`,
    offers: {
      '@type': 'Offer',
      priceCurrency: 'EUR',
      price: product.price || null,
      itemCondition: 'https://schema.org/NewCondition',
      availability: 'https://schema.org/InStock',
      seller: {
        '@type': 'Organization',
        name: store ? store.name : 'Partle',
      },
    },
  };

  return (
    <div className="w-full">
      <Helmet>
        <title>{product.name} - Partle</title>
        <meta name="description" content={product.description || product.name} />
        <script type="application/ld+json">
          {JSON.stringify(productSchema)}
        </script>
      </Helmet>

      {/* Go Back Button */}
      <button
        onClick={() => navigate(-1)}
        className="mb-6 flex items-center gap-2 text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-100 transition-colors"
        aria-label="Go back to previous page"
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        <span>Go Back</span>
      </button>

      {/* Two-column layout */}
      <div className="grid grid-cols-1 lg:grid-cols-5 gap-8 items-start">
        {/* Image Section - Left Column */}
        <div className="w-full lg:col-span-2">
          {/* Product Image */}
          {isEditing ? (
            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-1">
                Image URL
              </label>
              <input
                type="url"
                value={editForm.image_url}
                onChange={(e) => handleInputChange('image_url', e.target.value)}
                className={`w-full p-2 border rounded focus:outline-none ${
                  editForm.image_url && !isValidUrl(editForm.image_url)
                    ? 'border-red-300 focus:border-red-500'
                    : 'border-gray-300 focus:border-blue-500'
                }`}
                placeholder="https://example.com/image.jpg (optional)"
              />
              {editForm.image_url && !isValidUrl(editForm.image_url) && (
                <p className="text-red-500 text-sm mt-1">Please enter a valid image URL</p>
              )}
              {editForm.image_url && isValidUrl(editForm.image_url) && (
                <img
                  src={editForm.image_url}
                  alt="Preview"
                  className="w-full max-w-md h-auto object-cover rounded mt-2"
                  onError={(e) => {
                    (e.target as HTMLImageElement).style.display = 'none';
                  }}
                />
              )}
            </div>
          ) : (
            hasProductImage(product) && (
              <img
                src={getProductImageSrc(product) || ''}
                alt={product.name}
                className="w-full h-auto object-cover rounded-lg shadow-lg"
              />
            )
          )}
        </div>

        {/* Info Card - Right Column */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg border border-gray-200 dark:border-gray-700 p-6 lg:col-span-3">
          {/* Edit Controls */}
          {isOwner && (
            <div className="mb-4">
              <div className="flex gap-2">
                {isEditing ? (
                  <>
                    <button
                      onClick={handleSave}
                      disabled={isSaving || !editForm.name.trim()}
                      className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 text-sm"
                    >
                      {isSaving ? 'Saving...' : 'Save'}
                    </button>
                    <button
                      onClick={handleCancel}
                      disabled={isSaving}
                      className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 disabled:opacity-50 text-sm"
                    >
                      Cancel
                    </button>
                  </>
                ) : (
                  <button
                    onClick={() => {
                      setIsEditing(true);
                      // Scroll to top when entering edit mode
                      setTimeout(() => window.scrollTo({ top: 0, left: 0, behavior: 'smooth' }), 100);
                    }}
                    className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 text-sm"
                  >
                    Edit
                  </button>
                )}
              </div>
              
              {/* Success Message */}
              {successMessage && (
                <div className="mt-2 p-2 bg-green-100 border border-green-400 text-green-700 rounded text-sm">
                  {successMessage}
                </div>
              )}
              
              {/* Error Message */}
              {errorMessage && (
                <div className="mt-2 p-2 bg-red-100 border border-red-400 text-red-700 rounded text-sm">
                  {errorMessage}
                </div>
              )}
            </div>
          )}

          {/* Product Title */}
          {isEditing ? (
            <div className="mb-4">
              <input
                type="text"
                value={editForm.name}
                onChange={(e) => handleInputChange('name', e.target.value)}
                className={`text-2xl font-bold bg-transparent border-b-2 focus:outline-none w-full pb-2 ${
                  !editForm.name.trim() ? 'border-red-300 focus:border-red-500' : 'border-gray-300 focus:border-blue-500'
                }`}
                placeholder="Product name (required)"
              />
              {!editForm.name.trim() && (
                <p className="text-red-500 text-sm mt-1">Product name is required</p>
              )}
            </div>
          ) : (
            <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">{product.name}</h1>
          )}


          {/* Description Section */}
          {isEditing ? (
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Description
              </label>
              <textarea
                value={editForm.description}
                onChange={(e) => handleInputChange('description', e.target.value)}
                className="w-full p-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:border-blue-500 focus:outline-none bg-white dark:bg-gray-700"
                rows={4}
                placeholder="Product description"
              />
            </div>
          ) : (
            product.description && (
              <div className="mb-6">
                <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 uppercase tracking-wider mb-2">Description</h3>
                <p className="text-gray-800 dark:text-gray-200 leading-relaxed">{product.description}</p>
              </div>
            )
          )}

          {/* Price Section */}
          {isEditing ? (
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Price
              </label>
              <input
                type="number"
                step="0.01"
                min="0"
                value={editForm.price}
                onChange={(e) => handleInputChange('price', e.target.value)}
                className={`w-full p-3 border rounded-lg focus:outline-none bg-white dark:bg-gray-700 ${
                  editForm.price && (isNaN(parseFloat(editForm.price)) || parseFloat(editForm.price) < 0)
                    ? 'border-red-300 focus:border-red-500 dark:border-red-600'
                    : 'border-gray-300 dark:border-gray-600 focus:border-blue-500'
                }`}
                placeholder="0.00 (optional)"
              />
              {editForm.price && (isNaN(parseFloat(editForm.price)) || parseFloat(editForm.price) < 0) && (
                <p className="text-red-500 text-sm mt-1">Please enter a valid price (0 or greater)</p>
              )}
            </div>
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Currency
              </label>
              <input
                type="text"
                value={editForm.currency}
                onChange={(e) => handleInputChange('currency', e.target.value)}
                className="w-full p-3 border rounded-lg focus:outline-none bg-white dark:bg-gray-700 border-gray-300 dark:border-gray-600 focus:border-blue-500"
                placeholder="€, $, BTC, gold oz..."
              />
            </div>
          ) : (
            product.price !== null && product.price !== undefined && (
              <div className="mb-6">
                <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 uppercase tracking-wider mb-2">Price</h3>
                <p className="text-3xl font-bold text-green-600 dark:text-green-400">{product.currency || '€'}{product.price}</p>
              </div>
            )
          )}

          {/* URL Section */}
          {isEditing ? (
            <div className="mb-6">
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Product URL
              </label>
              <input
                type="url"
                value={editForm.url}
                onChange={(e) => handleInputChange('url', e.target.value)}
                className={`w-full p-3 border rounded-lg focus:outline-none bg-white dark:bg-gray-700 ${
                  editForm.url && !isValidUrl(editForm.url)
                    ? 'border-red-300 focus:border-red-500 dark:border-red-600'
                    : 'border-gray-300 dark:border-gray-600 focus:border-blue-500'
                }`}
                placeholder="https://example.com/product (optional)"
              />
              {editForm.url && !isValidUrl(editForm.url) && (
                <p className="text-red-500 text-sm mt-1">Please enter a valid URL</p>
              )}
            </div>
          ) : (
            product.url && (
              <div className="mb-6">
                <a
                  href={product.url}
                  className="inline-flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg transition-colors font-medium"
                  target="_blank"
                  rel="noopener noreferrer"
                  onClick={() => trackExternalLink(product.url || '', 'product')}
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                  </svg>
                  Visit Product Page
                </a>
              </div>
            )
          )}

          {/* Tags Section */}
          {product.tags && product.tags.length > 0 && (
            <div className="mb-6">
              <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 uppercase tracking-wider mb-3">Tags</h3>
              <div className="flex flex-wrap gap-2">
                {product.tags.map((tag) => (
                  <span
                    key={tag.id}
                    className="px-3 py-1 bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 text-sm rounded-full"
                  >
                    {tag.name}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Store Information */}
          {store && (
            <div className="border-t border-gray-200 dark:border-gray-600 pt-6">
              <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 uppercase tracking-wider mb-3">Store Information</h3>
              <div className="space-y-3">
                <div>
                  <p className="font-semibold text-gray-900 dark:text-white">{store.name}</p>
                  {store.type && (
                    <p className="text-sm text-gray-600 dark:text-gray-400 capitalize">{store.type} store</p>
                  )}
                </div>
                
                {/* Physical Address */}
                {store.address && (
                  <div>
                    <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Address:</p>
                    <p className="text-sm text-gray-600 dark:text-gray-400">{store.address}</p>
                  </div>
                )}
                
                {/* Location Actions */}
                <div className="flex flex-col gap-2">
                  {store.latitude && store.longitude && (
                    <a
                      href={`https://maps.google.com/?q=${store.latitude},${store.longitude}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 text-sm"
                      onClick={() => trackExternalLink(`https://maps.google.com/?q=${store.latitude},${store.longitude}`, 'store')}
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                      </svg>
                      View on Google Maps
                    </a>
                  )}
                  
                  {store.homepage && (
                    <a
                      href={store.homepage}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 text-sm"
                      onClick={() => trackExternalLink(store.homepage || '', 'store')}
                    >
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9" />
                      </svg>
                      Visit Store Website
                    </a>
                  )}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
