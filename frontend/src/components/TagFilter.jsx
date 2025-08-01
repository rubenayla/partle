import React from 'react';

export default function TagFilter({ selectedTags, onTagChange }) {
  const tags = ['tag1', 'tag2', 'tag3']; // Example tags

  const handleTagClick = (tag) => {
    if (selectedTags.includes(tag)) {
      onTagChange(selectedTags.filter((t) => t !== tag));
    } else {
      onTagChange([...selectedTags, tag]);
    }
  };

  return (
    <div className="flex flex-wrap gap-2">
      {tags.map((tag) => (
        <button
          key={tag}
          type="button"
          onClick={() => handleTagClick(tag)}
          className={`px-3 py-1 rounded-full text-sm ${
            selectedTags.includes(tag) ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
          }`}
        >
          {tag}
        </button>
      ))}
    </div>
  );
}
