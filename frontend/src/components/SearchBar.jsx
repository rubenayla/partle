// frontend/src/components/SearchBar.jsx
import React, { useState, useRef, useEffect } from 'react'
import { Search, User, Info, Plus } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { deleteAccount } from '../api/auth'
import Tooltip from './Tooltip'
import TagFilter from './TagFilter'
import * as DropdownMenu from '@radix-ui/react-dropdown-menu'
import api from '../api/index.ts'

export default function SearchBar({
  onSearch = () => { },
  isLoggedIn = false,
  onAccountClick = () => { },
  currentTheme, // New prop
  setTheme,     // New prop
}) {
  const [query, setQuery] = useState('')
  const [searchType, setSearchType] = useState('products')
  const [priceMin, setPriceMin] = useState(0)
  const [priceMax, setPriceMax] = useState(500)
  const [selectedTags, setSelectedTags] = useState([])
  const [sortBy, setSortBy] = useState('random')
  const [shortcutMode, setShortcutMode] = useState(false)
  const shortcutTimeoutRef = useRef(null)

  const sortOptions = {
    created_at: 'Newest',
    created_at_asc: 'Oldest',
    price_asc: 'Price ↑',
    price_desc: 'Price ↓',
    distance: 'Distance',
    random: 'Random',
    name_asc: 'Alphabetical Name',
  };


  const navigate = useNavigate()

  // Parse search operators from query
  const parseSearchOperators = (searchQuery) => {
    const operators = {};
    let cleanQuery = searchQuery;

    // Parse store:name or store:"name with spaces"
    const storeMatch = searchQuery.match(/\bstore:(['"]?)([^'"\s]+(?:\s+[^'"\s]+)*)\1/i);
    if (storeMatch) {
      operators.storeName = storeMatch[2];
      cleanQuery = cleanQuery.replace(storeMatch[0], '').trim();
    }

    // Parse tag:name or tag:"name with spaces"
    const tagMatches = searchQuery.matchAll(/\btag:(['"]?)([^'"\s]+(?:\s+[^'"\s]+)*)\1/gi);
    const extractedTags = [];
    for (const match of tagMatches) {
      extractedTags.push(match[2]);
      cleanQuery = cleanQuery.replace(match[0], '').trim();
    }
    if (extractedTags.length > 0) {
      operators.tags = extractedTags;
    }

    return {
      cleanQuery: cleanQuery.replace(/\s+/g, ' ').trim(),
      operators
    };
  };


  // Remove the local theme state and useEffect for theme management
  // useEffect(() => {
  //   const root = document.documentElement
  //   const applyTheme = (mode) => {
  //     if (mode === 'dark') root.classList.add('dark')
  //     else root.classList.remove('dark')
  //   }
  //   let media
  //   if (theme === 'auto') {
  //     media = window.matchMedia('(prefers-color-scheme: dark)')
  //     applyTheme(media.matches ? 'dark' : 'light')
  //     const handler = (e) => applyTheme(e.matches ? 'dark' : 'light')
  //     media.addEventListener('change', handler)
  //     return () => media.removeEventListener('change', handler)
  //   } else {
  //     applyTheme(theme)
  //   }
  //   localStorage.setItem('theme', theme)
  // }, [theme])


  // Chord-based keyboard shortcuts (Alt+N + second key)
  useEffect(() => {
    const handleKeyDown = (e) => {
      
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
            // Navigate to account (since dropdown is now handled by Radix)
            if (isLoggedIn) {
              navigate('/account')
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
  }, [shortcutMode, isLoggedIn, navigate])

  

  const handleSearch = (event) => {
    event.preventDefault()
    if (onSearch) {
      const { cleanQuery, operators } = parseSearchOperators(query);
      
      // Merge parsed tags with existing selectedTags
      const allTags = [...selectedTags, ...(operators.tags || [])];
      
      onSearch({ 
        query: cleanQuery, 
        searchType, 
        priceMin, 
        priceMax, 
        sortBy, 
        selectedTags: allTags,
        storeName: operators.storeName // Pass store name instead of store ID
      })
    }
  }

  return (
    <header className="fixed top-0 left-0 right-0 z-20 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700">
      <div className="w-full max-w-screen-2xl mx-auto flex items-center justify-between px-2 sm:px-4 py-3 overflow-x-hidden">
        <Tooltip text="Go home (Alt+N, H)">
          <a
            href="/"
            className="text-2xl font-semibold text-gray-900 dark:text-white"
          >
            Partle
          </a>
        </Tooltip>
        <form
          onSubmit={handleSearch}
          className="flex flex-1 mx-1 sm:mx-2 md:mx-4 lg:mx-6 bg-gray-100 dark:bg-gray-800 rounded-full pl-2 sm:pl-3 md:pl-4 pr-1 sm:pr-2 h-10 sm:h-12 items-center overflow-hidden"
        >
          <input
            type="search"
            placeholder="What are you looking for?"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-1 h-full bg-transparent placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white focus:outline-none"
            autoFocus
          />


          <div className="hidden sm:block h-6 border-l border-gray-300 dark:border-gray-600 mx-1 sm:mx-2 md:mx-3" />
          {/* Filters Section - moved before Sort */}
          <DropdownMenu.Root>
            <DropdownMenu.Trigger className="hidden sm:block h-full px-1 sm:px-2 md:px-3 text-xs sm:text-sm text-gray-700 dark:text-gray-300 bg-transparent hover:bg-gray-200 dark:hover:bg-gray-700 focus:outline-none focus:ring-0 border-0 hover:border-0">
              Filters
            </DropdownMenu.Trigger>
            <DropdownMenu.Portal>
              <DropdownMenu.Content
                className="w-64 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 z-[100] border border-gray-200 dark:border-gray-600 space-y-4"
                align="end"
                sideOffset={8}
              >
                {/* Search Type Toggle */}
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Search Type</label>
                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      onClick={() => {
                        setSearchType('products');
                        if (onSearch) {
                          onSearch({ query, searchType: 'products', priceMin, priceMax, sortBy, selectedTags });
                        }
                      }}
                      className={`px-3 py-1 rounded-full text-sm font-medium ${searchType === 'products' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-200'}`}
                    >
                      Products
                    </button>
                    <button
                      type="button"
                      onClick={() => {
                        setSearchType('stores');
                        if (onSearch) {
                          onSearch({ query, searchType: 'stores', priceMin, priceMax, sortBy, selectedTags });
                        }
                      }}
                      className={`px-3 py-1 rounded-full text-sm font-medium ${searchType === 'stores' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-200'}`}
                    >
                      Stores
                    </button>
                  </div>
                </div>
                
                
                {/* Tag Filter */}
                <TagFilter
                  selectedTags={selectedTags}
                  onTagChange={setSelectedTags}
                />

                {/* Price Range Filter */}
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Price Range</label>
                  <div className="space-y-2">
                    <div>
                      <label className="text-xs text-gray-600 dark:text-gray-400">Min €</label>
                      <input
                        type="number"
                        min={0}
                        value={priceMin}
                        onChange={(e) => {
                          setPriceMin(Number(e.target.value));
                          if (onSearch) {
                            onSearch({ query, searchType, priceMin: Number(e.target.value), priceMax, sortBy, selectedTags });
                          }
                        }}
                        className="w-full border border-gray-300 dark:border-gray-600 px-2 py-1 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                      />
                    </div>
                    <div>
                      <label className="text-xs text-gray-600 dark:text-gray-400">Max €</label>
                      <input
                        type="number"
                        min={0}
                        value={priceMax}
                        onChange={(e) => {
                          setPriceMax(Number(e.target.value));
                          if (onSearch) {
                            onSearch({ query, searchType, priceMin, priceMax: Number(e.target.value), sortBy, selectedTags });
                          }
                        }}
                        className="w-full border border-gray-300 dark:border-gray-600 px-2 py-1 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                      />
                    </div>
                  </div>
                </div>
              </DropdownMenu.Content>
            </DropdownMenu.Portal>
          </DropdownMenu.Root>

          <div className="hidden sm:block h-6 border-l border-gray-300 dark:border-gray-600 mx-1 sm:mx-2 md:mx-3" />
          <DropdownMenu.Root>
            <DropdownMenu.Trigger className="hidden md:block h-full px-1 sm:px-2 md:px-3 text-xs sm:text-sm text-gray-700 dark:text-gray-300 bg-transparent hover:bg-gray-200 dark:hover:bg-gray-700 focus:outline-none focus:ring-0 border-0 hover:border-0 whitespace-nowrap">
              <span className="hidden lg:inline">Sort: </span>{sortOptions[sortBy]}
            </DropdownMenu.Trigger>

            <DropdownMenu.Portal>
              <DropdownMenu.Content
                className="w-40 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-2 z-[100] border border-gray-200 dark:border-gray-600"
                align="end"
                sideOffset={8}
              >
                {Object.entries(sortOptions).map(([value, label]) => (
                  <DropdownMenu.Item
                    key={value}
                    className={`block w-full text-left px-2 py-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer focus:outline-none focus:bg-gray-100 dark:focus:bg-gray-700 ${
                      sortBy === value
                        ? 'font-semibold text-gray-900 dark:text-white'
                        : 'text-gray-700 dark:text-gray-300'
                    }`}
                    onSelect={() => {
                      setSortBy(value);
                      if (onSearch) {
                        onSearch({ query, searchType, priceMin, priceMax, sortBy: value, selectedTags });
                      }
                    }}
                  >
                    {label}
                  </DropdownMenu.Item>
                ))}
              </DropdownMenu.Content>
            </DropdownMenu.Portal>
          </DropdownMenu.Root>

          

          <div className="hidden sm:block h-6 border-l border-gray-300 dark:border-gray-600 mx-1 sm:mx-2 md:mx-3" />
          <button
            type="submit"
            aria-label="Search"
            className="p-2 rounded-full bg-transparent text-gray-600 dark:text-gray-400 hover:text-white hover:bg-blue-500 focus:outline-none focus:ring-0 border-0 hover:border-0"
          >
            <Search className="h-5 w-5" />
          </button>
        </form>

        <div className="flex items-center gap-1 sm:gap-2 md:gap-3">
          {isLoggedIn && (
            <DropdownMenu.Root>
              <DropdownMenu.Trigger className="bg-transparent text-gray-600 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-0 border-0 hover:border-0 p-1 sm:p-2">
                <Plus className="h-5 w-5 sm:h-6 sm:w-6" />
              </DropdownMenu.Trigger>

              <DropdownMenu.Portal>
                <DropdownMenu.Content
                  className="w-48 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 z-50 border border-gray-200 dark:border-gray-700"
                  align="end"
                  sideOffset={8}
                >
                  <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer focus:outline-none focus:bg-gray-100 dark:focus:bg-gray-700">
                    <Tooltip text="Add product (Alt+N, P)">
                      <a href="/products/new" className="block text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:font-medium">Add product</a>
                    </Tooltip>
                  </DropdownMenu.Item>
                  <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer focus:outline-none focus:bg-gray-100 dark:focus:bg-gray-700">
                    <Tooltip text="Add store (Alt+N, S)">
                      <a href="/stores/new" className="block text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:font-medium">Add store</a>
                    </Tooltip>
                  </DropdownMenu.Item>
                </DropdownMenu.Content>
              </DropdownMenu.Portal>
            </DropdownMenu.Root>
          )}

          <DropdownMenu.Root>
            <DropdownMenu.Trigger
              className="bg-transparent text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-0 border-0 hover:border-0 p-1 sm:p-2"
              onClick={!isLoggedIn ? onAccountClick : undefined}
              aria-label="User account"
            >
              <User className="h-6 w-6 sm:h-7 sm:w-7" />
            </DropdownMenu.Trigger>

            {isLoggedIn && (
              <DropdownMenu.Portal>
                <DropdownMenu.Content
                  className="w-56 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 z-50 border border-gray-200 dark:border-gray-600"
                  align="end"
                  sideOffset={8}
                >
                  <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer focus:outline-none focus:bg-gray-100 dark:focus:bg-gray-700">
                    <a href="/products/favourites" className="block text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:font-medium">Favourite Products</a>
                  </DropdownMenu.Item>
                  <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer focus:outline-none focus:bg-gray-100 dark:focus:bg-gray-700">
                    <a href="/stores/favourites" className="block text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:font-medium">Favourite Stores</a>
                  </DropdownMenu.Item>
                  <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer focus:outline-none focus:bg-gray-100 dark:focus:bg-gray-700">
                    <a href="/account" className="block text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:font-medium">Account</a>
                  </DropdownMenu.Item>

                  <div className="mt-2 px-2 py-1">
                    <div className="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-2">Theme</div>
                    <ThemeSwitch value={currentTheme} onChange={(mode) => setTheme(mode)} />
                  </div>

                  <DropdownMenu.Separator className="border-t border-gray-200 dark:border-gray-600 my-2" />
                  <DropdownMenu.Item
                    className="block w-full bg-transparent text-left px-2 py-1 text-red-600 dark:text-red-400 hover:bg-gray-100 dark:hover:bg-gray-700 hover:text-red-600 dark:text-red-400 hover:font-medium rounded cursor-pointer focus:outline-none focus:bg-gray-100 dark:focus:bg-gray-700"
                    onSelect={() => {
                      localStorage.removeItem('token')
                      window.location.reload()
                    }}
                  >
                    Log out
                  </DropdownMenu.Item>
                  <DropdownMenu.Item
                    className="mt-1 block w-full bg-transparent text-left px-2 py-1 text-red-600 dark:text-red-400 hover:bg-gray-100 dark:hover:bg-gray-700 hover:text-red-600 dark:text-red-400 hover:font-medium rounded cursor-pointer focus:outline-none focus:bg-gray-100 dark:focus:bg-gray-700"
                    onSelect={async () => {
                      if (confirm('Delete account?')) {
                        try {
                          await deleteAccount()
                          localStorage.removeItem('token')
                          window.location.reload()
                        } catch {
                          alert('Could not delete account')
                        }
                      }
                    }}
                  >
                    Delete account
                  </DropdownMenu.Item>

                  <DropdownMenu.Separator className="border-t border-gray-200 dark:border-gray-600 my-2" />
                  <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer focus:outline-none focus:bg-gray-100 dark:focus:bg-gray-700">
                    <a href="/premium" className="block text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:font-medium">Premium</a>
                  </DropdownMenu.Item>
                </DropdownMenu.Content>
              </DropdownMenu.Portal>
            )}
          </DropdownMenu.Root>

          <DropdownMenu.Root>
            <DropdownMenu.Trigger className="bg-transparent text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none focus:ring-0 border-0 hover:border-0 p-1 sm:p-2">
              <Info className="h-5 w-5 sm:h-6 sm:w-6" />
            </DropdownMenu.Trigger>
            
            <DropdownMenu.Portal>
              <DropdownMenu.Content
                className="w-48 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 z-50 border border-gray-200 dark:border-gray-700"
                align="end"
                sideOffset={8}
              >
                <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer focus:outline-none focus:bg-gray-100 dark:focus:bg-gray-700">
                  <a href="/about" className="block text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:font-medium">About</a>
                </DropdownMenu.Item>
                <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer focus:outline-none focus:bg-gray-100 dark:focus:bg-gray-700">
                  <a href="/contact" className="block text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:font-medium">Contact</a>
                </DropdownMenu.Item>
                <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer focus:outline-none focus:bg-gray-100 dark:focus:bg-gray-700">
                  <a href="/terms" className="block text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:font-medium">Terms</a>
                </DropdownMenu.Item>
                <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer focus:outline-none focus:bg-gray-100 dark:focus:bg-gray-700">
                  <a href="/privacy" className="block text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:font-medium">Privacy</a>
                </DropdownMenu.Item>
              </DropdownMenu.Content>
            </DropdownMenu.Portal>
          </DropdownMenu.Root>
        </div>
      </div>
    </header>
  )
}

// ─── ThemeSwitch ──────────────────────────────────────────
function ThemeSwitch({ value, onChange }) {
  const options = ["light", "system", "dark"];
  const index = options.indexOf(value);

  const WIDTH = 180; // px
  const SEGMENT = WIDTH / 3;

  return (
    <div style={{ width: `${WIDTH}px` }} className="h-9">
      <div className="relative flex h-full rounded-full bg-white dark:bg-gray-800 shadow-inner border border-gray-300 dark:border-gray-600 overflow-hidden">
        {/* Knob */}
        <div
          className="absolute inset-y-0 left-0 rounded-full transition-transform duration-200 z-0 pointer-events-none bg-blue-500"
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
              ${index === i ? "text-white dark:text-white" : "text-gray-700 dark:text-gray-300"}
              focus:outline-none border-none`}
          >
            {mode.charAt(0).toUpperCase() + mode.slice(1)}
          </button>
        ))}
      </div>
    </div>
  );
}
