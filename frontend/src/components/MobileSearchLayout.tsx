import React from 'react';
import { Search, User, Info, Plus } from 'lucide-react';
import * as DropdownMenu from '@radix-ui/react-dropdown-menu';
import TagFilter from './TagFilter';
import StoreFilter from './StoreFilter';
import { deleteAccount, currentUser } from '../api/auth';
import { ProductSearchParams, User as UserType, Theme } from '../types';

interface MobileSearchLayoutProps {
  query: string;
  setQuery: (query: string) => void;
  searchType: 'products' | 'stores';
  setSearchType: (type: 'products' | 'stores') => void;
  priceMin: number;
  setPriceMin: (price: number) => void;
  priceMax: number;
  setPriceMax: (price: number) => void;
  selectedTags: number[];
  setSelectedTags: (tags: number[]) => void;
  selectedStores: number[];
  setSelectedStores: (stores: number[]) => void;
  sortBy: string;
  setSortBy: (sort: string) => void;
  handleSearch: (event: React.FormEvent) => void;
  isLoggedIn: boolean;
  onAccountClick: () => void;
  user: UserType | null;
  currentTheme: Theme;
  setTheme: (theme: Theme) => void;
}

const sortOptions: Record<string, string> = {
  random: 'Random',
  price_desc: 'Price ↓',
  name_asc: 'Name A-Z',
  created_at: 'Newest',
};

export default function MobileSearchLayout({
  query,
  setQuery,
  searchType,
  setSearchType,
  priceMin,
  setPriceMin,
  priceMax,
  setPriceMax,
  selectedTags,
  setSelectedTags,
  selectedStores,
  setSelectedStores,
  sortBy,
  setSortBy,
  handleSearch,
  isLoggedIn,
  onAccountClick,
  user,
  currentTheme,
  setTheme,
}: MobileSearchLayoutProps) {
  return (
    <>
      {/* Floating top buttons */}
      <div className="fixed top-0 left-0 right-0 z-30 flex items-center justify-between px-4 py-3">
        <a
          href="/"
          className="text-xl font-bold text-gray-900 dark:text-white drop-shadow-lg bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm px-3 py-1 rounded-full"
        >
          Partle
        </a>

        <div className="flex items-center gap-2">
          {isLoggedIn && (
            <DropdownMenu.Root>
              <DropdownMenu.Trigger className="p-2 text-gray-700 dark:text-gray-300 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-full shadow-lg">
                <Plus className="h-5 w-5" />
              </DropdownMenu.Trigger>
              <DropdownMenu.Portal>
                <DropdownMenu.Content
                  className="w-48 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-2 z-50 border border-gray-200 dark:border-gray-700 max-h-96 overflow-y-auto"
                  align="end"
                  sideOffset={8}
                >
                  <DropdownMenu.Item className="block px-2 py-1 text-gray-900 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
                    <a href="/products/new" className="block text-inherit">Add product</a>
                  </DropdownMenu.Item>
                  <DropdownMenu.Item className="block px-2 py-1 text-gray-900 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
                    <a href="/stores/new" className="block text-inherit">Add store</a>
                  </DropdownMenu.Item>
                </DropdownMenu.Content>
              </DropdownMenu.Portal>
            </DropdownMenu.Root>
          )}

          <DropdownMenu.Root>
            <DropdownMenu.Trigger
              className="p-2 text-gray-700 dark:text-gray-300 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-full shadow-lg"
              onClick={!isLoggedIn ? onAccountClick : undefined}
            >
              <User className="h-5 w-5" />
            </DropdownMenu.Trigger>
            {isLoggedIn && (
              <DropdownMenu.Portal>
                <DropdownMenu.Content
                  className="w-56 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 z-50 border border-gray-200 dark:border-gray-600"
                  align="end"
                  sideOffset={8}
                >
                  <div className="px-2 pb-3 mb-2 border-b border-gray-200 dark:border-gray-600">
                    <div className="text-sm text-gray-500 dark:text-gray-400">Logged in as</div>
                    <div className="font-medium text-gray-900 dark:text-white">
                      {user?.username ? `@${user.username}` : user?.email}
                    </div>
                  </div>
                  <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
                    <a href="/products/my" className="block text-inherit">My Products</a>
                  </DropdownMenu.Item>
                  <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
                    <a href="/account" className="block text-inherit">Account</a>
                  </DropdownMenu.Item>
                  <div className="mt-2 px-2 py-1">
                    <div className="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-2">Theme</div>
                    <ThemeSwitch value={currentTheme} onChange={setTheme} />
                  </div>
                  <DropdownMenu.Separator className="border-t border-gray-200 dark:border-gray-600 my-2" />
                  <DropdownMenu.Item
                    className="block w-full text-left px-2 py-1 text-red-600 dark:text-red-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer"
                    onSelect={() => {
                      localStorage.removeItem('token');
                      window.location.reload();
                    }}
                  >
                    Log out
                  </DropdownMenu.Item>
                  <DropdownMenu.Item
                    className="mt-1 block w-full text-left px-2 py-1 text-red-600 dark:text-red-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer"
                    onSelect={async () => {
                      if (confirm('Delete account? This action cannot be undone.')) {
                        try {
                          await deleteAccount();
                          localStorage.removeItem('token');
                          window.location.href = '/';
                        } catch (error) {
                          alert('Could not delete account');
                        }
                      }
                    }}
                  >
                    Delete account
                  </DropdownMenu.Item>
                  <DropdownMenu.Separator className="border-t border-gray-200 dark:border-gray-600 my-2" />
                  <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
                    <a href="/premium" className="block text-inherit">Premium</a>
                  </DropdownMenu.Item>
                </DropdownMenu.Content>
              </DropdownMenu.Portal>
            )}
          </DropdownMenu.Root>

          <DropdownMenu.Root>
            <DropdownMenu.Trigger className="p-2 text-gray-700 dark:text-gray-300 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm rounded-full shadow-lg">
              <Info className="h-5 w-5" />
            </DropdownMenu.Trigger>
            <DropdownMenu.Portal>
              <DropdownMenu.Content
                className="w-48 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-2 z-50 border border-gray-200 dark:border-gray-700 max-h-96 overflow-y-auto"
                align="end"
                sideOffset={8}
              >
                <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
                  <a href="/documentation" className="block text-inherit">Documentation</a>
                </DropdownMenu.Item>
                <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
                  <a href="/about" className="block text-inherit">About</a>
                </DropdownMenu.Item>
                <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
                  <a href="/contact" className="block text-inherit">Contact</a>
                </DropdownMenu.Item>
                <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
                  <a href="/terms" className="block text-inherit">Terms</a>
                </DropdownMenu.Item>
                <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
                  <a href="/privacy" className="block text-inherit">Privacy</a>
                </DropdownMenu.Item>
              </DropdownMenu.Content>
            </DropdownMenu.Portal>
          </DropdownMenu.Root>
        </div>
      </div>

      {/* Bottom container fully rounded with margins - Gemini style */}
      <div className="fixed bottom-2 left-2 right-2 z-40 bg-white dark:bg-gray-900 rounded-3xl border border-gray-300 dark:border-gray-600 px-4 pt-4 pb-3" style={{ position: 'fixed' }}>
        {/* Search input with icon button */}
        <form onSubmit={handleSearch} className="flex items-center gap-2 mb-3" id="mobile-search-form">
          <input
            type="search"
            placeholder="Search products around you"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="flex-1 bg-transparent placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white focus:outline-none text-base px-2 py-3"
          />
          <button
            type="submit"
            aria-label="Search"
            className="p-2.5 rounded-full text-blue-500 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 transition-colors"
          >
            <Search className="h-5 w-5" />
          </button>
        </form>

        {/* Filter buttons row */}
        <div className="flex items-center gap-2 overflow-x-auto border-t border-gray-200 dark:border-gray-700 pt-3">
          {/* Filters Button */}
          <DropdownMenu.Root>
            <DropdownMenu.Trigger className="flex items-center px-4 py-1.5 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-800 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 focus:outline-none whitespace-nowrap transition-colors">
              Filters
            </DropdownMenu.Trigger>
            <DropdownMenu.Portal>
              <DropdownMenu.Content
                className="w-64 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 z-[100] border border-gray-200 dark:border-gray-600 space-y-4"
                align="start"
                sideOffset={8}
              >
                {/* Search Type Toggle */}
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Search Type</label>
                  <div className="flex items-center gap-2">
                    <button
                      type="button"
                      onClick={() => setSearchType('products')}
                      className={`px-3 py-1 rounded-full text-sm font-medium ${
                        searchType === 'products'
                          ? 'bg-blue-500 text-white'
                          : 'bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-200'
                      }`}
                    >
                      Products
                    </button>
                    <button
                      type="button"
                      onClick={() => setSearchType('stores')}
                      className={`px-3 py-1 rounded-full text-sm font-medium ${
                        searchType === 'stores'
                          ? 'bg-blue-500 text-white'
                          : 'bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-200'
                      }`}
                    >
                      Stores
                    </button>
                  </div>
                </div>

                {/* Price Range */}
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Price Range</label>
                  <div className="flex items-center gap-2">
                    <input
                      type="number"
                      min="0"
                      value={priceMin}
                      onChange={(e) => setPriceMin(Number(e.target.value))}
                      placeholder="Min"
                      className="w-full px-2 py-1 border border-gray-300 dark:border-gray-600 rounded dark:bg-gray-700 dark:text-white"
                    />
                    <span className="text-gray-500">-</span>
                    <input
                      type="number"
                      min="0"
                      value={priceMax}
                      onChange={(e) => setPriceMax(Number(e.target.value))}
                      placeholder="Max"
                      className="w-full px-2 py-1 border border-gray-300 dark:border-gray-600 rounded dark:bg-gray-700 dark:text-white"
                    />
                  </div>
                </div>

                {/* Tags */}
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Tags</label>
                  <TagFilter
                    selectedTags={selectedTags}
                    onTagChange={(tags) => {
                      setSelectedTags(tags);
                    }}
                  />
                </div>

                {/* Stores */}
                <div className="space-y-2">
                  <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Stores</label>
                  <StoreFilter
                    selectedStores={selectedStores}
                    onStoreChange={(stores) => {
                      setSelectedStores(stores);
                    }}
                  />
                </div>
              </DropdownMenu.Content>
            </DropdownMenu.Portal>
          </DropdownMenu.Root>

          {/* Sort Dropdown */}
          <DropdownMenu.Root>
            <DropdownMenu.Trigger className="flex items-center px-4 py-1.5 text-sm font-medium text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-800 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 focus:outline-none whitespace-nowrap transition-colors">
              Sort: {sortOptions[sortBy]}
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
                    className={`block w-full text-left px-2 py-1 rounded hover:bg-gray-100 dark:hover:bg-gray-700 cursor-pointer focus:outline-none ${
                      sortBy === value
                        ? 'font-semibold text-gray-900 dark:text-white'
                        : 'text-gray-700 dark:text-gray-300'
                    }`}
                    onSelect={() => setSortBy(value)}
                  >
                    {label}
                  </DropdownMenu.Item>
                ))}
              </DropdownMenu.Content>
            </DropdownMenu.Portal>
          </DropdownMenu.Root>
        </div>
      </div>
    </>
  );
}

/**
 * ThemeSwitch Component - Toggle between light/system/dark themes
 */
interface ThemeSwitchProps {
  value: Theme;
  onChange: (theme: Theme) => void;
}

function ThemeSwitch({ value, onChange }: ThemeSwitchProps) {
  const options: Theme[] = ['light', 'system', 'dark'];
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
              ${index === i ? 'text-white dark:text-white' : 'text-gray-700 dark:text-gray-300'}
              focus:outline-none border-none`}
          >
            {mode.charAt(0).toUpperCase() + mode.slice(1)}
          </button>
        ))}
      </div>
    </div>
  );
}