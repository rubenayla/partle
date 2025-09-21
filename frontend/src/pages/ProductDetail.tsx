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
import { getProductIdentifierWithLabel } from '../utils/product';
import { trackProductView, trackExternalLink, trackStoreVisit } from '../utils/analytics';

/**
 * Form data interface for product editing
 */
interface EditForm {
  name: string;
  sku: string;
  description: string;
  price: string;
  currency: string;
  url: string;
  imageFile: File | null;
  imagePreview: string | null;
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
    sku: '',
    description: '',
    price: '',
    currency: '€',
    url: '',
    imageFile: null,
    imagePreview: null
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
          sku: productData.sku || '',
          description: productData.description || '',
          price: productData.price?.toString() || '',
          currency: productData.currency || '€',
          url: productData.url || '',
          imageFile: null,
          imagePreview: null
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
    
    setIsSaving(true);
    try {
      // First update the product details
      const updateData: Partial<Product> = {
        name: editForm.name.trim(),
        sku: editForm.sku?.trim() || undefined,
        description: editForm.description?.trim() || undefined,
        price: editForm.price ? parseFloat(editForm.price) : undefined,
        currency: editForm.currency?.trim() || '€',
        url: editForm.url?.trim() || undefined
      };
      
      const response = await api.patch(`/v1/products/${id}/`, updateData);
      let updatedProduct = response.data as Product;
      
      // Then upload the image if a new file was selected
      if (editForm.imageFile) {
        const formData = new FormData();
        formData.append('file', editForm.imageFile);
        
        const imageResponse = await api.post(`/v1/products/${id}/image`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        updatedProduct = imageResponse.data as Product;
      }
      
      setProduct(updatedProduct);
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
      sku: product.sku || '',
      description: product.description || '',
      price: product.price?.toString() || '',
      currency: product.currency || '€',
      url: product.url || '',
      imageFile: null,
      imagePreview: null
    });
    setIsEditing(false);
    setErrorMessage('');
    setSuccessMessage('');
    // Scroll to top when exiting edit mode
    setTimeout(() => window.scrollTo({ top: 0, left: 0, behavior: 'smooth' }), 100);
  };

  /**
   * Handle product deletion
   */
  const handleDelete = async (): Promise<void> => {
    if (!product || !id) return;

    const confirmDelete = window.confirm(
      `Are you sure you want to delete "${product.name}"? This action cannot be undone.`
    );

    if (!confirmDelete) return;

    try {
      await api.delete(`/v1/products/${id}`);
      setSuccessMessage('Product deleted successfully. Redirecting...');
      setTimeout(() => {
        navigate('/products');
      }, 2000);
    } catch (error) {
      console.error('Error deleting product:', error);
      setErrorMessage('Failed to delete product. Please try again.');
    }
  };

  /**
   * Handle input changes in edit form
   */
  const handleInputChange = (field: keyof EditForm, value: string): void => {
    setEditForm(prev => ({ ...prev, [field]: value }));
  };

  /**
   * Handle image file selection
   */
  const handleImageFileChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    const file = event.target.files?.[0];
    if (!file) {
      setEditForm(prev => ({ ...prev, imageFile: null, imagePreview: null }));
      return;
    }

    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
      setErrorMessage('Please select a valid image file (JPEG, PNG, GIF, or WebP)');
      return;
    }

    // Validate file size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
      setErrorMessage('Image file must be less than 10MB');
      return;
    }

    // Create preview URL
    const previewUrl = URL.createObjectURL(file);
    setEditForm(prev => ({ ...prev, imageFile: file, imagePreview: previewUrl }));
    setErrorMessage('');
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

  // Check if current user is the product owner or an admin
  const isOwner = user && product && (user.id === product.creator_id || user.role === 'admin');

  if (!product) return <p>Loading…</p>;
  if (authLoading) return <p>Loading…</p>;

  // Structured data for SEO
  const productSchema: ProductSchema = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    description: product.description || product.name,
    image: getProductImageSrc(product) || '',
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
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                Product Image
              </label>
              <input
                type="file"
                accept="image/jpeg,image/png,image/gif,image/webp"
                onChange={handleImageFileChange}
                className="w-full p-2 border border-gray-300 dark:border-gray-600 rounded focus:outline-none focus:border-blue-500 dark:bg-gray-800 dark:text-white"
              />
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
                Accepted formats: JPEG, PNG, GIF, WebP (max 10MB)
              </p>
              
              {/* Image preview */}
              {(editForm.imagePreview || (product && hasProductImage(product))) && (
                <div className="mt-4">
                  <p className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Preview:</p>
                  <img
                    src={editForm.imagePreview || getProductImageSrc(product) || ''}
                    alt="Product preview"
                    className="w-full max-w-md h-auto object-cover rounded border border-gray-300 dark:border-gray-600"
                  />
                  {editForm.imageFile && (
                    <button
                      type="button"
                      onClick={() => setEditForm(prev => ({ ...prev, imageFile: null, imagePreview: null }))}
                      className="mt-2 text-sm text-red-600 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300"
                    >
                      Remove new image
                    </button>
                  )}
                </div>
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
                  <>
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
                    <button
                      onClick={handleDelete}
                      className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 text-sm"
                    >
                      Delete
                    </button>
                  </>
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

          {/* Product Title and SKU */}
          {isEditing ? (
            <div className="mb-4 space-y-4">
              <div>
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
              <div>
                <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                  SKU (Stock Keeping Unit)
                </label>
                <input
                  type="text"
                  value={editForm.sku}
                  onChange={(e) => handleInputChange('sku', e.target.value)}
                  className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white dark:bg-gray-800"
                  placeholder="Optional - unique identifier for this store"
                />
                <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                  Leave blank to use product ID
                </p>
              </div>
            </div>
          ) : (
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">{product.name}</h1>
              <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">{getProductIdentifierWithLabel(product)}</p>
            </div>
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
            <>
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
            </>
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

          {/* Last Updated Date */}
          {product.updated_at && (
            <div className="mb-6">
              <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 uppercase tracking-wider mb-2">Last Updated</h3>
              <p className="text-gray-700 dark:text-gray-300">
                {new Date(product.updated_at).toLocaleDateString(undefined, {
                  year: 'numeric',
                  month: 'long',
                  day: 'numeric',
                  hour: '2-digit',
                  minute: '2-digit'
                })}
              </p>
            </div>
          )}

          {/* Store Information */}
          {store && (
            <div className="border-t border-gray-200 dark:border-gray-600 pt-6">
              <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 uppercase tracking-wider mb-3">Store Information</h3>
              <div className="space-y-4">
                {/* Store Name and Type */}
                <div>
                  <Link
                    to={`/stores/${store.id}/products`}
                    className="font-semibold text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                  >
                    {store.name}
                  </Link>
                  {store.type && (
                    <p className="text-sm text-gray-600 dark:text-gray-400 capitalize">{store.type} store</p>
                  )}
                </div>

                {/* Location Section */}
                {(store.address || (store.lat && store.lon)) && (
                  <div className="space-y-3 pt-4 border-t border-gray-200 dark:border-gray-600">
                    <h4 className="text-sm font-medium text-gray-600 dark:text-gray-400 uppercase tracking-wider">Location</h4>

                    {/* Physical Address */}
                    {store.address && (
                      <div className="text-sm text-gray-700 dark:text-gray-300">
                        <span className="font-medium">Address: </span>
                        <span>{store.address}</span>
                      </div>
                    )}

                    {/* Coordinates and Map Links */}
                    {store.lat && store.lon && (
                      <>
                        {/* Coordinates Display */}
                        <div className="text-sm text-gray-700 dark:text-gray-300">
                          <span className="font-medium">Coordinates: </span>
                          <span className="font-mono">{store.lat.toFixed(6)}, {store.lon.toFixed(6)}</span>
                        </div>

                        {/* Map Action Buttons */}
                        <div className="flex flex-wrap gap-3 pt-1">
                          {/* Google Maps Link */}
                          <a
                            href={`https://maps.google.com/?q=${store.lat},${store.lon}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 text-sm font-medium"
                            onClick={() => trackExternalLink(`https://maps.google.com/?q=${store.lat},${store.lon}`, 'store')}
                          >
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                            </svg>
                            Open in Google Maps
                          </a>

                          {/* Get Directions Link */}
                          <a
                            href={`https://www.google.com/maps/dir/?api=1&destination=${store.lat},${store.lon}`}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center gap-2 text-green-600 hover:text-green-700 dark:text-green-400 dark:hover:text-green-300 text-sm font-medium"
                            onClick={() => trackExternalLink(`https://www.google.com/maps/dir/?api=1&destination=${store.lat},${store.lon}`, 'directions')}
                          >
                            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 20l-5.447-2.724A1 1 0 013 16.382V5.618a1 1 0 011.447-.894L9 7m0 13l6-3m-6 3V7m6 10l4.553 2.276A1 1 0 0021 18.382V7.618a1 1 0 00-.553-.894L15 4m0 13V4m0 0L9 7" />
                            </svg>
                            Get Directions
                          </a>
                        </div>
                      </>
                    )}
                  </div>
                )}

                {/* Store Website Link - Separate */}
                {store.homepage && (
                  <a
                    href={store.homepage}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 text-sm font-medium"
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
          )}

          {/* Creator Information */}
          {product.creator && product.creator.username && (
            <div className="border-t border-gray-200 dark:border-gray-600 pt-6">
              <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400 uppercase tracking-wider mb-3">Added By</h3>
              <div className="flex items-center gap-2">
                <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                </svg>
                <Link
                  to={`/users/${product.creator.id}/products`}
                  className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                >
                  @{product.creator.username}
                </Link>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
