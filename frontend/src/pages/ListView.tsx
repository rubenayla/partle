/**
 * @fileoverview ListView Component - Grid display for products and stores
 * @module pages/ListView
 */
import { Link } from 'react-router-dom';
import { ListViewItem } from '../types';
import { getProductImageSrc, hasProductImage } from '../utils/imageUtils';

/**
 * Props for the ListView component
 */
interface ListViewProps {
  /** Array of items to display (products or stores) */
  items: ListViewItem[];
}

/**
 * ListView Component - Responsive grid display for products and stores
 * 
 * Renders a responsive grid of items with images, names, and metadata.
 * Automatically detects item type (product vs store) based on properties
 * and renders appropriate links and information.
 * 
 * Features:
 * - Responsive grid layout (1-4 columns based on screen size)
 * - Automatic product/store detection and routing
 * - Image error handling with graceful fallback
 * - Hover effects and transitions
 * - Price display for products
 * - Address/homepage display for stores
 * 
 * @param props - Component props
 * @returns JSX element containing the grid layout
 * 
 * @example
 * ```tsx
 * function SearchResults() {
 *   const [products, setProducts] = useState<Product[]>([]);
 *   
 *   return (
 *     <div>
 *       <h2>Search Results</h2>
 *       <ListView items={products} />
 *     </div>
 *   );
 * }
 * ```
 */
export default function ListView({ items }: ListViewProps) {
  // Validate input
  if (!Array.isArray(items)) {
    return (
      <p className="text-red-600 dark:text-red-400">
        ListView: items must be an array
      </p>
    );
  }

  /**
   * Determine if an item is a product based on its properties
   * Products have either a price or creator_id property
   * 
   * @param item - Item to check
   * @returns true if item is a product, false if it's a store
   */
  const isProduct = (item: ListViewItem): boolean => {
    return item.price !== undefined || item.creator_id !== undefined;
  };

  return (
    <ul className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4 w-full">
      {items.map((item) => (
        <li key={item.id} className="h-full">
          <Link
            to={isProduct(item) ? `/products/${item.id}` : `/stores/${item.id}`}
            className="flex flex-col h-full border border-gray-200 dark:border-gray-700 rounded-xl p-4 bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 transition cursor-pointer"
            onClick={() => 
              console.log('ListView: Clicking card, ID:', item.id, 'URL:', isProduct(item) ? `/products/${item.id}` : `/stores/${item.id}`)
            }
          >
            {/* Item Image or Placeholder */}
            <div className="w-full h-32 mb-2">
              {(isProduct(item) ? hasProductImage(item) : item.image_url) ? (
                <img
                  src={isProduct(item) ? getProductImageSrc(item) || '' : item.image_url || ''}
                  alt={item.name}
                  className="w-full h-full object-cover rounded"
                  referrerPolicy="no-referrer"
                  crossOrigin="anonymous"
                  onError={(e) => {
                    // Replace with placeholder on error
                    e.currentTarget.style.display = 'none';
                    const parent = e.currentTarget.parentElement;
                    if (parent) {
                      parent.classList.add('bg-gray-200', 'dark:bg-gray-700', 'rounded', 'flex', 'items-center', 'justify-center');
                    }
                  }}
                  onLoad={() => {
                    // Image loaded successfully - no action needed
                  }}
                />
              ) : (
                <div className="w-full h-full bg-gray-200 dark:bg-gray-700 rounded flex items-center justify-center">
                  <svg className="w-8 h-8 text-gray-400 dark:text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </div>
              )}
            </div>
            
            {/* Content section with flex-grow to push metadata to bottom */}
            <div className="flex flex-col flex-grow">
              {/* Item Name */}
              <h3 className="font-semibold mb-1 text-gray-900 dark:text-white">
                {item.name}
              </h3>
              
              {/* Item Description (if available for products) */}
              {isProduct(item) && item.description && (
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-2 line-clamp-2">
                  {item.description}
                </p>
              )}
              
              {/* Spacer to push metadata to bottom */}
              <div className="flex-grow"></div>
              
              {/* Item Metadata */}
              {isProduct(item) ? (
                <p className="text-sm text-gray-600 dark:text-gray-300 mt-auto">
                  <span className="text-base font-semibold text-gray-900 dark:text-white">
                    {item.price ? `€${item.price}` : 'Price not set'}
                  </span>
                  {item.store && (
                    <span className="block text-xs mt-1">
                      {item.store.name}
                    </span>
                  )}
                </p>
              ) : (
                <p className="text-sm text-gray-600 dark:text-gray-300 mt-auto">
                  {item.description || 'No additional info'}
                </p>
              )}
            </div>
          </Link>
        </li>
      ))}
    </ul>
  );
}
