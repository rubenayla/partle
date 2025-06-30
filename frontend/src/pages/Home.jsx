// frontend/src/pages/Home.jsx
import { useState, useEffect } from "react";
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

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await axios.get("/api/v1/products");
        setProducts(response.data);
      } catch (error) {
        console.error("Error fetching products:", error);
      }
    };
    fetchProducts();
  }, []);

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
