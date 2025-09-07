/**
 * @fileoverview SearchBar Component - Main navigation and search interface
 * @module components/SearchBar
 */
import React, { useState, useRef, useEffect } from 'react';
import { Search, User, Info, Plus } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { deleteAccount, currentUser } from '../api/auth';
import Tooltip from './Tooltip';
import TagFilter from './TagFilter';
import * as DropdownMenu from '@radix-ui/react-dropdown-menu';
import api from '../api/index';
import { ProductSearchParams, User as UserType } from '../types';

interface SearchBarProps {
  onSearch?: (params: ProductSearchParams) => void;
  isLoggedIn?: boolean;
  onAccountClick?: () => void;
  currentTheme?: string;
  setTheme?: (theme: string) => void;
}

const sortOptions: Record<string, string> = {
  random: 'Random',
  price_desc: 'Price ↓',
  name_asc: 'Name A-Z',
  created_at: 'Newest',
};

export default function SearchBar({
  onSearch = () => { },
  isLoggedIn = false,
  onAccountClick = () => { },
  currentTheme,
  setTheme,
}: SearchBarProps) {
  const [query, setQuery] = useState<string>('');
  const [searchType, setSearchType] = useState<'products' | 'stores'>('products');
  const [priceMin, setPriceMin] = useState<number>(0);
  const [priceMax, setPriceMax] = useState<number>(500);
  const [selectedTags, setSelectedTags] = useState<number[]>([]);
  const [sortBy, setSortBy] = useState<string>('random');
  const [user, setUser] = useState<UserType | null>(null);
  const navigate = useNavigate();

  // Fetch current user when logged in
  useEffect(() => {
    if (isLoggedIn) {
      currentUser()
        .then(userData => setUser(userData))
        .catch(() => setUser(null));
    } else {
      setUser(null);
    }
  }, [isLoggedIn]);

  const handleSearch = (event: React.FormEvent) => {
    event.preventDefault();
    if (onSearch) {
      const searchParams: ProductSearchParams = {
        query,
        searchType,
        priceMin,
        priceMax,
        selectedTags,
        sortBy: sortBy as any,
        sortOrder: 'desc'
      };
      onSearch(searchParams);
    }
  };

  const handleSortChange = (value: string) => {
    setSortBy(value);
    if (onSearch) {
      const params: ProductSearchParams = {
        query,
        searchType,
        priceMin,
        priceMax,
        selectedTags,
        sortBy: value as any,
        sortOrder: 'desc'
      };
      onSearch(params);
    }
  };

  // Mobile Layout (3 rows)
  const MobileLayout = () => (
    <div className="flex flex-col px-2 py-2">
      {/* Row 1: Search bar */}
      <form onSubmit={handleSearch} className="flex w-full mb-2 bg-gray-100 dark:bg-gray-800 rounded-full pl-3 pr-1 h-10 items-center">
        <input
          type="search"
          placeholder="Search products"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-1 h-full bg-transparent placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white focus:outline-none text-sm"
        />
        <button
          type="submit"
          aria-label="Search"
          className="p-1.5 rounded-full bg-blue-500 dark:bg-blue-600 text-white hover:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none transition-colors"
        >
          <Search className="h-4 w-4" />
        </button>
      </form>

      {/* Row 2: Filters and Sort */}
      <div className="flex items-center justify-between gap-2 mb-2">
        {/* Filters Button */}
        <DropdownMenu.Root>
          <DropdownMenu.Trigger className="flex items-center px-3 py-1.5 text-sm text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-800 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 focus:outline-none">
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
                  onTagsChange={(tags) => {
                    setSelectedTags(tags);
                    if (onSearch) {
                      const params: ProductSearchParams = {
                        query,
                        searchType,
                        priceMin,
                        priceMax,
                        selectedTags: tags,
                        sortBy: sortBy as any,
                        sortOrder: 'desc'
                      };
                      onSearch(params);
                    }
                  }}
                />
              </div>
            </DropdownMenu.Content>
          </DropdownMenu.Portal>
        </DropdownMenu.Root>

        {/* Sort Dropdown */}
        <DropdownMenu.Root>
          <DropdownMenu.Trigger className="flex items-center px-3 py-1.5 text-sm text-gray-700 dark:text-gray-300 bg-gray-100 dark:bg-gray-800 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 focus:outline-none">
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
                  onSelect={() => handleSortChange(value)}
                >
                  {label}
                </DropdownMenu.Item>
              ))}
            </DropdownMenu.Content>
          </DropdownMenu.Portal>
        </DropdownMenu.Root>
      </div>

      {/* Row 3: Navigation icons */}
      <div className="flex items-center justify-between">
        <a
          href="/"
          className="text-xl font-bold text-gray-900 dark:text-white hover:text-gray-700 dark:hover:text-gray-300 transition-colors px-2"
        >
          Partle
        </a>

        <div className="flex items-center gap-3">
          {isLoggedIn && (
            <DropdownMenu.Root>
              <DropdownMenu.Trigger className="p-1.5 text-gray-600 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300">
                <Plus className="h-5 w-5" />
              </DropdownMenu.Trigger>
              <DropdownMenu.Portal>
                <DropdownMenu.Content
                  className="w-48 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 z-50 border border-gray-200 dark:border-gray-700"
                  align="end"
                  sideOffset={8}
                >
                  <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
                    <a href="/products/new" className="block">Add product</a>
                  </DropdownMenu.Item>
                  <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
                    <a href="/stores/new" className="block">Add store</a>
                  </DropdownMenu.Item>
                </DropdownMenu.Content>
              </DropdownMenu.Portal>
            </DropdownMenu.Root>
          )}

          <DropdownMenu.Root>
            <DropdownMenu.Trigger
              className="p-1.5 text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white"
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
                    <a href="/products/my" className="block">My Products</a>
                  </DropdownMenu.Item>
                  <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
                    <a href="/account" className="block">Account</a>
                  </DropdownMenu.Item>
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
                </DropdownMenu.Content>
              </DropdownMenu.Portal>
            )}
          </DropdownMenu.Root>

          <DropdownMenu.Root>
            <DropdownMenu.Trigger className="p-1.5 text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white">
              <Info className="h-5 w-5" />
            </DropdownMenu.Trigger>
            <DropdownMenu.Portal>
              <DropdownMenu.Content
                className="w-48 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 z-50 border border-gray-200 dark:border-gray-700"
                align="end"
                sideOffset={8}
              >
                <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
                  <a href="/about" className="block">About</a>
                </DropdownMenu.Item>
                <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
                  <a href="/docs" className="block">Documentation</a>
                </DropdownMenu.Item>
                <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
                  <a href="/api-docs" className="block">API Docs</a>
                </DropdownMenu.Item>
              </DropdownMenu.Content>
            </DropdownMenu.Portal>
          </DropdownMenu.Root>
        </div>
      </div>
    </div>
  );

  // Desktop Layout (single row)
  const DesktopLayout = () => (
    <div className="w-full max-w-screen-2xl mx-auto flex items-center justify-between px-2 sm:px-4 py-3">
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
        className="flex flex-1 mx-2 md:mx-4 lg:mx-6 bg-gray-100 dark:bg-gray-800 rounded-full pl-3 md:pl-4 pr-1 sm:pr-2 h-12 items-center"
      >
        <input
          type="search"
          placeholder="Search products around you"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          className="flex-1 h-full bg-transparent placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white focus:outline-none"
          autoFocus
        />

        <div className="h-6 border-l border-gray-300 dark:border-gray-600 mx-2 md:mx-3" />

        {/* Desktop Filters */}
        <DropdownMenu.Root>
          <DropdownMenu.Trigger className="h-full px-2 md:px-3 text-sm text-gray-700 dark:text-gray-300 bg-transparent hover:bg-gray-200 dark:hover:bg-gray-700 focus:outline-none">
            Filters
          </DropdownMenu.Trigger>
          <DropdownMenu.Portal>
            <DropdownMenu.Content
              className="w-64 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 z-[100] border border-gray-200 dark:border-gray-600 space-y-4"
              align="end"
              sideOffset={8}
            >
              {/* Same filter content as mobile */}
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
                  onTagsChange={(tags) => {
                    setSelectedTags(tags);
                    if (onSearch) {
                      const params: ProductSearchParams = {
                        query,
                        searchType,
                        priceMin,
                        priceMax,
                        selectedTags: tags,
                        sortBy: sortBy as any,
                        sortOrder: 'desc'
                      };
                      onSearch(params);
                    }
                  }}
                />
              </div>
            </DropdownMenu.Content>
          </DropdownMenu.Portal>
        </DropdownMenu.Root>

        <div className="hidden md:block h-6 border-l border-gray-300 dark:border-gray-600 mx-2 md:mx-3" />

        {/* Desktop Sort */}
        <DropdownMenu.Root>
          <DropdownMenu.Trigger className="hidden md:block h-full px-2 md:px-3 text-sm text-gray-700 dark:text-gray-300 bg-transparent hover:bg-gray-200 dark:hover:bg-gray-700 focus:outline-none whitespace-nowrap">
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
                  onSelect={() => handleSortChange(value)}
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
          className="p-2 rounded-full bg-blue-500 dark:bg-blue-600 text-white hover:bg-blue-600 dark:hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-400 transition-colors"
        >
          <Search className="h-5 w-5" />
        </button>
      </form>

      <div className="flex items-center gap-2 md:gap-3">
        {isLoggedIn && (
          <DropdownMenu.Root>
            <DropdownMenu.Trigger className="bg-transparent text-gray-600 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none p-2">
              <Plus className="h-6 w-6" />
            </DropdownMenu.Trigger>
            <DropdownMenu.Portal>
              <DropdownMenu.Content
                className="w-48 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 z-50 border border-gray-200 dark:border-gray-700"
                align="end"
                sideOffset={8}
              >
                <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
                  <Tooltip text="Add product (Alt+N, P)">
                    <a href="/products/new" className="block">Add product</a>
                  </Tooltip>
                </DropdownMenu.Item>
                <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
                  <Tooltip text="Add store (Alt+N, S)">
                    <a href="/stores/new" className="block">Add store</a>
                  </Tooltip>
                </DropdownMenu.Item>
              </DropdownMenu.Content>
            </DropdownMenu.Portal>
          </DropdownMenu.Root>
        )}

        <DropdownMenu.Root>
          <DropdownMenu.Trigger
            className="bg-transparent text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none p-2"
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
                  <a href="/products/my" className="block">My Products</a>
                </DropdownMenu.Item>
                <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
                  <a href="/account" className="block">Account</a>
                </DropdownMenu.Item>
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
              </DropdownMenu.Content>
            </DropdownMenu.Portal>
          )}
        </DropdownMenu.Root>

        <DropdownMenu.Root>
          <DropdownMenu.Trigger className="bg-transparent text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none p-2">
            <Info className="h-6 w-6" />
          </DropdownMenu.Trigger>
          <DropdownMenu.Portal>
            <DropdownMenu.Content
              className="w-48 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 z-50 border border-gray-200 dark:border-gray-700"
              align="end"
              sideOffset={8}
            >
              <DropdownMenu.Item className="block px-2 py-1 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded cursor-pointer">
                <a href="/about" className="block">About</a>
              </DropdownMenu.Item>
            </DropdownMenu.Content>
          </DropdownMenu.Portal>
        </DropdownMenu.Root>
      </div>
    </div>
  );

  return (
    <header className="fixed sm:top-0 sm:bottom-auto bottom-0 left-0 right-0 z-20 bg-white dark:bg-gray-900 sm:border-b border-t sm:border-t-0 border-gray-200 dark:border-gray-700">
      {/* Show mobile layout on small screens, desktop on larger */}
      <div className="sm:hidden">
        <MobileLayout />
      </div>
      <div className="hidden sm:block">
        <DesktopLayout />
      </div>
    </header>
  );
}