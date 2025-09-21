import { Link } from 'react-router-dom';
import { Store, MapPin, Globe, User, Upload } from 'lucide-react';
import { useAuth } from '../hooks/useAuth';

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

interface StoreCardProps {
  store: StoreData;
}

export default function StoreCard({ store }: StoreCardProps) {
  const { user } = useAuth();
  const isOwner = user?.id === store.owner_id;

  const getTypeIcon = () => {
    switch (store.type) {
      case 'physical':
        return <MapPin className="h-4 w-4" />;
      case 'online':
        return <Globe className="h-4 w-4" />;
      case 'chain':
        return <Store className="h-4 w-4" />;
      default:
        return <Store className="h-4 w-4" />;
    }
  };

  const getTypeLabel = () => {
    switch (store.type) {
      case 'physical':
        return 'Physical Store';
      case 'online':
        return 'Online Store';
      case 'chain':
        return 'Chain Store';
      default:
        return 'Store';
    }
  };

  return (
    <div className="bg-surface rounded-lg shadow-md border border-gray-300 dark:border-gray-600 p-4 hover:shadow-lg transition-shadow">
      <div className="flex items-start justify-between mb-3">
        <Link to={`/stores/${store.id}/products`}>
          <h3 className="font-semibold text-foreground hover:text-accent transition-colors">
            {store.name}
          </h3>
        </Link>
        <span className="flex items-center gap-1 text-xs text-secondary bg-gray-100 dark:bg-gray-800 px-2 py-1 rounded">
          {getTypeIcon()}
          <span>{getTypeLabel()}</span>
        </span>
      </div>

      {store.address && (
        <p className="text-sm text-secondary mb-2 flex items-start gap-1">
          <MapPin className="h-3 w-3 mt-0.5 flex-shrink-0" />
          <span className="line-clamp-2">{store.address}</span>
        </p>
      )}

      {store.homepage && (
        <a
          href={store.homepage}
          target="_blank"
          rel="noopener noreferrer"
          className="text-sm text-accent hover:underline flex items-center gap-1 mb-2"
        >
          <Globe className="h-3 w-3" />
          <span className="truncate">Visit website</span>
        </a>
      )}

      <div className="flex items-center justify-between mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-3">
          <Link
            to={`/stores/${store.id}/products`}
            className="text-sm text-accent hover:underline"
          >
            View products →
          </Link>
          {isOwner && (
            <Link
              to={`/stores/${store.id}/bulk-import`}
              className="flex items-center gap-1 text-sm text-green-600 hover:text-green-700 dark:text-green-400 dark:hover:text-green-300"
              title="Bulk import products"
            >
              <Upload className="h-3 w-3" />
              <span>Import</span>
            </Link>
          )}
        </div>

        {store.owner_id && !isOwner && (
          <Link
            to={`/user/${store.owner_id}`}
            className="flex items-center gap-1 text-xs text-secondary hover:text-accent transition-colors"
            title="View store owner's profile"
          >
            <User className="h-3 w-3" />
            <span>Owner</span>
          </Link>
        )}
      </div>
    </div>
  );
}