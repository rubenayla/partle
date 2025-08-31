// InfiniteScrollWrapper.jsx - Component-based approach to avoid hook issues
import { useState, useEffect, useCallback } from 'react';

export function InfiniteScrollWrapper({ 
  children, 
  fetchMore, 
  hasMore = true, 
  threshold = 1000 
}) {
  const [isFetching, setIsFetching] = useState(false);

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

  useEffect(() => {
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [handleScroll]);

  // Pass isFetching to children
  return typeof children === 'function' 
    ? children({ isFetching })
    : children;
}