import React from 'react';
import { Search, User, Info, Plus } from 'lucide-react';
import * as DropdownMenu from '@radix-ui/react-dropdown-menu';
import Tooltip from './Tooltip';
import TagFilter from './TagFilter';
import StoreFilter from './StoreFilter';
import { deleteAccount, currentUser } from '../api/auth';
import { ProductSearchParams, User as UserType, Theme } from '../types';

interface DesktopSearchLayoutProps {
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
  distance: '📍 Near me',
  random: '🎲 Random',
  price_desc: '💰 Price ↓',
  name_asc: '🔤 Name A-Z',
  created_at: '✨ Newest',
};

export default function DesktopSearchLayout({
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
}: DesktopSearchLayoutProps) {
  return (
    <div className="w-full max-w-screen-2xl mx-auto flex items-center justify-between gap-4 px-4 sm:px-6 py-3 rounded-[28px] border border-white/20 dark:border-white/5 bg-gradient-to-br from-white/40 via-white/25 to-white/15 dark:from-slate-900/90 dark:via-slate-900/70 dark:to-slate-950/60 shadow-[0_25px_60px_-30px_rgba(15,23,42,0.6)] dark:shadow-[0_35px_70px_-40px_rgba(0,0,0,0.95)] backdrop-blur-2xl transition-[background,box-shadow,border-color] duration-300">
      <Tooltip text="Go home (Alt+N, H)">
        <a
          href="/"
          className="text-2xl font-bold text-gray-900 dark:text-white hover:text-gray-700 dark:hover:text-gray-300 transition-colors"
        >
          Partle
        </a>
      </Tooltip>

      <form
        onSubmit={handleSearch}
        className="flex flex-1 mx-2 md:mx-4 lg:mx-6 rounded-[9999px] h-11 items-center pl-3 md:pl-4 pr-1 sm:pr-2 bg-transparent border border-transparent focus-within:bg-white/10 dark:focus-within:bg-white/5 focus-within:shadow-[0_0_25px_rgba(255,255,255,0.15)] transition-all"
      >
        <input
          type="search"
          placeholder="Search products around you"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-1 h-full bg-transparent placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white focus:outline-none"
        />

        <div className="h-6 border-l border-white/30 dark:border-white/10 mx-2 md:mx-3" />

        {/* Desktop Filters */}
        <DropdownMenu.Root>
          <DropdownMenu.Trigger className="h-full px-2 md:px-3 text-sm text-gray-600 dark:text-gray-400 bg-transparent hover:text-gray-900 dark:hover:text-gray-100 focus:outline-none transition-colors">
            Filters
          </DropdownMenu.Trigger>
          <DropdownMenu.Portal>
            <DropdownMenu.Content
              className="w-64 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 z-[100] border border-gray-200 dark:border-gray-600 space-y-4"
              align="end"
              sideOffset={8}
            >
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700 dark:text-gray-300">Search Type</label>
                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={() => setSearchType('products')}
                    className={`px-3 py-1 rounded-full text-sm font-medium ${
                      searchType === 'products'
                        ? 'bg-gray-700 dark:bg-gray-600 text-white'
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
                        ? 'bg-gray-700 dark:bg-gray-600 text-white'
                        : 'bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-200'
                    }`}
                  >
                    Stores
                  </button>
                </div>
              </div>

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

        <div className="hidden md:block h-6 border-l border-white/30 dark:border-white/10 mx-2 md:mx-3" />

        {/* Desktop Sort */}
        <DropdownMenu.Root>
          <DropdownMenu.Trigger className="hidden md:block h-full px-2 md:px-3 text-sm text-gray-600 dark:text-gray-400 bg-transparent hover:text-gray-900 dark:hover:text-gray-100 focus:outline-none whitespace-nowrap transition-colors">
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

        <div className="h-6 border-l border-gray-300 dark:border-gray-600 mx-2 md:mx-3" />

        <button
          type="submit"
          aria-label="Search"
          className="p-2 rounded-full bg-blue-500 text-white hover:bg-blue-600 dark:hover:bg-blue-400 focus:outline-none transition-colors"
        >
          <Search className="h-5 w-5" />
        </button>
      </form>

      <div className="flex items-center gap-2 md:gap-3">
        {isLoggedIn && (
          <DropdownMenu.Root>
            <DropdownMenu.Trigger className="rounded-full bg-transparent text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-white/40 dark:hover:bg-slate-800/70 focus:outline-none p-2 transition-colors">
              <Plus className="h-6 w-6" />
            </DropdownMenu.Trigger>
            <DropdownMenu.Portal>
              <DropdownMenu.Content
                className="w-48 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-2 z-50 border border-gray-200 dark:border-gray-700 max-h-96 overflow-y-auto"
                align="end"
                sideOffset={8}
              >
                <DropdownMenu.Item className="block px-2 py-1 text-gray-900 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
                  <Tooltip text="Add product (Alt+N, P)">
                    <a href="/products/new" className="block text-inherit">Add product</a>
                  </Tooltip>
                </DropdownMenu.Item>
                <DropdownMenu.Item className="block px-2 py-1 text-gray-900 dark:text-white hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
                  <Tooltip text="Add store (Alt+N, S)">
                    <a href="/stores/new" className="block text-inherit">Add store</a>
                  </Tooltip>
                </DropdownMenu.Item>
              </DropdownMenu.Content>
            </DropdownMenu.Portal>
          </DropdownMenu.Root>
        )}

        <DropdownMenu.Root>
          <DropdownMenu.Trigger
            className="rounded-full bg-transparent text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-white/40 dark:hover:bg-slate-800/70 focus:outline-none p-2 transition-colors"
            onClick={!isLoggedIn ? onAccountClick : undefined}
          >
            <User className="h-7 w-7" />
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
          <DropdownMenu.Trigger className="rounded-full bg-transparent text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-white/40 dark:hover:bg-slate-800/70 focus:outline-none p-2 transition-colors">
            <Info className="h-6 w-6" />
          </DropdownMenu.Trigger>
          <DropdownMenu.Portal>
            <DropdownMenu.Content
              className="w-48 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 z-50 border border-gray-200 dark:border-gray-700"
              align="end"
              sideOffset={8}
            >
              <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
                <a href="/documentation" target="_blank" rel="noopener noreferrer" className="block text-inherit">Documentation</a>
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
