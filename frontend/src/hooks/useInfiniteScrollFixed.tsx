/**
 * @fileoverview useInfiniteScrollFixed Hook - Fixed version of infinite scroll hook
 * @module hooks/useInfiniteScrollFixed
 */
import React from 'react';

/**
 * useInfiniteScrollFixed Hook - Infinite scroll with fixed React hooks implementation
 * 
 * Provides infinite scrolling functionality by monitoring scroll position
 * and triggering data fetching when user approaches page bottom.
 * 
 * @param fetchMore - Function to fetch additional data
 * @param hasMore - Whether more data is available to fetch
 * @param threshold - Distance from bottom to trigger loading (pixels)
 * @returns Array containing isFetching boolean state
 * 
 * @example
 * ```tsx
 * function ProductList() {
 *   const [products, setProducts] = useState([]);
 *   const [hasMore, setHasMore] = useState(true);
 *   
 *   const fetchMoreProducts = async () => {
 *     const newProducts = await api.getProducts(products.length);
 *     setProducts(prev => [...prev, ...newProducts]);
 *     setHasMore(newProducts.length > 0);
 *   };
 *   
 *   const [isFetching] = useInfiniteScrollFixed(fetchMoreProducts, hasMore, 800);
 *   
 *   return (
 *     <div>
 *       {products.map(product => <ProductCard key={product.id} product={product} />)}
 *       {isFetching && <LoadingSpinner />}
 *     </div>
 *   );
 * }
 * ```
 */
export function useInfiniteScrollFixed(
  fetchMore: () => Promise<void>,
  hasMore: boolean = true,
  threshold: number = 1000
): [boolean] {
  const [isFetching, setIsFetching] = React.useState<boolean>(false);
  
  /**
   * Handle scroll event to check if more data should be fetched
   * Triggers fetchMore when user scrolls near bottom of page
   */
  const handleScroll = React.useCallback(() => {
    if (
      window.innerHeight + document.documentElement.scrollTop >=
      document.documentElement.offsetHeight - threshold &&
      hasMore &&
      !isFetching
    ) {
      setIsFetching(true);
      fetchMore().finally(() => setIsFetching(false));
    }
  }, [hasMore, isFetching, fetchMore, threshold]);

  // Set up scroll event listener
  React.useEffect(() => {
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [handleScroll]);

  return [isFetching];
}