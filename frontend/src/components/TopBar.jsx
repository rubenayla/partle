// frontend/src/components/TopBar.jsx
import { useState } from 'react';
import { Search } from 'lucide-react';
import { User } from 'lucide-react';

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
            className="bg-transparent flex-1 placeholder-gray-700 text-gray-800 focus:outline-none"
          />

          {/* Separator */}
          <div className="h-6 border-l border-gray-300" />

          {/* Price range */}
          <div className="flex items-center space-x-1">
            <input
              type="number"
              min={0}
              value={priceMin}
              onChange={(e) => setPriceMin(Number(e.target.value))}
              placeholder="Min"
              className="w-16 bg-transparent placeholder-gray-700 text-gray-800 focus:outline-none text-sm"
            />
            —
            <input
              type="number"
              min={0}
              value={priceMax}
              onChange={(e) => setPriceMax(Number(e.target.value))}
              placeholder="Max"
              className="w-16 bg-transparent placeholder-gray-700 text-gray-800 focus:outline-none text-sm"
            />
          </div>

          {/* Separator */}
          <div className="h-6 border-l border-gray-300" />

          {/* Sort select */}
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="bg-transparent text-gray-800 focus:outline-none text-sm"
          >
            <option value="relevance">Relevance</option>
            <option value="price_asc">Price ↑</option>
            <option value="price_desc">Price ↓</option>
            <option value="distance">Closest</option>
          </select>

          {/* Submit button with lucide-react icon */}
          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white rounded-full p-2 flex items-center justify-center"
          >
            <Search className="h-5 w-5" />
          </button>
        </form>

        {/* Account icon */}
        <a href="/login" title="My Account" className="text-gray-600 hover:text-gray-800 flex-shrink-0">
          <User className="h-8 w-8 text-gray-800" />
        </a>
      </div>
    </header>
  );
}
