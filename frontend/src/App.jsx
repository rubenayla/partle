import { useEffect, useState } from "react";
import ListView from "./pages/ListView";
import MapView from "./pages/MapView";

export default function App() {
  const [view, setView] = useState("list");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [filtered, setFiltered] = useState([]);

  // Load data once
  useEffect(() => {
    fetch("/api/search.json")
      .then((res) => res.json())
      .then((data) => {
        setResults(data);
        setFiltered(data);
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
      {/* Full-width background bar */}
      <div className="w-screen bg-gray-50">
        {/* Centered content container with narrower max-width */}
        <div className="w-full max-w-3xl mx-auto px-8 py-6">
          {/* Header: logo/buttons on left, search on right */}
          <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
            <div className="flex items-center gap-4">
              <span className="text-2xl font-bold text-blue-600">Partle</span>
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
            </div>
            <div className="flex items-center gap-2 flex-1 min-w-[200px]">
              <input
                type="text"
                placeholder="Search a part…"
                className="flex-1 border rounded p-2"
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
          </div>

          {/* Main content */}
          {view === "list" ? (
            <ListView results={filtered} />
          ) : (
            <MapView
              results={results}
              highlights={filtered.map((r) => r.storeId)}
            />
          )}
        </div>
      </div>
    </main>
  );
}
