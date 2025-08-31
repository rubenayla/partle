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
        <li 
          key={item.id} 
          className="border border-gray-200 dark:border-gray-700 rounded-xl p-4 bg-gray-50 dark:bg-gray-800 hover:bg-gray-100 dark:hover:bg-gray-700 transition"
        >
          {/* Item Image */}
          {(isProduct(item) ? hasProductImage(item) : item.image_url) && (
            <img
              src={isProduct(item) ? getProductImageSrc(item) || '' : item.image_url || ''}
              alt={item.name}
              className="w-full h-32 object-cover rounded mb-2"
              referrerPolicy="no-referrer"
              crossOrigin="anonymous"
              onError={(e) => {
                // Hide failed images (CORS/404 errors)
                e.currentTarget.style.display = 'none';
              }}
              onLoad={() => {
                // Image loaded successfully - no action needed
              }}
            />
          )}
          
          {/* Item Name with Link */}
          <h3 className="font-semibold mb-1">
            {isProduct(item) ? (
              <Link 
                to={`/products/${item.id}`} 
                className="text-gray-900 dark:text-white hover:underline"
                onClick={() => 
                  console.log('ListView: Clicking product link, ID:', item.id, 'URL:', `/products/${item.id}`)
                }
              >
                {item.name}
              </Link>
            ) : (
              <Link 
                to={`/stores/${item.id}`} 
                className="text-gray-900 dark:text-white hover:underline"
                onClick={() => 
                  console.log('ListView: Clicking store link, ID:', item.id, 'URL:', `/stores/${item.id}`)
                }
              >
                {item.name}
              </Link>
            )}
          </h3>
          
          {/* Item Metadata */}
          {isProduct(item) ? (
            <p className="text-sm text-gray-600 dark:text-gray-300">
              {item.price ? `€${item.price}` : 'Price not set'}
              {item.store && ` — ${item.store.name}`}
            </p>
          ) : (
            <p className="text-sm text-gray-600 dark:text-gray-300">
              {item.description || 'No additional info'}
            </p>
          )}
        </li>
      ))}
    </ul>
  );
}
