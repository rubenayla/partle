// useInfiniteScrollFixed.jsx - Testing with JSX extension and React import
import React from 'react';

export function useInfiniteScrollFixed(fetchMore, hasMore = true, threshold = 1000) {
  const [isFetching, setIsFetching] = React.useState(false);
  
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

  React.useEffect(() => {
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, [handleScroll]);

  return [isFetching];
}