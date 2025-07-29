// frontend/src/hooks/useInfiniteScroll.js
import { useState, useEffect, useCallback } from 'react';

export function useInfiniteScroll(fetchMore, hasMore = true) {
  const [isFetching, setIsFetching] = useState(false);

  const isScrolling = useCallback(() => {
    if (window.innerHeight + document.documentElement.scrollTop !== document.documentElement.offsetHeight || isFetching) {
      return;
    }
    setIsFetching(true);
  }, [isFetching]);

  useEffect(() => {
    if (!isFetching || !hasMore) return;
    
    const loadMore = async () => {
      await fetchMore();
      setIsFetching(false);
    };

    loadMore();
  }, [isFetching, fetchMore, hasMore]);

  useEffect(() => {
    if (!hasMore) return;
    
    window.addEventListener('scroll', isScrolling);
    return () => window.removeEventListener('scroll', isScrolling);
  }, [isScrolling, hasMore]);

  return [isFetching, setIsFetching];
}