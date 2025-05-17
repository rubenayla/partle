import { useEffect, useState } from "react";
import ListView from "./pages/ListView";
import MapView from "./pages/MapView";

export default function App() {
  const [view, setView] = useState("list");
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [filtered, setFiltered] = useState([]);

  // Load data once from backend
  useEffect(() => {
    Promise.all([
      fetch("http://localhost:8000/v1/parts").then((res) => res.json()),
      fetch("http://localhost:8000/v1/stores").then((res) => res.json()),
    ]).then(([parts, stores]) => {
      const storeMap = {};
      for (const store of stores) {
        storeMap[store.id] = store.name;
      }
      
      
      const enriched = parts.map((p) => {
        const store = stores.find((s) => s.id === p.store_id);
        return {
          id: p.id,
          name: p.name,
          sku: p.sku, // Stock Keeping Unit: Id of store, not manufacturer
          price: p.price,
          qty: p.stock,
          storeId: p.store_id,
          storeName: store?.name || "Unknown store",
          lat: store?.lat,
          lng: store?.lon,
          distanceKm: 0                // ⏱ placeholder for now
        };
      });

      console.log("Fetched parts:", parts);
      console.log("Fetched stores:", stores);
      console.log("Enriched:", enriched);
      
      setResults(enriched);
      setFiltered(enriched);
    });
  }, []);

  // React to search input
  useEffect(() => {
    const q = query.toLowerCase();
    setFiltered(
      results.filter((item) =>
        `${item.storeName} ${item.name}`.toLowerCase().includes(q)
      )
    );
  }, [query, results]);

  return (
    <main className="min-h-screen bg-gray-50 text-gray-900">
      <div className="w-screen bg-gray-50">
        <div className="w-full max-w-4xl mx-auto px-8 py-6">
          {/* Header */}
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
