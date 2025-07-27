// frontend/src/pages/Home.jsx
import { useState, useEffect } from "react";
import axios from "axios";
import SearchBar from "../components/SearchBar";
import ListView from "./ListView";
import AuthModal from "../components/AuthModal";

export default function Home() {
  /** ─── Auth flag ─────────────────────────────────────────────── */
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("token")
  );

  /** ─── Modal visibility ──────────────────────────────────────── */
  const [accountOpen, setAccountOpen] = useState(false);

  const [products, setProducts] = useState([]);
  const [stores, setStores] = useState([]);
  const [searchParams, setSearchParams] = useState({
    query: "",
    searchType: "products",
    priceMin: 0,
    priceMax: 500,
    selectedTags: [],
    sortBy: "relevance",
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        let response;
        if (searchParams.searchType === "products") {
          response = await axios.get("/api/v1/products", {
            params: {
              q: searchParams.query,
              min_price: searchParams.priceMin,
              max_price: searchParams.priceMax,
              sort_by: searchParams.sortBy,
              tags: searchParams.selectedTags.join(","),
            },
          });
          setProducts(response.data);
        } else {
          response = await axios.get("/api/v1/stores", {
            params: {
              q: searchParams.query,
              sort_by: searchParams.sortBy,
              tags: searchParams.selectedTags.join(","),
            },
          });
          setStores(response.data);
        }
      } catch (error) {
        console.error(`Error fetching ${searchParams.searchType}:`, error);
      }
    };
    fetchData();
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
        </div>
      </main>
    </div>
  );
}
