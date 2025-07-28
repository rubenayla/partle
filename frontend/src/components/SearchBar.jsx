// frontend/src/components/SearchBar.jsx
import React, { useState, useRef, useEffect } from 'react'
import { Search, User, Info, Plus } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { deleteAccount } from '../api/auth'
import Tooltip from './Tooltip'
import TagFilter from './TagFilter'

export default function SearchBar({
  onSearch = () => { },
  isLoggedIn = false,
  onAccountClick = () => { },
}) {
  const [query, setQuery] = useState('')
  const [searchType, setSearchType] = useState('products')
  const [priceMin, setPriceMin] = useState(0)
  const [priceMax, setPriceMax] = useState(500)
  const [selectedTags, setSelectedTags] = useState([])
  const [sortBy, setSortBy] = useState('relevance')
  const [theme, setTheme] = useState(() => localStorage.getItem('theme') || 'auto')
  const [shortcutMode, setShortcutMode] = useState(false)
  const shortcutTimeoutRef = useRef(null)

  const sortOptions = {
    relevance: 'Relevance',
    created_at: 'Newest',
    created_at_asc: 'Oldest',
    price_asc: 'Price ↑',
    price_desc: 'Price ↓',
    distance: 'Distance',
    random: 'Random',
  };

  const [priceOpen, setPriceOpen] = useState(false)
  const [sortOpen, setSortOpen] = useState(false)
  const [accountOpen, setAccountOpen] = useState(false)
  const [infoOpen, setInfoOpen] = useState(false)
  const [createOpen, setCreateOpen] = useState(false)
  const [filterOpen, setFilterOpen] = useState(false)
  const [sortPosition, setSortPosition] = useState({ top: 0, left: 0 })

  const priceRef = useRef()
  const sortRef = useRef()
  const accountRef = useRef()
  const infoRef = useRef()
  const filterRef = useRef()

  const navigate = useNavigate()
  const createRef = useRef()

  useEffect(() => {
    const root = document.documentElement

    const applyTheme = (mode) => {
      if (mode === 'dark') root.classList.add('dark')
      else root.classList.remove('dark')
    }

    let media
    if (theme === 'auto') {
      media = window.matchMedia('(prefers-color-scheme: dark)')
      applyTheme(media.matches ? 'dark' : 'light')
      const handler = (e) => applyTheme(e.matches ? 'dark' : 'light')
      media.addEventListener('change', handler)
      return () => media.removeEventListener('change', handler)
    } else {
      applyTheme(theme)
    }

    localStorage.setItem('theme', theme)
  }, [theme])

  useEffect(() => {
    const closeAll = (e) => {
      if (!priceRef.current?.contains(e.target)) setPriceOpen(false)
      if (!sortRef.current?.contains(e.target)) setSortOpen(false)
      if (!accountRef.current?.contains(e.target)) setAccountOpen(false)
      if (!infoRef.current?.contains(e.target)) setInfoOpen(false)
      if (!createRef.current?.contains(e.target)) setCreateOpen(false)
      if (!filterRef.current?.contains(e.target)) setFilterOpen(false)
    }
    document.addEventListener('mousedown', closeAll)
    return () => document.removeEventListener('mousedown', closeAll)
  }, [])

  // Chord-based keyboard shortcuts (Alt+N + second key)
  useEffect(() => {
    const handleKeyDown = (e) => {
      const isInInput = e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA'
      
      // First chord: Alt+N (works even in inputs)
      if (e.altKey && e.key.toLowerCase() === 'n') {
        e.preventDefault()
        setShortcutMode(true)
        
        // Clear any existing timeout
        if (shortcutTimeoutRef.current) {
          clearTimeout(shortcutTimeoutRef.current)
        }
        
        // Reset shortcut mode after 1 second
        shortcutTimeoutRef.current = setTimeout(() => {
          setShortcutMode(false)
        }, 1000)
        
        return
      }

      // Second chord: Execute shortcuts when in shortcut mode
      if (shortcutMode) {
        e.preventDefault() // Always prevent default when in shortcut mode
        
        switch (e.key.toLowerCase()) {
          case 'p':
            // Navigate to add product
            navigate('/products/new')
            break
          case 's':
            // Navigate to add store
            navigate('/stores/new')
            break
          case 'h':
            // Navigate to home
            navigate('/')
            break
          case 'a':
            // Toggle account menu
            if (isLoggedIn) {
              setAccountOpen(!accountOpen)
            }
            break
          case 'escape':
            // Cancel shortcut mode
            break
        }
        
        // Clear timeout and exit shortcut mode
        if (shortcutTimeoutRef.current) {
          clearTimeout(shortcutTimeoutRef.current)
        }
        setShortcutMode(false)
      }
    }

    document.addEventListener('keydown', handleKeyDown)
    return () => {
      document.removeEventListener('keydown', handleKeyDown)
      if (shortcutTimeoutRef.current) {
        clearTimeout(shortcutTimeoutRef.current)
      }
    }
  }, [shortcutMode, isLoggedIn, accountOpen, navigate])

  

  const handleSearch = (event) => {
    event.preventDefault()
    onSearch({ query, searchType, priceMin, priceMax, sortBy, selectedTags })
  }

  return (
    <header className="fixed top-0 left-0 right-0 z-20 bg-background border-b border-gray-200 dark:border-gray-700">
      <div className="w-full max-w-screen-2xl mx-auto flex items-center justify-between px-2 sm:px-4 py-3 overflow-x-hidden">
        <Tooltip text="Go home (Alt+N, H)">
          <a
            href="/"
            className="text-2xl font-semibold text-foreground"
          >
            Partle
          </a>
        </Tooltip>
        <form
          onSubmit={handleSearch}
          className="flex flex-1 mx-1 sm:mx-2 md:mx-4 lg:mx-6 bg-surface rounded-full pl-2 sm:pl-3 md:pl-4 pr-1 sm:pr-2 h-10 sm:h-12 items-center overflow-hidden"
        >
          <input
            type="search"
            placeholder={searchType === 'products' ? 'What products are you looking for?' : 'What stores are you looking for?'}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-1 h-full bg-transparent placeholder-text-secondary text-foreground focus:outline-none"
            autoFocus
          />

          <div className="hidden sm:flex items-center ml-2">
            <button
              type="button"
              onClick={() => setSearchType('products')}
              className={`px-2 sm:px-3 py-1 rounded-full text-xs sm:text-sm font-medium ${searchType === 'products' ? 'bg-primary text-white' : 'bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-200'}`}
            >
              Products
            </button>
            <button
              type="button"
              onClick={() => setSearchType('stores')}
              className={`ml-1 sm:ml-2 px-2 sm:px-3 py-1 rounded-full text-xs sm:text-sm font-medium ${searchType === 'stores' ? 'bg-primary text-white' : 'bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-200'}`}
            >
              Stores
            </button>
          </div>

          <div className="hidden sm:block h-6 border-l border-gray-300 dark:border-gray-600 mx-1 sm:mx-2 md:mx-3" />
          <div ref={sortRef} className="relative hidden md:block overflow-visible">
            <button
              type="button"
              onClick={() => {
                if (sortRef.current) {
                  const rect = sortRef.current.getBoundingClientRect();
                  setSortPosition({ 
                    top: rect.bottom + 8, 
                    left: rect.right - 160 // 160px = w-40 width
                  });
                }
                setSortOpen(!sortOpen);
              }}
              className="h-full px-1 sm:px-2 md:px-3 text-xs sm:text-sm text-foreground bg-transparent focus:outline-none whitespace-nowrap"
            >
              <span className="hidden lg:inline">Sort: </span>{sortOptions[sortBy]}
            </button>
          </div>

          <div className="hidden sm:block h-6 border-l border-gray-300 dark:border-gray-600 mx-1 sm:mx-2 md:mx-3" />
          {/* New Filter Section */}
          <div className="relative hidden lg:block overflow-visible">
            <button
              type="button"
              onClick={() => setFilterOpen(!filterOpen)}
              className="h-full px-1 sm:px-2 md:px-3 text-xs sm:text-sm text-foreground bg-transparent focus:outline-none"
            >
              Filters
            </button>
            {filterOpen && (
              <div ref={filterRef} className="absolute top-full mt-2 right-0 w-64 bg-surface rounded-xl shadow-lg p-4 z-50 space-y-2 max-w-screen">
                <TagFilter
                  selectedTags={selectedTags}
                  onTagChange={setSelectedTags}
                />
              </div>
            )}
          </div>

          <div className="hidden sm:block h-6 border-l border-gray-300 dark:border-gray-600 mx-1 sm:mx-2 md:mx-3" />
          <div ref={priceRef} className="relative hidden md:block overflow-visible">
            <button
              type="button"
              onClick={() => setPriceOpen(!priceOpen)}
              className="h-full px-1 sm:px-2 md:px-3 text-xs sm:text-sm text-foreground bg-transparent focus:outline-none whitespace-nowrap"
            >
              <span className="hidden lg:inline">Price: </span>{priceMin}–{priceMax}
            </button>
            {priceOpen && (
              <div className="absolute top-full mt-2 right-0 w-64 bg-surface rounded-xl shadow-lg p-4 z-50 space-y-2 max-w-screen">
                <label className="text-sm text-secondary">Min €</label>
                <input
                  type="number"
                  min={0}
                  value={priceMin}
                  onChange={(e) => setPriceMin(Number(e.target.value))}
                  className="w-full border px-2 py-1 rounded bg-background text-foreground"
                />
                <label className="text-sm text-secondary">Max €</label>
                <input
                  type="number"
                  min={0}
                  value={priceMax}
                  onChange={(e) => setPriceMax(Number(e.target.value))}
                  className="w-full border px-2 py-1 rounded bg-background text-foreground"
                />
              </div>
            )}
          </div>

          

          <div className="hidden sm:block h-6 border-l border-gray-300 dark:border-gray-600 mx-1 sm:mx-2 md:mx-3" />
          <button
            type="submit"
            className="p-2 rounded-full bg-transparent text-foreground hover:text-white hover:bg-primary focus:outline-none"
          >
            <Search className="h-5 w-5" />
          </button>
        </form>

        <div className="flex items-center gap-1 sm:gap-2 md:gap-3">
          {isLoggedIn && (
            <div ref={createRef} className="relative">
              <button
                type="button"
                onClick={() => setCreateOpen(!createOpen)}
                className="bg-transparent text-foreground hover:text-foreground focus:outline-none p-1 sm:p-2"
              >
                <Plus className="h-5 w-5 sm:h-6 sm:w-6" />
              </button>

              {createOpen && (
                <div className="absolute right-0 mt-2 w-48 bg-surface rounded-xl shadow-lg p-4 z-50">
                  <Tooltip text="Add product (Alt+N, P)">
                    <a
                      href="/products/new"
                      className="block px-2 py-1 text-foreground hover:bg-background rounded"
                    >Add product</a>
                  </Tooltip>
                  <Tooltip text="Add store (Alt+N, S)">
                    <a href="/stores/new" className="block px-2 py-1 text-foreground hover:bg-background rounded">Add store</a>
                  </Tooltip>
                </div>
              )}
            </div>
          )}

          <div ref={accountRef} className="relative">
            <button
              type="button"
              onClick={() =>
                isLoggedIn ? setAccountOpen(!accountOpen) : onAccountClick()
              }
              className="bg-transparent text-foreground hover:text-foreground focus:outline-none p-1 sm:p-2"
            >
              <User className="h-6 w-6 sm:h-7 sm:w-7" />
            </button>

            {isLoggedIn && accountOpen && (
              <div className="absolute right-0 mt-2 w-56 bg-surface rounded-xl shadow-lg p-4 z-50">
                <a href="/products/favourites" className="block px-2 py-1 text-foreground hover:bg-background rounded">Favourite Products</a>
                <a href="/stores/favourites" className="block px-2 py-1 text-foreground hover:bg-background rounded">Favourite Stores</a>
                <a href="/account" className="block px-2 py-1 text-foreground hover:bg-background rounded">Account</a>

                <div className="mt-2 px-2 py-1">
                  <div className="text-sm font-semibold text-secondary mb-2">Theme</div>
                  <ThemeSwitch value={theme} onChange={(mode) => setTheme(mode)} />
                </div>

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
                <button
                  className="mt-1 block w-full bg-transparent text-left px-2 py-1 text-danger hover:bg-background rounded"
                  onClick={async () => {
                    if (confirm('Delete account?')) {
                      try {
                        await deleteAccount()
                        localStorage.removeItem('token')
                        window.location.reload()
                      } catch (e) {
                        alert('Could not delete account')
                      }
                    }
                  }}
                >
                  Delete account
                </button>

                <div className="border-t border-gray-200 dark:border-gray-600 my-2" />
                <a href="/premium" className="block px-2 py-1 text-foreground hover:bg-background rounded">Premium</a>
              </div>
            )}
          </div>

          <div ref={infoRef} className="relative">
            <button
              type="button"
              onClick={() => setInfoOpen(!infoOpen)}
              className="bg-transparent text-foreground hover:text-foreground focus:outline-none p-1 sm:p-2"
            >
              <Info className="h-5 w-5 sm:h-6 sm:w-6" />
            </button>
            {infoOpen && (
              <div className="absolute right-0 mt-2 w-48 bg-surface rounded-xl shadow-lg p-4 z-50">
                <a href="/contact" className="block px-2 py-1 text-foreground hover:bg-background rounded">Contact</a>
                <a href="/terms" className="block px-2 py-1 text-foreground hover:bg-background rounded">Terms</a>
                <a href="/privacy" className="block px-2 py-1 text-foreground hover:bg-background rounded">Privacy</a>
                
              </div>
            )}
          </div>
        </div>
      </div>
      
      {/* Dropdowns positioned outside form to avoid scroll issues */}
      {sortOpen && (
        <div 
          className="fixed w-40 bg-surface rounded-xl shadow-lg p-2 z-[100] max-w-screen border border-gray-200 dark:border-gray-600"
          style={{ top: `${sortPosition.top}px`, left: `${sortPosition.left}px` }}
        >
          {Object.entries(sortOptions).map(([value, label]) => (
            <button
              key={value}
              onClick={() => {
                setSortBy(value);
                setSortOpen(false);
                onSearch({ query, searchType, priceMin, priceMax, sortBy: value, selectedTags });
              }}
              className={`block w-full text-left px-2 py-1 rounded hover:bg-background ${sortBy === value
                  ? 'font-semibold text-foreground'
                  : 'text-foreground'
                }`}
            >
              {label}
            </button>
          ))}
        </div>
      )}
    </header>
  )
}

// ─── ThemeSwitch ──────────────────────────────────────────
function ThemeSwitch({ value, onChange }) {
  const options = ["light", "auto", "dark"];
  const index = options.indexOf(value);

  const WIDTH = 180; // px
  const SEGMENT = WIDTH / 3;

  return (
    <div style={{ width: `${WIDTH}px` }} className="h-9">
      <div className="relative flex h-full rounded-full bg-surface shadow-inner border border-gray-300 dark:border-gray-600 overflow-hidden">
        {/* Knob */}
        <div
          className="absolute inset-y-0 left-0 rounded-full transition-transform duration-200 z-0 pointer-events-none bg-primary"
          style={{
            width: `${SEGMENT}px`,
            transform: `translateX(${index * SEGMENT}px)`
          }}
        />
        {/* Labels */}
        {options.map((mode, i) => (
          <button
            key={mode}
            onClick={() => onChange(mode)}
            style={{ width: `${SEGMENT}px` }}
            className={`relative z-10 h-full flex items-center justify-center text-sm font-medium transition-colors
              ${index === i ? "text-white dark:text-white" : "text-foreground"}
              focus:outline-none border-none`}
          >
            {mode.charAt(0).toUpperCase() + mode.slice(1)}
          </button>
        ))}
      </div>
    </div>
  );
}