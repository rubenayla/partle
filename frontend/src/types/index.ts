/**
 * @fileoverview Central type definitions for the Partle application
 * @module types
 */

/**
 * Supported store types in the application
 */
export type StoreType = 'physical' | 'online' | 'chain';

/**
 * Theme options for the application
 */
export type Theme = 'light' | 'dark' | 'system';

/**
 * Backend service health status
 */
export type BackendStatus = 'online' | 'offline' | 'checking';

/**
 * Search type filter options
 */
export type SearchType = 'products' | 'stores';

/**
 * Sort order options for search results
 */
export type SortOrder = 'asc' | 'desc';

/**
 * Product sort field options
 */
export type ProductSortBy = 'name' | 'price' | 'created_at' | 'updated_at';

/**
 * Store entity representing a retail location or website
 */
export interface Store {
  /** Unique store identifier */
  id: number;
  /** Store name */
  name: string;
  /** Store type classification */
  type: StoreType;
  /** Store website URL (optional) */
  website?: string;
  /** Store logo image URL (optional) */
  image_url?: string;
  /** Store description */
  description?: string;
  /** Physical address (for physical stores) */
  address?: string;
  /** Geographic latitude coordinate */
  latitude?: number;
  /** Geographic longitude coordinate */
  longitude?: number;
  /** When the store was created */
  created_at?: string;
  /** When the store was last updated */
  updated_at?: string;
  /** ID of the user who created this store */
  creator_id?: number;
}

/**
 * Product entity representing an item for sale
 */
export interface Product {
  /** Unique product identifier */
  id: number;
  /** Product name */
  name: string;
  /** Product description */
  description?: string;
  /** Product price in cents (to avoid floating point issues) */
  price?: number;
  /** Currency for the price (free text, defaults to €) */
  currency?: string;
  /** Product image filename (when stored in database) */
  image_filename?: string;
  /** Product image content type (when stored in database) */
  image_content_type?: string;
  /** URL to the product page on the store's website */
  url?: string;
  /** Store where this product is sold */
  store_id: number;
  /** Store information (populated via join) */
  store?: Store;
  /** Associated tags for categorization */
  tags?: Tag[];
  /** When the product was created */
  created_at?: string;
  /** When the product was last updated */
  updated_at?: string;
  /** ID of the user who created this product */
  creator_id?: number;
  /** Creator information (populated via join) */
  creator?: {
    id: number;
    username: string | null;
  };
}

/**
 * Tag entity for product categorization
 */
export interface Tag {
  /** Unique tag identifier */
  id: number;
  /** Tag name/label */
  name: string;
  /** Tag color for UI display (hex color) */
  color?: string;
  /** Number of products using this tag */
  product_count?: number;
}

/**
 * User entity representing a registered user
 */
export interface User {
  /** Unique user identifier */
  id: number;
  /** User's email address */
  email: string;
  /** User's unique username (optional until set) */
  username?: string | null;
  /** Whether the user's email has been verified */
  is_verified?: boolean;
  /** User's display name (optional) */
  display_name?: string;
  /** User's avatar image URL (optional) */
  avatar_url?: string;
  /** When the user account was created */
  created_at?: string;
  /** When the user account was last updated */
  updated_at?: string;
}

/**
 * Search parameters for filtering products
 */
export interface ProductSearchParams {
  /** Search query string */
  query: string;
  /** Search type (products or stores) */
  searchType: SearchType;
  /** Minimum price filter (in cents) */
  priceMin: number;
  /** Maximum price filter (in cents) */
  priceMax: number;
  /** Selected tag IDs for filtering */
  selectedTags: number[];
  /** Sort field */
  sortBy: ProductSortBy;
  /** Sort order */
  sortOrder: SortOrder;
  /** Store type filter */
  storeType?: StoreType;
}

/**
 * API response wrapper for paginated results
 */
export interface PaginatedResponse<T> {
  /** Array of result items */
  items: T[];
  /** Total number of items available */
  total: number;
  /** Current page number (0-based) */
  page: number;
  /** Number of items per page */
  size: number;
  /** Whether there are more pages available */
  has_more: boolean;
}

/**
 * API error response structure
 */
export interface ApiError {
  /** Error message for display */
  detail: string;
  /** HTTP status code */
  status?: number;
  /** Error type/code for programmatic handling */
  error_code?: string;
  /** Additional error context */
  context?: Record<string, unknown>;
}

/**
 * Geographic coordinate pair
 */
export interface Coordinates {
  /** Latitude in decimal degrees */
  latitude: number;
  /** Longitude in decimal degrees */
  longitude: number;
}

/**
 * Geographic bounds for map display
 */
export interface Bounds {
  /** Southwest corner coordinates */
  southwest: Coordinates;
  /** Northeast corner coordinates */
  northeast: Coordinates;
}

/**
 * Form validation error structure
 */
export interface FormError {
  /** Form field name */
  field: string;
  /** Error message for the field */
  message: string;
}

/**
 * Authentication context value
 */
export interface AuthContextValue {
  /** Currently authenticated user (null if not logged in) */
  user: User | null;
  /** Whether authentication status is being loaded */
  isLoading: boolean;
  /** Function to log in a user */
  login: (email: string, password: string) => Promise<void>;
  /** Function to log out the current user */
  logout: () => void;
  /** Function to register a new user */
  register: (email: string, password: string) => Promise<void>;
}

/**
 * Theme context value
 */
export interface ThemeContextValue {
  /** Current theme setting */
  theme: Theme;
  /** Function to change the theme */
  setTheme: (theme: Theme) => void;
}

/**
 * Component props for items that can be displayed in list view
 */
export interface ListViewItem {
  /** Unique identifier */
  id: number;
  /** Display name */
  name: string;
  /** Optional image URL */
  image_url?: string;
  /** Optional price (for products) */
  price?: number;
  /** Optional description */
  description?: string;
  /** Optional URL link */
  url?: string;
  /** Optional store information (for products) */
  store?: Store;
  /** Optional creator ID (for access control) */
  creator_id?: number;
}

/**
 * Props for infinite scroll functionality
 */
export interface InfiniteScrollProps {
  /** Function to fetch more data */
  fetchMore: () => Promise<void>;
  /** Whether more data is available */
  hasMore: boolean;
  /** Distance from bottom to trigger loading (pixels) */
  threshold?: number;
  /** Whether to use passive event listeners */
  passive?: boolean;
}

/**
 * Map component props
 */
export interface MapProps {
  /** Stores to display on the map */
  stores: Store[];
  /** Map center coordinates */
  center?: Coordinates;
  /** Map zoom level */
  zoom?: number;
  /** Map bounds */
  bounds?: Bounds;
  /** Callback when store marker is clicked */
  onStoreClick?: (store: Store) => void;
}