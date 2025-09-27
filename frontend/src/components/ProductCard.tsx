import { Link } from 'react-router-dom';
import { Package, Store, User, Building2 } from 'lucide-react';
import { getProductImageSrc } from '../utils/helpers';
import { getStoreLogoSrc } from '../utils/imageUtils';

interface Product {
  id: number;
  name: string;
  price: number | null;
  currency: string | null;
  description: string | null;
  image_url: string | null;
  store_id: number | null;
  store?: {
    id: number;
    name: string;
    logo_filename?: string | null;
    logo_content_type?: string | null;
  };
  creator?: { id: number; email: string; username?: string };
  created_at: string;
  updated_at: string;
}

interface ProductCardProps {
  product: Product;
}

export default function ProductCard({ product }: ProductCardProps) {
  const imageSrc = getProductImageSrc(product.id, product.image_url);
  const displayCreator = product.creator?.username || product.creator?.email?.split('@')[0];
  const storeLogoSrc = product.store ? getStoreLogoSrc(product.store as any) : null;

  return (
    <div className="bg-surface rounded-lg shadow-md border border-gray-300 dark:border-gray-600 overflow-hidden hover:shadow-lg transition-shadow">
      <Link to={`/products/${product.id}`}>
        {imageSrc ? (
          <img
            src={imageSrc}
            alt={product.name}
            className="w-full h-48 object-cover"
            referrerPolicy="no-referrer"
            crossOrigin="anonymous"
            onError={(e) => {
              const target = e.target as HTMLImageElement;
              target.style.display = 'none';
              const parent = target.parentElement;
              if (parent) {
                const placeholder = document.createElement('div');
                placeholder.className = 'w-full h-48 bg-gray-100 dark:bg-gray-800 flex items-center justify-center';
                placeholder.innerHTML = '<svg class="h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"></path></svg>';
                parent.appendChild(placeholder);
              }
            }}
          />
        ) : (
          <div className="w-full h-48 bg-gray-100 dark:bg-gray-800 flex items-center justify-center">
            <Package className="h-12 w-12 text-gray-400" />
          </div>
        )}
      </Link>

      <div className="p-4">
        <Link to={`/products/${product.id}`} className="block mb-2">
          <h3 className="font-semibold text-foreground line-clamp-2">
            {product.name}
          </h3>
        </Link>

        {product.price !== null && (
          <p className="text-lg font-bold text-foreground mb-2">
            {product.price} {product.currency || '€'}
          </p>
        )}

        {product.description && (
          <p className="text-sm text-secondary line-clamp-2 mb-3">
            {product.description}
          </p>
        )}

        <div className="space-y-2">
          <div className="flex items-center justify-between text-xs text-secondary">
            {product.store ? (
              <Link
                to={`/stores/${product.store.id}/products`}
                className="flex items-center gap-1 text-secondary hover:text-foreground transition-colors"
              >
                {storeLogoSrc ? (
                  <img
                    src={storeLogoSrc}
                    alt={`${product.store.name} logo`}
                    className="w-4 h-4 object-contain rounded"
                  />
                ) : (
                  <Store className="h-3 w-3" />
                )}
                <span className="truncate">{product.store.name}</span>
              </Link>
            ) : (
              <span className="text-gray-400 italic">No store</span>
            )}

            {product.creator && (
              <Link
                to={`/user/${product.creator.id}`}
                className="flex items-center gap-1 text-secondary hover:text-foreground transition-colors"
                title={`View ${displayCreator}'s profile`}
              >
                <User className="h-3 w-3" />
                <span className="truncate">{displayCreator}</span>
              </Link>
            )}
          </div>

          {product.updated_at && (
            <div className="text-xs text-gray-500 dark:text-gray-400">
              Updated: {new Date(product.updated_at).toLocaleDateString(undefined, {
                month: 'short',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}