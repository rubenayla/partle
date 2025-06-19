// frontend/src/components/TopBar.jsx
import { useState } from "react";

/**
 * Minimal, dependency‑free top bar:
 * – plain <input>, <select>, and <button> elements only
 * – no external UI kit (so no missing imports)
 */
export default function TopBar({
  mode = "list",
  onModeChange = () => {},
  onSearch = () => {},
  onFiltersChange = () => {},
}) {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState("");
  const [priceMin, setPriceMin] = useState(0);
  const [priceMax, setPriceMax] = useState(500);
  const [sortBy, setSortBy] = useState("relevance");

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    onSearch(query.trim());
  };

  const emitFilters = (extra = {}) =>
    onFiltersChange({ category, priceMin, priceMax, sortBy, ...extra });

  return (
    <header className="sticky top-0 z-20 bg-white shadow px-4 py-3 flex items-start gap-6">
      {/* Logo */}
      <a href="/" className="text-xl font-semibold whitespace-nowrap">
        Partle
      </a>

      {/* Search */}
      <form onSubmit={handleSearchSubmit} className="flex-1">
        <input
          type="search"
          placeholder="Search products…"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="w-full border rounded px-3 py-2"
        />
      </form>

      {/* Filters */}
      <div className="flex-shrink-0 flex flex-col gap-2 min-w-[220px] text-sm">
        {/* Category */}
        <select
          value={category}
          onChange={(e) => {
            setCategory(e.target.value);
            emitFilters({ category: e.target.value });
          }}
          className="border rounded px-2 py-1"
        >
          <option value="">All Categories</option>
          <option value="electronics">Electronics</option>
          <option value="furniture">Furniture</option>
          <option value="tools">Tools</option>
        </select>

        {/* Price range */}
        <label className="flex items-center gap-1">
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

        {/* Sort */}
        <select
          value={sortBy}
          onChange={(e) => {
            setSortBy(e.target.value);
            emitFilters({ sortBy: e.target.value });
          }}
          className="border rounded px-2 py-1"
        >
          <option value="relevance">Relevance</option>
          <option value="price_asc">Price: Low → High</option>
          <option value="price_desc">Price: High → Low</option>
          <option value="distance">Closest</option>
        </select>
      </div>

      {/* View toggle */}
      <div className="flex-shrink-0 flex items-center gap-2">
        <button
          onClick={() => onModeChange("list")}
          className={`border px-2 py-1 rounded ${
            mode === "list" ? "bg-gray-200" : "bg-white"
          }`}
          title="List view"
        >
          📋
        </button>
        <button
          onClick={() => onModeChange("map")}
          className={`border px-2 py-1 rounded ${
            mode === "map" ? "bg-gray-200" : "bg-white"
          }`}
          title="Map view"
        >
          🗺️
        </button>
      </div>
    </header>
  );
}
