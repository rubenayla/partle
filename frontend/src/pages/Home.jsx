// frontend/src/pages/Home.jsx
import React, { useState, useEffect } from "react";
import axios from "axios";
import SearchBar from "../components/SearchBar";
import ListView   from "./ListView";
import AuthModal  from "../components/AuthModal";

export default function Home() {
  /** ─── Auth flag ─────────────────────────────────────────────── */
  const [isLoggedIn, setIsLoggedIn] = useState(
    !!localStorage.getItem("token")
  );

  /** ─── Modal visibility ──────────────────────────────────────── */
  const [accountOpen, setAccountOpen] = useState(false);

  const [products, setProducts] = useState([]);
  const [filters, setFilters] = useState({ query: '', priceMin: 0, priceMax: 500, sortBy: 'relevance', selectedTags: [] });

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const params = {
          q: filters.query,
          min_price: filters.priceMin,
          max_price: filters.priceMax,
          sort_by: filters.sortBy,
          tags: filters.selectedTags.join(','), // Pass tags as a comma-separated string
        };
        const response = await axios.get("/api/v1/products", { params });
        console.log("API Response Data:", response.data);
        setProducts(response.data);
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    };
    fetchProducts();
  }, [filters]);

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
        onSearch={(newFilters) => setFilters(newFilters)}
      />

      {accountOpen && (
        <AuthModal
          onClose={() => setAccountOpen(false)}
          onSuccess={() => setIsLoggedIn(true)}
        />
      )}

      <main className="flex-1 pt-24">
        <div className="w-full max-w-screen-2xl mx-auto px-4">
          <h2 className="text-lg font-semibold mb-4">Latest products</h2>
          <ListView products={products} />
        </div>
      </main>
    </div>
  );
}
