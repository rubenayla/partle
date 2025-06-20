// frontend/src/components/SearchBar.jsx
import { useState, useRef, useEffect } from 'react';
import { Search, User, Info } from 'lucide-react';

export default function SearchBar({ onSearch = () => {}, isLoggedIn = false }) {
  const [query, setQuery] = useState('');
  const [priceMin, setPriceMin] = useState(0);
  const [priceMax, setPriceMax] = useState(500);
  const [sortBy, setSortBy] = useState('relevance');
  const [priceOpen, setPriceOpen] = useState(false);
  const [sortOpen, setSortOpen] = useState(false);
  const [accountOpen, setAccountOpen] = useState(false);
  const [infoOpen, setInfoOpen] = useState(false);

  const priceRef = useRef();
  const sortRef = useRef();
  const accountRef = useRef();
  const infoRef = useRef();

  useEffect(() => {
    const closeAll = (e) => {
      if (priceRef.current && !priceRef.current.contains(e.target)) setPriceOpen(false);
      if (sortRef.current && !sortRef.current.contains(e.target)) setSortOpen(false);
      if (accountRef.current && !accountRef.current.contains(e.target)) setAccountOpen(false);
      if (infoRef.current && !infoRef.current.contains(e.target)) setInfoOpen(false);
    };
    document.addEventListener('mousedown', closeAll);
    return () => document.removeEventListener('mousedown', closeAll);
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    onSearch({ query, priceMin, priceMax, sortBy });
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-20 bg-white border-b border-gray-200">
      <div className="w-full max-w-screen-2xl mx-auto flex items-center justify-between px-4 py-3">
        <a href="/" className="text-2xl font-semibold text-indigo-600">Partle</a>

        <form
          onSubmit={handleSearch}
          className="flex flex-1 mx-6 bg-gray-100 rounded-full pl-4 pr-2 h-12 items-center"
        >
          <input
            type="search"
            placeholder="What are you looking for?"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-1 h-full bg-transparent placeholder-gray-500 text-gray-800 focus:outline-none"
          />

          <div className="h-6 border-l border-gray-300 mx-3" />
          <div ref={priceRef} className="relative">
            <button
              type="button"
              onClick={() => setPriceOpen(!priceOpen)}
              className="h-full px-3 text-sm text-gray-800 bg-transparent focus:outline-none"
            >
              Price: {priceMin}–{priceMax}
            </button>
            {priceOpen && (
              <div className="absolute top-14 left-0 w-64 bg-white rounded-xl shadow-lg p-4 z-50 space-y-2">
                <label className="text-sm">Min €</label>
                <input
                  type="number"
                  min={0}
                  value={priceMin}
                  onChange={(e) => setPriceMin(Number(e.target.value))}
                  className="w-full border px-2 py-1 rounded"
                />
                <label className="text-sm">Max €</label>
                <input
                  type="number"
                  min={0}
                  value={priceMax}
                  onChange={(e) => setPriceMax(Number(e.target.value))}
                  className="w-full border px-2 py-1 rounded"
                />
              </div>
            )}
          </div>

          <div className="h-6 border-l border-gray-300 mx-3" />
          <div ref={sortRef} className="relative">
            <button
              type="button"
              onClick={() => setSortOpen(!sortOpen)}
              className="h-full px-3 text-sm text-gray-800 bg-transparent focus:outline-none"
            >
              Sort: {sortBy.replace('_', ' ')}
            </button>
            {sortOpen && (
              <div className="absolute top-14 left-0 w-44 bg-white rounded-xl shadow-lg p-2 z-50">
                {['relevance', 'price_asc', 'price_desc', 'distance'].map((opt) => (
                  <button
                    key={opt}
                    onClick={() => { setSortBy(opt); setSortOpen(false); }}
                    className={`block w-full text-left px-2 py-1 rounded hover:bg-gray-100 ${sortBy===opt ? 'font-semibold text-indigo-600' : ''}`}
                  >
                    {opt.replace('_',' ').replace('asc','↑').replace('desc','↓')}
                  </button>
                ))}
              </div>
            )}
          </div>

          <div className="h-6 border-l border-gray-300 mx-3" />
          <button
            type="submit"
            className="p-2 rounded-full bg-transparent text-indigo-600 hover:text-indigo-800 focus:outline-none flex items-center justify-center"
          >
            <Search className="h-5 w-5" />
          </button>
        </form>

        <div className="flex items-center gap-4">
          <div ref={accountRef} className="relative">
            <button
              type="button"
              onClick={() => setAccountOpen(!accountOpen)}
              className="bg-transparent text-gray-600 hover:text-gray-800 focus:outline-none"
            >
              <User className="h-8 w-8" />
            </button>
            {accountOpen && (
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg p-4 z-50">
                <a href="/account" className="block px-2 py-1 hover:bg-gray-100 rounded">Account</a>
                {isLoggedIn && (
                  <>
                    <a href="/account/theme" className="block px-2 py-1 hover:bg-gray-100 rounded">Theme</a>
                    <a href="/favorites/stores" className="block px-2 py-1 hover:bg-gray-100 rounded">Favorite Stores</a>
                    <a href="/favorites/products" className="block px-2 py-1 hover:bg-gray-100 rounded">Favorite Products</a>
                    <div className="border-t border-gray-200 my-2" />
                    <button className="w-full text-left px-2 py-1 hover:bg-gray-100 rounded">Log out</button>
                  </>
                )}
                <div className="border-t border-gray-200 my-2" />
                <a href="/premium" className="block px-2 py-1 hover:bg-gray-100 rounded">Premium</a>
              </div>
            )}
          </div>

          <div ref={infoRef} className="relative">
            <button
              type="button"
              onClick={() => setInfoOpen(!infoOpen)}
              className="bg-transparent text-gray-600 hover:text-gray-800 focus:outline-none"
            >
              <Info className="h-6 w-6" />
            </button>
            {infoOpen && (
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-xl shadow-lg p-4 z-50">
                <a href="/contact" className="block px-2 py-1 hover:bg-gray-100 rounded">Contact</a>
                <a href="/terms" className="block px-2 py-1 hover:bg-gray-100 rounded">Terms</a>
                <a href="/privacy" className="block px-2 py-1 hover:bg-gray-100 rounded">Privacy</a>
                <a href="/social" className="block px-2 py-1 hover:bg-gray-100 rounded">Social Networks</a>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
