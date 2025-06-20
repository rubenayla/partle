// frontend/src/components/SearchBar.jsx
import { useState, useRef, useEffect } from 'react'
import { Search, User, Info } from 'lucide-react'

export default function SearchBar({
  onSearch = () => {},
  isLoggedIn = false,
  onAccountClick = () => {},
}) {
  const [query, setQuery] = useState('')
  const [priceMin, setPriceMin] = useState(0)
  const [priceMax, setPriceMax] = useState(500)
  const [sortBy, setSortBy] = useState('relevance')

  const [priceOpen, setPriceOpen] = useState(false)
  const [sortOpen, setSortOpen] = useState(false)
  const [accountOpen, setAccountOpen] = useState(false)
  const [infoOpen, setInfoOpen] = useState(false)

  const [theme, setTheme] = useState(
    () => localStorage.getItem('theme') || 'auto'
  )

  useEffect(() => {
    const root = document.documentElement
    if (theme === 'dark') root.classList.add('dark')
    else root.classList.remove('dark')
    localStorage.setItem('theme', theme)
  }, [theme])

  const priceRef = useRef()
  const sortRef = useRef()
  const accountRef = useRef()
  const infoRef = useRef()

  useEffect(() => {
    const closeAll = (e) => {
      if (!priceRef.current?.contains(e.target)) setPriceOpen(false)
      if (!sortRef.current?.contains(e.target)) setSortOpen(false)
      if (!accountRef.current?.contains(e.target)) setAccountOpen(false)
      if (!infoRef.current?.contains(e.target)) setInfoOpen(false)
    }
    document.addEventListener('mousedown', closeAll)
    return () => document.removeEventListener('mousedown', closeAll)
  }, [])

  const handleSearch = (e) => {
    e.preventDefault()
    onSearch({ query, priceMin, priceMax, sortBy })
  }

  return (
    <header className="fixed top-0 left-0 right-0 z-20 bg-background border-b border-gray-200 dark:border-gray-700">
      <div className="w-full max-w-screen-2xl mx-auto flex items-center justify-between px-4 py-3">

        {/* Logo */}
        <a href="/" className="text-2xl font-semibold text-primary">
          Partle
        </a>

        {/* Search */}
        <form
          onSubmit={handleSearch}
          className="flex flex-1 mx-6 bg-surface rounded-full pl-4 pr-2 h-12 items-center"
        >
          <input
            type="search"
            placeholder="What are you looking for?"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-1 h-full bg-transparent placeholder-text-secondary text-primary focus:outline-none"
          />

          {/* Price Filter */}
          <div className="h-6 border-l border-gray-300 dark:border-gray-600 mx-3" />
          <div ref={priceRef} className="relative">
            <button
              type="button"
              onClick={() => setPriceOpen(!priceOpen)}
              className="h-full px-3 text-sm text-primary bg-transparent focus:outline-none"
            >
              Price: {priceMin}–{priceMax}
            </button>
            {priceOpen && (
              <div className="absolute top-14 left-0 w-64 bg-surface rounded-xl shadow-lg p-4 z-50 space-y-2">
                <label className="text-sm text-secondary">Min €</label>
                <input
                  type="number"
                  min={0}
                  value={priceMin}
                  onChange={(e) => setPriceMin(Number(e.target.value))}
                  className="w-full border px-2 py-1 rounded bg-background text-primary"
                />
                <label className="text-sm text-secondary">Max €</label>
                <input
                  type="number"
                  min={0}
                  value={priceMax}
                  onChange={(e) => setPriceMax(Number(e.target.value))}
                  className="w-full border px-2 py-1 rounded bg-background text-primary"
                />
              </div>
            )}
          </div>

          {/* Sort Filter */}
          <div className="h-6 border-l border-gray-300 dark:border-gray-600 mx-3" />
          <div ref={sortRef} className="relative">
            <button
              type="button"
              onClick={() => setSortOpen(!sortOpen)}
              className="h-full px-3 text-sm text-primary bg-transparent focus:outline-none"
            >
              Sort: {sortBy.replace('_', ' ')}
            </button>
            {sortOpen && (
              <div className="absolute top-14 left-0 w-44 bg-surface rounded-xl shadow-lg p-2 z-50">
                {['relevance', 'price_asc', 'price_desc', 'distance'].map(
                  (opt) => (
                    <button
                      key={opt}
                      onClick={() => {
                        setSortBy(opt)
                        setSortOpen(false)
                      }}
                      className={`block w-full text-left px-2 py-1 rounded hover:bg-background ${
                        sortBy === opt
                          ? 'font-semibold text-primary'
                          : 'text-primary'
                      }`}
                    >
                      {opt.replace('_', ' ').replace('asc', '↑').replace('desc', '↓')}
                    </button>
                  ),
                )}
              </div>
            )}
          </div>

          {/* Search Submit */}
          <div className="h-6 border-l border-gray-300 dark:border-gray-600 mx-3" />
          <button
            type="submit"
            className="p-2 rounded-full bg-transparent text-primary hover:text-white hover:bg-primary focus:outline-none"
          >
            <Search className="h-5 w-5" />
          </button>
        </form>

        {/* Right Section */}
        <div className="flex items-center gap-4">
          {/* Account */}
          <div ref={accountRef} className="relative">
            <button
              type="button"
              onClick={() =>
                isLoggedIn ? setAccountOpen(!accountOpen) : onAccountClick()
              }
              className="bg-transparent text-primary hover:text-primary focus:outline-none"
            >
              <User className="h-8 w-8" />
            </button>

            {isLoggedIn && accountOpen && (
              <div className="absolute right-0 mt-2 w-56 bg-surface rounded-xl shadow-lg p-4 z-50">
                <a href="/account" className="block px-2 py-1 text-primary hover:bg-background rounded">Account</a>

                {/* Theme */}
                <div className="mt-2 px-2 py-1">
                  <div className="text-sm font-semibold text-secondary mb-1">Theme</div>
                  {['auto', 'light', 'dark'].map((mode) => (
                    <button
                      key={mode}
                      onClick={() => setTheme(mode)}
                      className={`block w-full bg-transparent text-left px-2 py-1 rounded ${
                        theme === mode
                          ? 'font-semibold text-primary'
                          : 'text-primary hover:bg-background'
                      }`}
                    >
                      {mode.charAt(0).toUpperCase() + mode.slice(1)}
                    </button>
                  ))}
                </div>

                <div className="border-t border-gray-200 dark:border-gray-600 my-2" />

                <a href="/stores/favourites" className="block px-2 py-1 text-primary hover:bg-background rounded">Favourite Stores</a>
                <a href="/products/favourites" className="block px-2 py-1 text-primary hover:bg-background rounded">Favourite Products</a>

                <div className="border-t border-gray-200 dark:border-gray-600 my-2" />

                <button
                  className="block w-full bg-transparent text-left px-2 py-1 text-danger hover:bg-background rounded"
                  onClick={() => {
                    localStorage.removeItem('token')
                    window.location.reload()
                  }}
                >
                  Log out
                </button>

                <div className="border-t border-gray-200 dark:border-gray-600 my-2" />

                <a href="/premium" className="block px-2 py-1 text-primary hover:bg-background rounded">Premium</a>
              </div>
            )}
          </div>

          {/* Info */}
          <div ref={infoRef} className="relative">
            <button
              type="button"
              onClick={() => setInfoOpen(!infoOpen)}
              className="bg-transparent text-primary hover:text-primary focus:outline-none"
            >
              <Info className="h-6 w-6" />
            </button>
            {infoOpen && (
              <div className="absolute right-0 mt-2 w-48 bg-surface rounded-xl shadow-lg p-4 z-50">
                <a href="/contact" className="block px-2 py-1 text-primary hover:bg-background rounded">Contact</a>
                <a href="/terms" className="block px-2 py-1 text-primary hover:bg-background rounded">Terms</a>
                <a href="/privacy" className="block px-2 py-1 text-primary hover:bg-background rounded">Privacy</a>
                <a href="/social" className="block px-2 py-1 text-primary hover:bg-background rounded">Social Networks</a>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  )
}
