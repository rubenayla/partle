// frontend/src/components/SearchBar.jsx
import { useState, useRef, useEffect } from 'react';

export default function SearchBar({ onSearch = () => {} }) {
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
      if (priceRef.current && !priceRef.current.contains(e.target)) setPriceOpen(false);
      if (sortRef.current && !sortRef.current.contains(e.target)) setSortOpen(false);
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    onSearch({ query, priceMin, priceMax, sortBy });
  };

  return (
    <header className="sticky top-0 left-0 right-0 w-screen bg-white border-b border-gray-200 z-20">
      <div className="flex items-center justify-between w-full px-4 py-3">
        <a href="/" className="text-2xl font-semibold text-indigo-600">
          Partle
        </a>

        <form
          onSubmit={handleSearch}
          className="flex flex-1 mx-6 bg-gray-100 rounded-full px-4 h-12 items-center"
        >
          {/* search input */}
          <input
            type="search"
            placeholder="What are you looking for?"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-1 h-full bg-transparent placeholder-gray-500 text-gray-800 focus:outline-none"
          />

          {/* separators and minimal buttons */}
          <div className="h-6 border-l border-gray-300 mx-4" />
          <div ref={priceRef} className="relative">
            <button
              type="button"
              onClick={() => setPriceOpen(!priceOpen)}
              className="h-full px-4 text-sm text-gray-800 bg-transparent focus:outline-none"
            >
              Price: {priceMin}–{priceMax}
            </button>
            {priceOpen && (
              <div className="absolute top-14 left-0 w-64 bg-white rounded-xl shadow-lg p-4 z-50">
                {/* Min/Max inputs */}
              </div>
            )}
          </div>

          <div className="h-6 border-l border-gray-300 mx-4" />
          <div ref={sortRef} className="relative">
            <button
              type="button"
              onClick={() => setSortOpen(!sortOpen)}
              className="h-full px-4 text-sm text-gray-800 bg-transparent focus:outline-none"
            >
              Sort: {sortBy.replace('_', ' ')}
            </button>
            {sortOpen && (
              <div className="absolute top-14 left-0 w-56 bg-white rounded-xl shadow-lg p-4 z-50">
                {/* Sort options */}
              </div>
            )}
          </div>

          <div className="h-6 border-l border-gray-300 mx-4" />
          <button
            type="submit"
            className="h-full px-4 text-indigo-600 bg-transparent focus:outline-none flex items-center justify-center"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="currentColor" viewBox="0 0 20 20">
              <path d="M12.9 14.32a8 8 0 111.414-1.414l4.387 4.386a1 1 0 01-1.414 1.415l-4.387-4.386zM8 14a6 6 0 100-12 6 6 0 000 12z" />
            </svg>
          </button>
        </form>

        <a href="/login" className="text-gray-800 hover:text-gray-600 flex-shrink-0">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M10 2a4 4 0 100 8 4 4 0 000-8zM2 18a8 8 0 1116 0H2z" clipRule="evenodd" />
          </svg>
        </a>
      </div>
    </header>
  );
}
