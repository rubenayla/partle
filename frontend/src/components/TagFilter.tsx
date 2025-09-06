/**
 * @fileoverview TagFilter Component - Notion-style tag selection with search
 * @module components/TagFilter
 */
import React, { useState, useEffect, useRef } from 'react';
import { Check, Search, X } from 'lucide-react';
import { getTags } from '../api/tags';
import type { Tag } from '../types';

/**
 * Props for the TagFilter component
 */
interface TagFilterProps {
  /** Array of currently selected tag IDs */
  selectedTags: number[];
  /** Callback function when tag selection changes */
  onTagChange: (tags: number[]) => void;
}

/**
 * TagFilter Component - Notion-style tag selector with popup list
 * 
 * Features a compact search input that shows a filtered list of tags on focus.
 * Selected tags are indicated with checkmarks. The list closes when clicking outside.
 * 
 * @param props - Component props
 * @returns JSX element containing the tag filter
 * 
 * @example
 * ```tsx
 * function FilterSection() {
 *   const [selectedTags, setSelectedTags] = useState<number[]>([]);
 *   
 *   return (
 *     <TagFilter 
 *       selectedTags={selectedTags} 
 *       onTagChange={setSelectedTags} 
 *     />
 *   );
 * }
 * ```
 */
export default function TagFilter({ selectedTags, onTagChange }: TagFilterProps) {
  const [tags, setTags] = useState<Tag[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [isOpen, setIsOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // Fetch tags from API on mount
  useEffect(() => {
    const fetchTags = async () => {
      setLoading(true);
      try {
        const fetchedTags = await getTags();
        setTags(fetchedTags);
      } catch (error) {
        console.error('Failed to load tags:', error);
        // Fallback to empty array if API fails
        setTags([]);
      } finally {
        setLoading(false);
      }
    };

    fetchTags();
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

  // Filter tags based on search term
  const filteredTags = tags.filter(tag =>
    tag.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  /**
   * Toggle tag selection
   */
  const handleTagToggle = (tagId: number) => {
    if (selectedTags.includes(tagId)) {
      onTagChange(selectedTags.filter(id => id !== tagId));
    } else {
      onTagChange([...selectedTags, tagId]);
    }
  };

  /**
   * Get display text for the input
   */
  const getInputDisplay = () => {
    if (selectedTags.length === 0) {
      return '';
    }
    const count = selectedTags.length;
    return `${count} tag${count !== 1 ? 's' : ''} selected`;
  };

  return (
    <div className="relative" ref={containerRef}>
      {/* Search Input */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-blue-500 dark:text-blue-400" />
        <input
          ref={inputRef}
          type="text"
          placeholder={selectedTags.length > 0 ? getInputDisplay() : "Search tags"}
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          onFocus={() => setIsOpen(true)}
          className="w-full pl-9 pr-10 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg 
                     bg-white dark:bg-gray-700 text-gray-900 dark:text-white 
                     placeholder-gray-500 dark:placeholder-gray-400
                     focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400"
        />
        {selectedTags.length > 0 && (
          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              onTagChange([]);
              setSearchTerm('');
            }}
            className="absolute right-3 top-1/2 transform -translate-y-1/2 p-1 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-full transition-colors"
            aria-label="Clear tags"
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
                Loading tags...
              </div>
            ) : filteredTags.length === 0 ? (
              <div className="px-4 py-3 text-sm text-gray-500 dark:text-gray-400">
                {tags.length === 0 ? 'No tags available' : 'No tags found'}
              </div>
            ) : (
              <ul className="py-1">
                {filteredTags.map(tag => {
                  const isSelected = selectedTags.includes(tag.id);
                  return (
                    <li key={tag.id}>
                      <button
                        type="button"
                        onClick={() => handleTagToggle(tag.id)}
                        className="w-full px-4 py-2 text-left text-sm hover:bg-gray-100 dark:hover:bg-gray-700 
                                 flex items-center justify-between group transition-colors"
                      >
                        <span className={`${isSelected ? 'font-medium text-blue-600 dark:text-blue-400' : 'text-gray-700 dark:text-gray-300'}`}>
                          {tag.name}
                        </span>
                        <div className="flex items-center gap-2">
                          {tag.product_count !== undefined && (
                            <span className="text-xs text-gray-400 dark:text-gray-500">
                              {tag.product_count}
                            </span>
                          )}
                          {isSelected && (
                            <Check className="w-4 h-4 text-blue-600 dark:text-blue-400" />
                          )}
                        </div>
                      </button>
                    </li>
                  );
                })}
              </ul>
            )}
          </div>
          
          {/* Clear selection button */}
          {selectedTags.length > 0 && (
            <div className="border-t border-gray-200 dark:border-gray-600 px-4 py-2">
              <button
                type="button"
                onClick={() => {
                  onTagChange([]);
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