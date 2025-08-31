/**
 * @fileoverview Home Component - Main search interface content
 * @module pages/Home
 */
import { useState, useEffect, useCallback } from 'react';
import api from '../api';
import ListView from './ListView';
import { useInfiniteScroll } from '../hooks/useInfiniteScroll';
import { Product, Store, ProductSearchParams } from '../types';

/**
 * API response type for paginated data
 */
interface ApiResponse<T> {
  data: T[];
}

/**
 * Home Component - Main search interface content
 * 
 * This component renders the main product/store search results grid.
 * The SearchBar is provided by the Layout component and is visible on all pages.
 * 
 * Features:
 * - Product/Store grid display with infinite scroll
 * - Search state management (receives search params from Layout's SearchBar)
 * - Data fetching and filtering logic
 * - Automatic loading of more results when scrolling
 * 
 * The Layout component handles:
 * - SearchBar (visible on all pages, functional on home page)
 * - Authentication modal management
 * - Overall page structure and styling
 * 
 * @returns JSX element containing the search results grid
 * 
 * @example
 * ```tsx
 * function App() {
 *   return (
 *     <Layout>
 *       <Routes>
 *         <Route path="/" element={<Home />} />
 *       </Routes>
 *     </Layout>
 *   );
 * }
 * ```
 */
export default function Home() {
  const [products, setProducts] = useState<Product[]>([]);
  const [stores, setStores] = useState<Store[]>([]);
  const [hasMore, setHasMore] = useState<boolean>(true);
  const [offset, setOffset] = useState<number>(0);
  const [searchParams, setSearchParams] = useState<ProductSearchParams>({
    query: '',
    searchType: 'products',
    priceMin: 0,
    priceMax: 500,
    selectedTags: [],
    sortBy: 'created_at',
    sortOrder: 'desc'
  });

  /**
   * Fetch products or stores based on current search parameters
   * 
   * @param reset - Whether to reset results (true) or append to existing (false)
   * @param currentSearchParams - Search parameters to use for the request
   * @param currentOffset - Pagination offset to use
   */
  const fetchData = useCallback(async (
    reset: boolean = true, 
    currentSearchParams: ProductSearchParams = searchParams, 
    currentOffset: number = offset
  ) => {
    try {
      const offsetToUse = reset ? 0 : currentOffset;
      let response: ApiResponse<Product | Store>;
      
      if (currentSearchParams.searchType === 'products') {
        // Searching products
        const productParams: Record<string, any> = {
          q: currentSearchParams.query,
          min_price: currentSearchParams.priceMin,
          max_price: currentSearchParams.priceMax,
          sort_by: currentSearchParams.sortBy,
          tags: currentSearchParams.selectedTags.join(','),
          limit: 20,
          offset: offsetToUse,
        };
        
        // Add store_name filter if provided via search operators
        if (currentSearchParams.storeType) {
          productParams.store_type = currentSearchParams.storeType;
        }
        
        response = await api.get('/v1/products/', {
          params: productParams,
        });
        
        // Product API response received
        if (reset) {
          // Setting products (reset)
          setProducts(response.data as Product[]);
        } else {
          setProducts(prev => {
            const existingIds = new Set(prev.map(item => item.id));
            const newItems = (response.data as Product[]).filter(item => !existingIds.has(item.id));
            const updatedProducts = [...prev, ...newItems];
            // Appending products
            return updatedProducts;
          });
        }
      } else {
        console.log('fetchData: Sending store query', currentSearchParams.query);
        response = await api.get('/v1/stores/', {
          params: {
            q: currentSearchParams.query,
            sort_by: currentSearchParams.sortBy,
            tags: currentSearchParams.selectedTags.join(','),
            limit: 20,
            offset: offsetToUse,
          },
        });
        
        console.log('fetchData: Store API response', response.data);
        if (reset) {
          console.log('fetchData: Setting stores to', response.data);
          setStores(response.data as Store[]);
        } else {
          setStores(prev => {
            const existingIds = new Set(prev.map(item => item.id));
            const newItems = (response.data as Store[]).filter(item => !existingIds.has(item.id));
            const updatedStores = [...prev, ...newItems];
            console.log('fetchData: Appending stores, new total:', updatedStores.length);
            return updatedStores;
          });
        }
      }
      
      // Update pagination state
      if (reset) {
        setOffset(20);
        setHasMore(response.data.length === 20);
      } else {
        setOffset(prev => prev + 20);
        setHasMore(response.data.length === 20);
      }
    } catch (error: any) {
      console.error(`Error fetching ${currentSearchParams.searchType}:`, error);
      console.error('Error details:', error.response?.data || error.message);
      
      // Ensure state remains as arrays even on error
      if (reset) {
        if (currentSearchParams.searchType === 'products') {
          setProducts([]);
        } else {
          setStores([]);
        }
        setOffset(0);
        setHasMore(false);
      }
    }
  }, []);

  /**
   * Fetch more data for infinite scroll
   * Uses current search parameters and offset
   */
  const fetchMoreData = useCallback((): Promise<void> => {
    return fetchData(false, searchParams, offset);
  }, [searchParams, offset, fetchData]);

  // Use infinite scroll hook for automatic loading
  const isFetching = useInfiniteScroll(fetchMoreData, hasMore);

  useEffect(() => {
    // Search params changed, resetting results
    setOffset(0);
    setHasMore(true);
    fetchData(true, searchParams, 0);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchParams]);

  // Debug: Track state changes in development
  useEffect(() => {
    if (import.meta.env.DEV) {
      console.debug('Products updated:', products.length);
    }
  }, [products]);

  useEffect(() => {
    if (import.meta.env.DEV) {
      console.debug('Stores updated:', stores.length);
    }
  }, [stores]);

  // Expose setSearchParams to parent via global window object
  // TODO: Replace with proper React context or props drilling
  useEffect(() => {
    // Type assertion for global window property
    (window as any).homeSearchHandler = (params: ProductSearchParams) => {
      console.log('Home.tsx: window.homeSearchHandler called with params', params);
      setSearchParams(params);
    };
    return () => {
      delete (window as any).homeSearchHandler;
    };
  }, []);

  return (
    <>
      <h2 className="text-lg font-semibold mb-4">
        {searchParams.searchType === 'products'
          ? 'Latest products'
          : 'Latest stores'}
      </h2>
      {searchParams.searchType === 'products' ? (
        <ListView items={products} />
      ) : (
        <ListView items={stores} />
      )}
      
      {isFetching && (
        <div className="flex justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      )}
      
      {!hasMore && (searchParams.searchType === 'products' ? products.length > 0 : stores.length > 0) && (
        <div className="text-center py-8 text-muted">
          No more {searchParams.searchType} to load
        </div>
      )}
    </>
  );
}
