import { useState } from "react";
import SearchBar from "../components/SearchBar";
import ListView from "./ListView";
import AuthModal from "../components/AuthModal";

export default function Home() {
  const [accountOpen, setAccountOpen] = useState(false);

  return (
    <div className="min-h-screen w-screen flex flex-col bg-white text-gray-900">
      <SearchBar onAccountClick={() => setAccountOpen(true)} />
      {accountOpen && <AuthModal onClose={() => setAccountOpen(false)} />}
      <main className="flex-1 pt-24">
        <div className="w-full max-w-screen-2xl mx-auto px-4">
          <h2 className="text-lg font-semibold mb-4">Latest products</h2>
          <ListView />
        </div>
      </main>
    </div>
  );
}
