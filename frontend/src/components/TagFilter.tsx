/**
 * @fileoverview TagFilter Component - Tag selection interface for search filtering
 * @module components/TagFilter
 */
import React from 'react';

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
 * TagFilter Component - Interactive tag selection for filtering
 * 
 * Displays available tags as clickable buttons. Selected tags are highlighted.
 * Currently uses hardcoded example tags - should be replaced with API data.
 * 
 * Features:
 * - Toggle tag selection on click
 * - Visual indication of selected tags
 * - Responsive grid layout
 * 
 * @param props - Component props
 * @returns JSX element containing tag filter buttons
 * 
 * @example
 * ```tsx
 * function SearchForm() {
 *   const [selectedTags, setSelectedTags] = useState<number[]>([]);
 *   
 *   return (
 *     <form>
 *       <TagFilter 
 *         selectedTags={selectedTags} 
 *         onTagChange={setSelectedTags} 
 *       />
 *     </form>
 *   );
 * }
 * ```
 * 
 * @todo Replace hardcoded tags with API data from /v1/tags/
 */
export default function TagFilter({ selectedTags, onTagChange }: TagFilterProps) {
  // TODO: Replace with actual tag data from API
  const tags: string[] = ['tag1', 'tag2', 'tag3']; // Example tags

  /**
   * Handle tag button click - toggle selection
   * 
   * @param tag - Tag name to toggle
   */
  const handleTagClick = (tag: string): void => {
    const tagIndex = tags.indexOf(tag);
    if (selectedTags.includes(tagIndex)) {
      onTagChange(selectedTags.filter((t) => t !== tagIndex));
    } else {
      onTagChange([...selectedTags, tagIndex]);
    }
  };

  return (
    <div className="flex flex-wrap gap-2">
      {tags.map((tag, index) => (
        <button
          key={tag}
          type="button"
          onClick={() => handleTagClick(tag)}
          className={`px-3 py-1 rounded-full text-sm ${
            selectedTags.includes(index)
              ? 'bg-blue-500 text-white'
              : 'bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
          }`}
        >
          {tag}
        </button>
      ))}
    </div>
  );
}
