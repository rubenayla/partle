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
      <div className="max-w-xl mx-auto p-6">
        <h1 className="text-3xl font-bold text-blue-600 mb-4">Partle</h1>

        <input
          type="text"
          placeholder="Search a part (e.g. JST 6-pin)"
          className="w-full border rounded p-2 mb-4"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />

        <div className="flex gap-2 mb-4">
          <button
            className={`flex-1 px-4 py-2 rounded ${
              view === "list" ? "bg-blue-600 text-white" : "bg-gray-200"
            }`}
            onClick={() => setView("list")}
          >
            List
          </button>
          <button
            className={`flex-1 px-4 py-2 rounded ${
              view === "map" ? "bg-blue-600 text-white" : "bg-gray-200"
            }`}
            onClick={() => setView("map")}
          >
            Map
          </button>
        </div>

        {view === "list" ? (
          <ListView results={filtered} />
        ) : (
          <MapView results={results} highlights={filtered.map((r) => r.storeId)} />
        )}
      </div>
    </main>
  );
}
