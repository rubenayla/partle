/**
 * @fileoverview Infinite scroll hook for loading more content as user scrolls
 * @module useInfiniteScroll
 */

import { useState, useEffect, useRef, useCallback } from 'react';

/**
 * Configuration options for infinite scroll behavior
 */
interface InfiniteScrollOptions {
  /** Distance from bottom of page (in pixels) to trigger loading */
  threshold?: number;
  /** Whether to use passive event listeners for better performance */
  passive?: boolean;
}

/**
 * Function signature for fetching more data
 * @returns Promise that resolves when data is loaded
 */
type FetchMoreFunction = () => Promise<void> | Promise<unknown> | void;

/**
 * Custom hook for implementing infinite scroll functionality
 * 
 * This hook automatically triggers data loading when the user scrolls near
 * the bottom of the page. It handles loading states and prevents duplicate
 * requests while data is being fetched.
 * 
 * @example
 * ```tsx
 * function ProductList() {
 *   const [products, setProducts] = useState<Product[]>([]);
 *   const [hasMore, setHasMore] = useState(true);
 *   
 *   const fetchMore = useCallback(async () => {
 *     const newProducts = await api.getProducts(products.length);
 *     if (newProducts.length === 0) setHasMore(false);
 *     else setProducts(prev => [...prev, ...newProducts]);
 *   }, [products.length]);
 *   
 *   const isFetching = useInfiniteScroll(fetchMore, hasMore, { threshold: 500 });
 *   
 *   return (
 *     <div>
 *       {products.map(product => <ProductCard key={product.id} product={product} />)}
 *       {isFetching && <LoadingSpinner />}
 *     </div>
 *   );
 * }
 * ```
 * 
 * @param fetchMore - Function to call when more data should be loaded
 * @param hasMore - Whether there is more data available to load
 * @param options - Configuration options for scroll behavior
 * @returns Boolean indicating if data is currently being fetched
 * 
 * @see {@link https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener#passive} For passive listeners
 */
export function useInfiniteScroll(
  fetchMore: FetchMoreFunction,
  hasMore: boolean = true,
  options: InfiniteScrollOptions = {}
): boolean {
  const { threshold = 1000, passive = true } = options;
  
  // Loading state for the hook consumer
  const [isFetching, setIsFetching] = useState<boolean>(false);
  
  // Refs to avoid stale closures and unnecessary re-renders
  // This pattern prevents the hook from recreating event listeners
  // when dependencies change, improving performance
  const fetchMoreRef = useRef<FetchMoreFunction>(fetchMore);
  const hasMoreRef = useRef<boolean>(hasMore);
  const thresholdRef = useRef<number>(threshold);
  
  // Update refs when values change - this ensures we always have
  // the latest values without causing effect re-runs
  fetchMoreRef.current = fetchMore;
  hasMoreRef.current = hasMore;
  thresholdRef.current = threshold;
  
  /**
   * Scroll event handler that checks if we should load more data
   * 
   * Calculates if user has scrolled to within the threshold distance
   * of the bottom of the document. Uses refs to access current values
   * without depending on them in the useCallback dependency array.
   */
  const handleScroll = useCallback(() => {
    // Calculate if we're close enough to the bottom to trigger loading
    const scrollTop = document.documentElement.scrollTop;
    const windowHeight = window.innerHeight;
    const documentHeight = document.documentElement.offsetHeight;
    
    const distanceFromBottom = documentHeight - (scrollTop + windowHeight);
    
    if (
      distanceFromBottom <= thresholdRef.current &&
      hasMoreRef.current &&
      !isFetching
    ) {
      setIsFetching(true);
      
      // Execute fetch function and handle completion
      // Supports both sync and async fetch functions
      Promise.resolve(fetchMoreRef.current())
        .then(() => setIsFetching(false))
        .catch((error: Error) => {
          console.error('Infinite scroll fetch error:', error);
          setIsFetching(false);
        });
    }
  }, [isFetching]); // Only isFetching in deps - refs handle everything else
  
  /**
   * Set up scroll event listener when component mounts or hasMore changes
   */
  useEffect(() => {
    if (!hasMore) {
      // No point in listening for scroll events if there's no more data
      return;
    }
    
    // Add scroll listener with optional passive flag for better performance
    // Passive listeners tell the browser we won't call preventDefault,
    // allowing for better scroll performance optimizations
    const eventOptions = passive ? { passive: true } : undefined;
    window.addEventListener('scroll', handleScroll, eventOptions);
    
    // Cleanup function to remove listener when component unmounts
    // or when dependencies change
    return () => {
      window.removeEventListener('scroll', handleScroll);
    };
  }, [hasMore, handleScroll, passive]);
  
  return isFetching;
}