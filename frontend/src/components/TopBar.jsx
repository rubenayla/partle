// frontend/src/components/TopBar.jsx
import { useState } from 'react';

export default function TopBar({
  mode = 'list',
  onModeChange = () => {},
  onSearch = () => {},
  onFiltersChange = () => {},
}) {
  const [query, setQuery] = useState('');
  const [priceMin, setPriceMin] = useState(0);
  const [priceMax, setPriceMax] = useState(500);
  const [sortBy, setSortBy] = useState('relevance');

  const handleSearch = (e) => {
    e.preventDefault();
    onSearch({ query, priceMin, priceMax, sortBy });
  };

  return (
    <header className="sticky top-0 left-0 right-0 w-screen bg-white shadow z-20">
      <div className="flex items-center justify-between w-full px-4 py-3">
        {/* Logo */}
        <a href="/" className="text-2xl font-bold text-indigo-600 flex-shrink-0">
          Partle
        </a>

        {/* Search & filters pill */}
        <form
          onSubmit={handleSearch}
          className="flex flex-1 mx-6 bg-gray-100 rounded-full shadow px-4 py-2 items-center space-x-4"
        >
          {/* Search input */}
          <input
            type="search"
            placeholder="What are you looking for?"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="bg-transparent flex-1 placeholder-gray-500 focus:outline-none"
          />

          {/* Vertical separator */}
          <div className="h-6 border-l border-gray-300" />

          {/* Price range */}
          <div className="flex items-center space-x-1">
            <input
              type="number"
              min={0}
              value={priceMin}
              onChange={(e) => setPriceMin(Number(e.target.value))}
              className="w-16 bg-transparent placeholder-gray-500 focus:outline-none text-sm"
              placeholder="Min"
            />
            —
            <input
              type="number"
              min={0}
              value={priceMax}
              onChange={(e) => setPriceMax(Number(e.target.value))}
              className="w-16 bg-transparent placeholder-gray-500 focus:outline-none text-sm"
              placeholder="Max"
            />
          </div>

          {/* Separator */}
          <div className="h-6 border-l border-gray-300" />

          {/* Sort select */}
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="bg-transparent focus:outline-none text-sm"
          >
            <option value="relevance">Relevance</option>
            <option value="price_asc">Price ↑</option>
            <option value="price_desc">Price ↓</option>
            <option value="distance">Closest</option>
          </select>

          {/* Search button */}
          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white rounded-full p-2"
          >
            🔍
          </button>
        </form>

        {/* Account icon */}
        <a href="/login" title="My Account" className="text-gray-600 hover:text-gray-800 flex-shrink-0">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5.121 17.804A13.937 13.937 0 0112 15c2.485 0 4.817.656 6.879 1.804M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
        </a>
      </div>
    </header>
  );
}
