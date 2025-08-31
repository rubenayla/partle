/**
 * @fileoverview InfiniteScrollWrapper Component - Component-based infinite scroll without hooks issues
 * @module components/InfiniteScrollWrapper
 */
import React, { useState, useEffect, useCallback, ReactNode } from 'react';

/**
 * Render props for infinite scroll children
 */
interface InfiniteScrollRenderProps {
  /** Whether data is currently being fetched */
  isFetching: boolean;
}

/**
 * Props for the InfiniteScrollWrapper component
 */
interface InfiniteScrollWrapperProps {
  /** Child components or render prop function */
  children: ReactNode | ((props: InfiniteScrollRenderProps) => ReactNode);
  /** Function to fetch more data when scroll threshold is reached */
  fetchMore: () => Promise<void>;
  /** Whether more data is available to fetch */
  hasMore?: boolean;
  /** Distance from bottom to trigger loading (pixels) */
  threshold?: number;
}

/**
 * InfiniteScrollWrapper Component - Component-based infinite scroll
 * 
 * Provides infinite scrolling functionality without using hooks in a problematic way.
 * Monitors scroll position and triggers data fetching when user approaches bottom.
 * 
 * @param props - Component props
 * @returns JSX element wrapping children with infinite scroll behavior
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
 *   return (
 *     <InfiniteScrollWrapper
 *       fetchMore={fetchMoreProducts}
 *       hasMore={hasMore}
 *       threshold={800}
 *     >
 *       {({ isFetching }) => (
 *         <div>
 *           {products.map(product => <ProductCard key={product.id} product={product} />)}
 *           {isFetching && <LoadingSpinner />}
 *         </div>
 *       )}
 *     </InfiniteScrollWrapper>
 *   );
 * }
 * ```
 */
export function InfiniteScrollWrapper({ 
  children, 
  fetchMore, 
  hasMore = true, 
  threshold = 1000 
}: InfiniteScrollWrapperProps): JSX.Element {
  const [isFetching, setIsFetching] = useState<boolean>(false);

  /**
   * Handle scroll event to check if more data should be fetched
   * Triggers fetchMore when user scrolls near bottom of page
   */
  const handleScroll = useCallback(() => {
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
  useEffect(() => {
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [handleScroll]);

  // Pass isFetching to children if using render prop pattern
  return (
    <>
      {typeof children === 'function' 
        ? children({ isFetching })
        : children}
    </>
  );
}