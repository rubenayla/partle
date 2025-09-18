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
import StoreFilter from './StoreFilter';
import MobileSearchLayout from './MobileSearchLayout';
import DesktopSearchLayout from './DesktopSearchLayout';
import * as DropdownMenu from '@radix-ui/react-dropdown-menu';
import api from '../api/index';
import { ProductSearchParams, User as UserType, Theme } from '../types';

interface SearchBarProps {
  onSearch?: (params: ProductSearchParams) => void;
  isLoggedIn?: boolean;
  onAccountClick?: () => void;
  currentTheme: Theme;
  setTheme: (theme: Theme) => void;
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
  const [selectedStores, setSelectedStores] = useState<number[]>([]);
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
        selectedStores,
        sortBy: sortBy as any,
        sortOrder: 'desc'
      };
      onSearch(searchParams);
    }
  };

  const handleSortChange = (value: string) => {
    setSortBy(value);
  };

  return (
    <>
      {/* Mobile layout uses separate component to prevent re-renders */}
      <div className="sm:hidden">
        <MobileSearchLayout
          query={query}
          setQuery={setQuery}
          searchType={searchType}
          setSearchType={setSearchType}
          priceMin={priceMin}
          setPriceMin={setPriceMin}
          priceMax={priceMax}
          setPriceMax={setPriceMax}
          selectedTags={selectedTags}
          setSelectedTags={setSelectedTags}
          selectedStores={selectedStores}
          setSelectedStores={setSelectedStores}
          sortBy={sortBy}
          setSortBy={setSortBy}
          handleSearch={handleSearch}
          isLoggedIn={isLoggedIn}
          onAccountClick={onAccountClick}
          user={user}
          currentTheme={currentTheme}
          setTheme={setTheme}
        />
      </div>
      {/* Desktop header uses separate component to prevent re-renders */}
      <header className="hidden sm:block fixed top-0 left-0 right-0 z-20 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700">
        <DesktopSearchLayout
          query={query}
          setQuery={setQuery}
          searchType={searchType}
          setSearchType={setSearchType}
          priceMin={priceMin}
          setPriceMin={setPriceMin}
          priceMax={priceMax}
          setPriceMax={setPriceMax}
          selectedTags={selectedTags}
          setSelectedTags={setSelectedTags}
          selectedStores={selectedStores}
          setSelectedStores={setSelectedStores}
          sortBy={sortBy}
          setSortBy={setSortBy}
          handleSearch={handleSearch}
          isLoggedIn={isLoggedIn}
          onAccountClick={onAccountClick}
          user={user}
          currentTheme={currentTheme}
          setTheme={setTheme}
        />
      </header>
    </>
  );
}

/**
 * Props for ThemeSwitch component
 */
interface ThemeSwitchProps {
  /** Current theme value */
  value: Theme;
  /** Callback when theme changes */
  onChange: (theme: Theme) => void;
}

/**
 * ThemeSwitch Component - Toggle between light/system/dark themes
 * 
 * @param props - Component props
 * @returns JSX element containing the theme switch
 */
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