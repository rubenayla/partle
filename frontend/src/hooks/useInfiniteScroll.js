// frontend/src/hooks/useInfiniteScroll.js
import { useState, useEffect, useRef, useCallback } from 'react';

/**
 * Optimized infinite scroll hook with performance best practices
 * @param {Function} fetchMore - Function to fetch more data
 * @param {boolean} hasMore - Whether more data is available
 * @param {number} threshold - Pixels from bottom to trigger load (default: 1000)
 * @returns {[boolean]} - [isFetching]
 */
export function useInfiniteScroll(fetchMore, hasMore = true, threshold = 1000) {
  const [isFetching, setIsFetching] = useState(false);
  
  // Use refs to avoid stale closures and unnecessary re-renders
  const fetchMoreRef = useRef(fetchMore);
  const hasMoreRef = useRef(hasMore);
  const isFetchingRef = useRef(isFetching);
  const thresholdRef = useRef(threshold);
  
  // Update refs when props change
  fetchMoreRef.current = fetchMore;
  hasMoreRef.current = hasMore;
  isFetchingRef.current = isFetching;
  thresholdRef.current = threshold;
  
  // Throttled scroll handler for performance
  const handleScroll = useCallback(() => {
    // Use refs to avoid stale closures - no dependency array needed!
    if (
      window.innerHeight + document.documentElement.scrollTop >=
      document.documentElement.offsetHeight - thresholdRef.current &&
      hasMoreRef.current &&
      !isFetchingRef.current
    ) {
      setIsFetching(true);
      
      // Execute fetch and handle completion
      Promise.resolve(fetchMoreRef.current())
        .then(() => setIsFetching(false))
        .catch((error) => {
          console.error('Infinite scroll fetch error:', error);
          setIsFetching(false);
        });
    }
  }, []); // Empty dependency array - uses refs for current values!
  
  // Throttled scroll listener for performance
  const throttledScrollHandler = useRef(null);
  
  useEffect(() => {
    // Create throttled version (16ms = ~60fps)
    let timeoutId;
    throttledScrollHandler.current = () => {
      if (timeoutId) return; // Already scheduled
      
      timeoutId = setTimeout(() => {
        handleScroll();
        timeoutId = null;
      }, 16);
    };
    
    if (hasMore) {
      window.addEventListener('scroll', throttledScrollHandler.current, { passive: true });
    }
    
    return () => {
      window.removeEventListener('scroll', throttledScrollHandler.current);
      if (timeoutId) clearTimeout(timeoutId);
    };
  }, [hasMore, handleScroll]); // Only re-run if hasMore changes
  
  return [isFetching];
}