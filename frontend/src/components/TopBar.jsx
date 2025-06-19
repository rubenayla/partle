// frontend/src/components/TopBar.jsx
import { useState, useRef, useEffect } from 'react';

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
  const [priceOpen, setPriceOpen] = useState(false);
  const [sortOpen, setSortOpen] = useState(false);

  const priceRef = useRef();
  const sortRef = useRef();

  useEffect(() => {
    const handler = (e) => {
      if (priceRef.current && !priceRef.current.contains(e.target)) {
        setPriceOpen(false);
      }
      if (sortRef.current && !sortRef.current.contains(e.target)) {
        setSortOpen(false);
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

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
          className="flex flex-1 mx-6 bg-gray-100 rounded-full shadow px-4 py-2 items-center space-x-4 relative"
        >
          {/* Search input */}
          <input
            type="search"
            placeholder="What are you looking for?"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="bg-transparent flex-1 placeholder-gray-700 text-gray-800 focus:outline-none"
          />

          {/* Price selector pill */}
          <div className="relative" ref={priceRef}>
            <button
              type="button"
              onClick={() => setPriceOpen(!priceOpen)}
              className="px-3 py-1 text-sm text-gray-800 bg-white rounded-full shadow border border-gray-300 hover:bg-gray-50"
            >
              Price: {priceMin} – {priceMax}
            </button>
            {priceOpen && (
              <div className="absolute top-12 left-0 w-64 bg-white rounded-xl shadow-xl p-4 z-50">
                <label className="block text-sm mb-1">Min price</label>
                <input
                  type="number"
                  value={priceMin}
                  onChange={(e) => setPriceMin(Number(e.target.value))}
                  className="w-full border px-2 py-1 rounded mb-3"
                />
                <label className="block text-sm mb-1">Max price</label>
                <input
                  type="number"
                  value={priceMax}
                  onChange={(e) => setPriceMax(Number(e.target.value))}
                  className="w-full border px-2 py-1 rounded"
                />
              </div>
            )}
          </div>

          {/* Sort selector pill */}
          <div className="relative" ref={sortRef}>
            <button
              type="button"
              onClick={() => setSortOpen(!sortOpen)}
              className="px-3 py-1 text-sm text-gray-800 bg-white rounded-full shadow border border-gray-300 hover:bg-gray-50"
            >
              Sort by: {sortBy.replace('_', ' ')}
            </button>
            {sortOpen && (
              <div className="absolute top-12 left-0 w-56 bg-white rounded-xl shadow-xl p-4 z-50 space-y-2">
                {['relevance', 'price_asc', 'price_desc', 'distance'].map((option) => (
                  <button
                    key={option}
                    onClick={() => {
                      setSortBy(option);
                      setSortOpen(false);
                    }}
                    className={`block w-full text-left px-2 py-1 rounded hover:bg-gray-100 text-sm ${sortBy === option ? 'font-semibold text-blue-600' : 'text-gray-800'}`}
                  >
                    {option.replace('_', ' ')}
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Search button with inline modern SVG */}
          <button
            type="submit"
            className="bg-blue-600 hover:bg-blue-700 text-white rounded-full p-2 flex items-center justify-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path d="M12.9 14.32a8 8 0 111.414-1.414l4.387 4.386a1 1 0 01-1.414 1.415l-4.387-4.386zM8 14a6 6 0 100-12 6 6 0 000 12z" />
            </svg>
          </button>
        </form>

        {/* Account icon with inline SVG */}
        <a href="/login" title="My Account" className="text-gray-600 hover:text-gray-800 flex-shrink-0">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-gray-800" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 2a4 4 0 100 8 4 4 0 000-8zM2 18a8 8 0 1116 0H2z" clipRule="evenodd" />
          </svg>
        </a>
      </div>
    </header>
  );
}
