/**
 * @fileoverview ProductDetail page component for viewing and editing product information
 * @module pages/ProductDetail
 */
import { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import api from '../api/index';
import { Helmet } from 'react-helmet-async';
import { useAuth } from '../hooks/useAuth';
import { Product, Store, User } from '../types';
import { getProductImageSrc, hasProductImage } from '../utils/imageUtils';

/**
 * Form data interface for product editing
 */
interface EditForm {
  name: string;
  description: string;
  price: string;
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

  useEffect(() => {
    console.log('ProductDetail: Loading product with ID:', id);
    if (!id) {
      console.error('ProductDetail: No product ID provided');
      return;
    }
    
    api.get(`/v1/products/${id}/`)
      .then((res) => {
        const productData: Product = res.data;
        console.log('ProductDetail: Successfully loaded product:', productData.name);
        setProduct(productData);
        setEditForm({
          name: productData.name || '',
          description: productData.description || '',
          price: productData.price?.toString() || '',
          url: productData.url || '',
          image_url: productData.image_url || ''
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
    
    setIsSaving(true);
    try {
      const updateData: Partial<Product> = {
        name: editForm.name,
        description: editForm.description || undefined,
        price: editForm.price ? parseFloat(editForm.price) : undefined,
        url: editForm.url || undefined,
        image_url: editForm.image_url || undefined
      };
      
      const response = await api.patch(`/v1/products/${id}/`, updateData);
      setProduct(response.data as Product);
      setIsEditing(false);
    } catch (error: any) {
      console.error('Failed to update product:', error);
      alert('Failed to update product. Please try again.');
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
  };

  /**
   * Handle input changes in edit form
   */
  const handleInputChange = (field: keyof EditForm, value: string): void => {
    setEditForm(prev => ({ ...prev, [field]: value }));
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
    <main className="w-full max-w-screen-2xl mx-auto px-4">
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
        className="mb-4 flex items-center gap-2 text-gray-600 hover:text-gray-900 dark:text-gray-400 dark:hover:text-gray-100 transition-colors"
        aria-label="Go back to previous page"
      >
        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        <span>Go Back</span>
      </button>

      <header className="flex justify-between items-start mb-4">
        {isEditing ? (
          <input
            type="text"
            value={editForm.name}
            onChange={(e) => handleInputChange('name', e.target.value)}
            className="text-2xl font-semibold bg-transparent border-b border-gray-300 focus:border-blue-500 focus:outline-none flex-1 mr-4"
            placeholder="Product name"
          />
        ) : (
          <h1 className="text-2xl font-semibold">{product.name}</h1>
        )}
        
        {isOwner && (
          <div className="flex gap-2">
            {isEditing ? (
              <>
                <button
                  onClick={handleSave}
                  disabled={isSaving || !editForm.name.trim()}
                  className="px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
                >
                  {isSaving ? 'Saving...' : 'Save'}
                </button>
                <button
                  onClick={handleCancel}
                  disabled={isSaving}
                  className="px-3 py-1 bg-gray-600 text-white rounded hover:bg-gray-700 disabled:opacity-50"
                >
                  Cancel
                </button>
              </>
            ) : (
              <button
                onClick={() => setIsEditing(true)}
                className="px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700"
              >
                Edit
              </button>
            )}
          </div>
        )}
      </header>

      {/* Image Section */}
      {isEditing ? (
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Image URL
          </label>
          <input
            type="url"
            value={editForm.image_url}
            onChange={(e) => handleInputChange('image_url', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:border-blue-500 focus:outline-none"
            placeholder="https://example.com/image.jpg"
          />
          {editForm.image_url && (
            <img
              src={editForm.image_url}
              alt="Preview"
              className="w-full max-w-sm h-auto object-cover rounded mt-2"
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
            className="w-full max-w-sm h-auto object-cover rounded mb-4"
          />
        )
      )}

      {/* Description Section */}
      {isEditing ? (
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Description
          </label>
          <textarea
            value={editForm.description}
            onChange={(e) => handleInputChange('description', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:border-blue-500 focus:outline-none"
            rows={3}
            placeholder="Product description"
          />
        </div>
      ) : (
        product.description && <p className="mb-3">{product.description}</p>
      )}

      {/* URL Section */}
      {isEditing ? (
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Product URL
          </label>
          <input
            type="url"
            value={editForm.url}
            onChange={(e) => handleInputChange('url', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:border-blue-500 focus:outline-none"
            placeholder="https://example.com/product"
          />
        </div>
      ) : (
        product.url && (
          <p className="mb-3">
            <a
              href={product.url}
              className="text-blue-600 underline"
              target="_blank"
              rel="noopener noreferrer"
            >
              {product.url}
            </a>
          </p>
        )
      )}

      {/* Price Section */}
      {isEditing ? (
        <div className="mb-4">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Price (€)
          </label>
          <input
            type="number"
            step="0.01"
            value={editForm.price}
            onChange={(e) => handleInputChange('price', e.target.value)}
            className="w-full p-2 border border-gray-300 rounded focus:border-blue-500 focus:outline-none"
            placeholder="0.00"
          />
        </div>
      ) : (
        product.price !== null && product.price !== undefined && (
          <p className="mb-3">Price: €{product.price}</p>
        )
      )}

      {/* Store Information */}
      {store && (
        <section className="mt-6 border-t pt-4">
          <h2 className="font-medium text-lg mb-2">Store Information</h2>
          <div className="space-y-2">
            <p className="font-medium">{store.name}</p>
            
            {/* Store Type */}
            {store.type && (
              <p className="text-sm text-gray-600">
                Type: <span className="capitalize">{store.type}</span>
              </p>
            )}
            
            {/* Physical Address */}
            {store.address && (
              <div>
                <p className="text-sm text-gray-600">Address:</p>
                <p className="text-sm">{store.address}</p>
              </div>
            )}
            
            {/* Map Link */}
            {store.latitude && store.longitude && (
              <div className="mt-2">
                <a
                  href={`https://maps.google.com/?q=${store.latitude},${store.longitude}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-2 text-blue-600 hover:text-blue-700 text-sm"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                  </svg>
                  View on Google Maps
                </a>
              </div>
            )}
            
            {/* Store Website */}
            {store.website && (
              <p className="text-sm">
                <a
                  href={store.website}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-600 hover:text-blue-700"
                >
                  Visit Store Website
                </a>
              </p>
            )}
          </div>
        </section>
      )}
    </main>
  );
}
