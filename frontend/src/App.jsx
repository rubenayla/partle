import { useState } from "react";
import ListView from "./pages/ListView";
import MapView from "./pages/MapView";
import data from "./data/mock_inventory.json";

export default function App() {
  const [view, setView] = useState("list");
  const [query, setQuery] = useState("");

  const filtered = data.filter((item) =>
    `${item.storeName} ${item.partName}`.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <main className="max-w-xl mx-auto p-6">
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
          className={`px-4 py-2 rounded ${
            view === "list" ? "bg-black text-white" : "bg-gray-200"
          }`}
          onClick={() => setView("list")}
        >
          List
        </button>
        <button
          className={`px-4 py-2 rounded ${
            view === "map" ? "bg-black text-white" : "bg-gray-200"
          }`}
          onClick={() => setView("map")}
        >
          Map
        </button>
      </div>

      {view === "list" ? (
        <ListView results={filtered} />
      ) : (
        <MapView results={filtered} />
      )}
    </main>
  );
}
