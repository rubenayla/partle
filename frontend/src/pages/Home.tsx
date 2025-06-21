// frontend/src/pages/Home.tsx
import { useState, useEffect } from "react";
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

  /* keep isLoggedIn fresh (other tab → logout, etc.) */
  useEffect(() => {
    const id = setInterval(
      () => setIsLoggedIn(!!localStorage.getItem("token")),
      1000
    );
    return () => clearInterval(id);
  }, []);

  return (
    <div className="min-h-screen w-screen flex flex-col bg-background text-primary">
      
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
          <ListView />
        </div>
      </main>
    </div>
  );
}
