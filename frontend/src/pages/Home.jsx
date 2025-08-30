// frontend/src/pages/Home.jsx
/**
 * Home Component - Main search interface content
 * 
 * This component renders the main product/store search results grid.
 * The SearchBar is provided by the Layout component and is visible on all pages.
 * 
 * Scope:
 * - Product/Store grid display with infinite scroll
 * - Search state management (receives search params from Layout's SearchBar)
 * - Data fetching and filtering logic
 * 
 * The Layout component handles:
 * - SearchBar (visible on all pages, functional on home page)
 * - Authentication modal management
 * - Overall page structure and styling
 */
import { useState, useEffect, useCallback } from "react";
import api from "../api";
import ListView from "./ListView";
import { useInfiniteScroll } from "../hooks/useInfiniteScroll";

export default function Home() {
  const [products, setProducts] = useState([]);
  const [stores, setStores] = useState([]);
  const [hasMore, setHasMore] = useState(true);
  const [offset, setOffset] = useState(0);
  const [searchParams, setSearchParams] = useState({
    query: "",
    searchType: "products",
    priceMin: 0,
    priceMax: 500,
    selectedTags: [],
    sortBy: "random",
  });

  const fetchData = useCallback(async (reset = true, currentSearchParams = searchParams, currentOffset = offset) => {
    console.log('fetchData: currentSearchParams', currentSearchParams);
    try {
      const offsetToUse = reset ? 0 : currentOffset;
      let response;
      
      if (currentSearchParams.searchType === "products") {
        console.log('fetchData: Sending product query', currentSearchParams.query);
        response = await api.get("/v1/products/", {
          params: {
            q: currentSearchParams.query,
            min_price: currentSearchParams.priceMin,
            max_price: currentSearchParams.priceMax,
            sort_by: currentSearchParams.sortBy,
            tags: currentSearchParams.selectedTags.join(","),
            limit: 20,
            offset: offsetToUse,
          },
        });
        
        console.log('fetchData: Product API response', response.data);
        if (reset) {
          console.log('fetchData: Setting products to', response.data);
          setProducts(response.data);
        } else {
          setProducts(prev => {
            const existingIds = new Set(prev.map(item => item.id));
            const newItems = response.data.filter(item => !existingIds.has(item.id));
            const updatedProducts = [...prev, ...newItems];
            console.log('fetchData: Appending products, new total:', updatedProducts.length);
            return updatedProducts;
          });
        }
      } else {
        console.log('fetchData: Sending store query', currentSearchParams.query);
        response = await api.get("/v1/stores/", {
          params: {
            q: currentSearchParams.query,
            sort_by: currentSearchParams.sortBy,
            tags: currentSearchParams.selectedTags.join(","),
            limit: 20,
            offset: offsetToUse,
          },
        });
        
        console.log('fetchData: Store API response', response.data);
        if (reset) {
          console.log('fetchData: Setting stores to', response.data);
          setStores(response.data);
        } else {
          setStores(prev => {
            const existingIds = new Set(prev.map(item => item.id));
            const newItems = response.data.filter(item => !existingIds.has(item.id));
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
    } catch (error) {
      console.error(`Error fetching ${currentSearchParams.searchType}:`, error);
      console.error('Error details:', error.response?.data || error.message);
    }
  }, []);

  const fetchMoreData = useCallback(() => {
    return fetchData(false, searchParams, offset);
  }, [searchParams, offset, fetchData]);

  const [isFetching] = useInfiniteScroll(fetchMoreData, hasMore);

  useEffect(() => {
    console.log('Home.jsx: searchParams changed', searchParams);
    setOffset(0);
    setHasMore(true);
    fetchData(true, searchParams, 0);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchParams]);

  // Debug: Log when products/stores state actually changes
  useEffect(() => {
    console.log('Home.jsx: Products state updated, count:', products.length);
  }, [products]);

  useEffect(() => {
    console.log('Home.jsx: Stores state updated, count:', stores.length);
  }, [stores]);

  // Expose setSearchParams to parent via useImperativeHandle or props
  // For now, we'll use a global approach via window object as a quick solution
  useEffect(() => {
    window.homeSearchHandler = (params) => {
      console.log('Home.jsx: window.homeSearchHandler called with params', params);
      setSearchParams(params);
    };
    return () => {
      delete window.homeSearchHandler;
    };
  }, []);

  return (
    <>
      <h2 className="text-lg font-semibold mb-4">
        {searchParams.searchType === "products"
          ? "Latest products"
          : "Latest stores"}
      </h2>
      {searchParams.searchType === "products" ? (
        <ListView items={products} />
      ) : (
        <ListView items={stores} />
      )}
      
      {isFetching && (
        <div className="flex justify-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      )}
      
      {!hasMore && (searchParams.searchType === "products" ? products.length > 0 : stores.length > 0) && (
        <div className="text-center py-8 text-muted">
          No more {searchParams.searchType} to load
        </div>
      )}
    </>
  );
}