/**
 * @fileoverview StoreFilter Component - Store selection with search functionality
 * @module components/StoreFilter
 */
import React, { useState, useEffect, useRef } from 'react';
import { Check, Search, X, Store as StoreIcon } from 'lucide-react';
import api from '../api';
import type { Store } from '../types';

/**
 * Props for the StoreFilter component
 */
interface StoreFilterProps {
  /** Array of currently selected store IDs */
  selectedStores: number[];
  /** Callback function when store selection changes */
  onStoreChange: (stores: number[]) => void;
}

/**
 * StoreFilter Component - Store selector with search and multiple selection
 * 
 * Features a compact search input that shows a filtered list of stores on focus.
 * Selected stores are indicated with checkmarks. The list closes when clicking outside.
 * 
 * @param props - Component props
 * @returns JSX element containing the store filter
 * 
 * @example
 * ```tsx
 * function FilterSection() {
 *   const [selectedStores, setSelectedStores] = useState<number[]>([]);
 *   
 *   return (
 *     <StoreFilter 
 *       selectedStores={selectedStores} 
 *       onStoreChange={setSelectedStores} 
 *     />
 *   );
 * }
 * ```
 */
export default function StoreFilter({ selectedStores, onStoreChange }: StoreFilterProps) {
  const [stores, setStores] = useState<Store[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Fetch stores from API on mount
  useEffect(() => {
    const fetchStores = async () => {
      setLoading(true);
      try {
        const response = await api.get('/v1/stores/');
        setStores(response.data as Store[]);
      } catch (error) {
        console.error('Failed to load stores:', error);
        // Fallback to empty array if API fails
        setStores([]);
      } finally {
        setLoading(false);
      }
    };

    fetchStores();
  }, []);

  // Handle click outside to close dropdown
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      return () => document.removeEventListener('mousedown', handleClickOutside);
    }
  }, [isOpen]);

  // Filter stores based on search term
  const filteredStores = stores.filter(store =>
    store.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  /**
   * Toggle store selection
   */
  const handleStoreToggle = (storeId: number) => {
    if (selectedStores.includes(storeId)) {
      onStoreChange(selectedStores.filter(id => id !== storeId));
    } else {
      onStoreChange([...selectedStores, storeId]);
    }
  };

  /**
   * Get display text for the input
   */
  const getInputDisplay = () => {
    if (selectedStores.length === 0) {
      return '';
    }
    const count = selectedStores.length;
    return `${count} store${count !== 1 ? 's' : ''} selected`;
  };

  /**
   * Get store type badge color
   */
  const getStoreTypeBadgeColor = (type: string) => {
    switch (type) {
      case 'online':
        return 'bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-300';
      case 'physical':
        return 'bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-300';
      case 'chain':
        return 'bg-purple-100 text-purple-700 dark:bg-purple-900 dark:text-purple-300';
      default:
        return 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  return (
    <div className="relative" ref={containerRef}>
      {/* Search Input */}
      <div className="relative">
        <StoreIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-blue-500 dark:text-blue-400" />
        <input
          ref={inputRef}
          type="text"
          placeholder={selectedStores.length > 0 ? getInputDisplay() : "Search stores"}
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          onFocus={() => setIsOpen(true)}
          className="w-full pl-9 pr-10 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg 
                     bg-white dark:bg-gray-700 text-gray-900 dark:text-white 
                     placeholder-gray-500 dark:placeholder-gray-400
                     focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400"
        />
        {selectedStores.length > 0 && (
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              onStoreChange([]);
              setSearchTerm('');
            }}
            className="absolute right-3 top-1/2 transform -translate-y-1/2 p-1 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-full transition-colors"
            aria-label="Clear stores"
          >
            <X className="w-4 h-4 text-gray-500 dark:text-gray-400" />
          </button>
        )}
      </div>

      {/* Dropdown List */}
      {isOpen && (
        <div className="absolute z-50 w-full mt-2 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-600 overflow-hidden">
          <div className="max-h-64 overflow-y-auto">
            {loading ? (
              <div className="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">
                Loading stores...
              </div>
            ) : filteredStores.length === 0 ? (
              <div className="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">
                {stores.length === 0 ? 'No stores available' : 'No stores found'}
              </div>
            ) : (
              <ul className="py-1">
                {filteredStores.map(store => {
                  const isSelected = selectedStores.includes(store.id);
                  return (
                    <li key={store.id}>
                      <button
                        type="button"
                        onClick={() => handleStoreToggle(store.id)}
                        className="w-full px-4 py-2 text-left text-sm hover:bg-gray-100 dark:hover:bg-gray-700 
                                 flex items-center justify-between group transition-colors"
                      >
                        <div className="flex items-center gap-2">
                          <span className={`${isSelected ? 'font-medium text-blue-600 dark:text-blue-400' : 'text-gray-700 dark:text-gray-300'}`}>
                            {store.name}
                          </span>
                          <span className={`text-xs px-1.5 py-0.5 rounded-full ${getStoreTypeBadgeColor(store.type)}`}>
                            {store.type}
                          </span>
                        </div>
                        {isSelected && (
                          <Check className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                        )}
                      </button>
                    </li>
                  );
                })}
              </ul>
            )}
          </div>
          
          {/* Clear selection button */}
          {selectedStores.length > 0 && (
            <div className="border-t border-gray-200 dark:border-gray-600 px-4 py-2">
              <button
                type="button"
                onClick={() => {
                  onStoreChange([]);
                  setSearchTerm('');
                }}
                className="text-xs text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
              >
                Clear selection
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
}