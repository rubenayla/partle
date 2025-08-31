// frontend/src/hooks/useInfiniteScroll.js
import { useState, useEffect, useCallback } from 'react';

export function useInfiniteScroll(fetchMore, hasMore = true) {
  // Defensive check - ensure we're in a React component context
  if (typeof useState !== 'function') {
    console.error('useInfiniteScroll: React hooks not available');
    return [false, () => {}];
  }
  
  const [isFetching, setIsFetching] = useState(false);

  const handleScroll = useCallback(() => {
    // Check if we're at the bottom of the page
    if (
      window.innerHeight + document.documentElement.scrollTop >=
      document.documentElement.offsetHeight - 1000 // Start loading 1000px before bottom
    ) {
      if (!isFetching && hasMore) {
        setIsFetching(true);
      }
    }
  }, [isFetching, hasMore]);

  useEffect(() => {
    if (!isFetching || !hasMore) return;
    
    const loadMore = async () => {
      try {
        await fetchMore();
      } catch (error) {
        console.error('Error fetching more data:', error);
      } finally {
        setIsFetching(false);
      }
    };

    loadMore();
  }, [isFetching, fetchMore, hasMore]);

  useEffect(() => {
    if (!hasMore) return;
    
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [handleScroll, hasMore]);

  return [isFetching, setIsFetching];
}