import { useState, useEffect } from 'react';
import axios from 'axios';

export default function TagFilter({ selectedTags, onTagChange }) {
  const [tags, setTags] = useState([]);

  useEffect(() => {
    const fetchTags = async () => {
      try {
        const response = await axios.get('/api/v1/tags');
        setTags(response.data);
      } catch (error) {
        console.error('Error fetching tags:', error);
      }
    };
    fetchTags();
  }, []);

  const handleTagClick = (tagId) => {
    const newSelectedTags = selectedTags.includes(tagId)
      ? selectedTags.filter((id) => id !== tagId)
      : [...selectedTags, tagId];
    onTagChange(newSelectedTags);
  };

  return (
    <div className="space-y-2">
      <h3 className="text-sm font-semibold text-secondary">Tags</h3>
      <div className="flex flex-wrap gap-2">
        {tags.map((tag) => (
          <button
            key={tag.id}
            type="button"
            onClick={() => handleTagClick(tag.id)}
            className={`px-3 py-1 rounded-full text-sm ${selectedTags.includes(tag.id)
                ? 'bg-primary text-white'
                : 'bg-surface-hover text-foreground'}
            `}
          >
            {tag.name}
          </button>
        ))}
      </div>
    </div>
  );
}
