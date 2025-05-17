import { useEffect, useState } from "react";
import ListView from "./pages/ListView";
import MapView from "./pages/MapView";

export default function App() {
  const [view, setView] = useState("list");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);     // all data
  const [filtered, setFiltered] = useState([]);   // only matches
  
  // Load data once
  useEffect(() => {
    fetch("/api/search.json")
      .then((res) => res.json())
      .then((data) => {
        setResults(data);    // store full dataset
        setFiltered(data);   // default: show all
      });
  }, []);
  
  // React to search input
  useEffect(() => {
    const q = query.toLowerCase();
    setFiltered(
      results.filter((item) =>
        `${item.storeName} ${item.partName}`.toLowerCase().includes(q)
      )
    );
  }, [query, results]);
  
  return (
    <main className="min-h-screen bg-gray-50 text-gray-900">
      <div className="w-full max-w-5xl mx-auto px-4 py-4">
      <div className="flex flex-wrap items-center gap-2 mb-6">
        <span className="text-2xl font-bold text-blue-600 mr-4">Partle</span>

        <button
          className={`px-4 py-2 rounded ${
            view === "list" ? "bg-blue-600 text-white" : "bg-gray-200"
          }`}
          onClick={() => setView("list")}
        >
          List
        </button>
        <button
          className={`px-4 py-2 rounded ${
            view === "map" ? "bg-blue-600 text-white" : "bg-gray-200"
          }`}
          onClick={() => setView("map")}
        >
          Map
        </button>

        <input
          type="text"
          placeholder="Search a part..."
          className="flex-1 border rounded p-2 min-w-[180px]"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />

        <button
          className="px-4 py-2 bg-blue-600 text-white rounded"
          onClick={() => {}}
        >
          Search
        </button>
      </div>

      {/* content */}
      {view === "list" ? (
        <ListView results={filtered} />
      ) : (
        <MapView results={results} highlights={filtered.map((r) => r.storeId)} />
      )}
    </div>

    </main>
  );
}
