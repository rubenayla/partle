// frontend/src/pages/Home.jsx
import { useState, useEffect, useCallback } from "react";
import axios from "axios";
import SearchBar from "../components/SearchBar";
import ListView from "./ListView";
import AuthModal from "../components/AuthModal";
import { useInfiniteScroll } from "../hooks/useInfiniteScroll";

export default function Home() {
  /** ─── Auth flag ─────────────────────────────────────────────── */
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("token")
  );

  /** ─── Modal visibility ──────────────────────────────────────── */
  const [accountOpen, setAccountOpen] = useState(false);

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
    try {
      const offsetToUse = reset ? 0 : currentOffset;
      let response;
      
      if (currentSearchParams.searchType === "products") {
        response = await axios.get("/api/v1/products", {
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
        
        if (reset) {
          setProducts(response.data);
        } else {
          setProducts(prev => [...prev, ...response.data]);
        }
      } else {
        response = await axios.get("/api/v1/stores", {
          params: {
            q: currentSearchParams.query,
            sort_by: currentSearchParams.sortBy,
            tags: currentSearchParams.selectedTags.join(","),
            limit: 20,
            offset: offsetToUse,
          },
        });
        
        if (reset) {
          setStores(response.data);
        } else {
          setStores(prev => [...prev, ...response.data]);
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
    }
  }, [searchParams, offset]);

  const fetchMoreData = useCallback(() => {
    return fetchData(false, searchParams, offset);
  }, [searchParams, offset, fetchData]);

  const [isFetching] = useInfiniteScroll(fetchMoreData, hasMore);

  useEffect(() => {
    setOffset(0);
    setHasMore(true);
    fetchData(true);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchParams]);

  /* keep isLoggedIn fresh (other tab → logout, etc.) */
  useEffect(() => {
    const id = setInterval(
      () => setIsLoggedIn(!!localStorage.getItem("token")),
      1000
    );
    return () => clearInterval(id);
  }, []);

  return (
    <div className="min-h-screen w-screen flex flex-col bg-background text-foreground">
      <SearchBar
        isLoggedIn={isLoggedIn}
        onAccountClick={() => setAccountOpen(true)}
        onSearch={setSearchParams}
      />

      {accountOpen && (
        <AuthModal
          onClose={() => setAccountOpen(false)}
          onSuccess={() => setIsLoggedIn(true)}
        />
      )}

      <main className="flex-1 pt-24">
        <div className="w-full max-w-screen-2xl mx-auto px-4">
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
        </div>
      </main>
    </div>
  );
}
