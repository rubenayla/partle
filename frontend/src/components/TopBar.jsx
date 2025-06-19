// frontend/src/components/TopBar.jsx
import { useState } from "react";

export default function TopBar({
  mode = "list",
  onModeChange = () => {},
  onSearch = () => {},
  onFiltersChange = () => {},
}) {
  const [query, setQuery] = useState("");
  const [priceMin, setPriceMin] = useState(0);
  const [priceMax, setPriceMax] = useState(500);
  const [sortBy, setSortBy] = useState("relevance");

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    onSearch(query.trim());
  };

  const emitFilters = (extra = {}) =>
    onFiltersChange({ priceMin, priceMax, sortBy, ...extra });

  return (
    <header className="sticky top-0 left-0 z-20 w-screen bg-white shadow-sm">
      <div className="flex items-center gap-4 px-4 py-2 overflow-x-auto whitespace-nowrap">
        {/* Logo */}
        <a href="/" className="text-xl font-semibold flex-shrink-0">
          Partle
        </a>

        {/* Search */}
        <form onSubmit={handleSearchSubmit} className="flex-1 min-w-[200px]">
          <input
            type="search"
            placeholder="Search products…"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full border rounded px-3 py-2"
          />
        </form>

        {/* Price range filters */}
        <label className="flex items-center gap-1 flex-shrink-0">
          €
          <input
            type="number"
            value={priceMin}
            min={0}
            onChange={(e) => {
              const v = Number(e.target.value);
              setPriceMin(v);
              emitFilters({ priceMin: v });
            }}
            className="w-16 border rounded px-1"
          />
          —
          <input
            type="number"
            value={priceMax}
            min={0}
            onChange={(e) => {
              const v = Number(e.target.value);
              setPriceMax(v);
              emitFilters({ priceMax: v });
            }}
            className="w-16 border rounded px-1"
          />
        </label>

        {/* Sort dropdown */}
        <select
          value={sortBy}
          onChange={(e) => {
            setSortBy(e.target.value);
            emitFilters({ sortBy: e.target.value });
          }}
          className="border rounded px-2 py-1 flex-shrink-0"
        >
          <option value="relevance">Relevance</option>
          <option value="price_asc">Price ↑</option>
          <option value="price_desc">Price ↓</option>
          <option value="distance">Closest</option>
        </select>

        {/* View toggle */}
        <button
          onClick={() => onModeChange(mode === "list" ? "map" : "list")}
          className="border px-2 py-1 rounded flex-shrink-0"
          title={mode === "list" ? "Switch to map" : "Switch to list"}
        >
          {mode === "list" ? "🗺️" : "📋"}
        </button>

        {/* Account button */}
        <a
          href="/login"
          className="ml-auto border rounded-full w-8 h-8 flex items-center justify-center bg-gray-100 flex-shrink-0"
          title="Account"
        >
          👤
        </a>
      </div>
    </header>
  );
}
