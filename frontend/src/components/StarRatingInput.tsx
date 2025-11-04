/**
 * @fileoverview StarRatingInput component for user rating input
 * @module components/StarRatingInput
 */

import type { FC } from 'react';
import { useState } from 'react';
import { Star } from 'lucide-react';

interface StarRatingInputProps {
  /** Current rating value (1-5) */
  value: number;
  /** Callback when rating changes */
  onChange: (rating: number) => void;
  /** Label to show above the stars */
  label: string;
  /** Maximum number of stars (default: 5) */
  maxStars?: number;
  /** Size of stars in pixels (default: 24) */
  size?: number;
  /** Whether the input is disabled */
  disabled?: boolean;
  /** Additional CSS classes */
  className?: string;
  /** Required field indicator */
  required?: boolean;
}

/**
 * Interactive star rating input component
 *
 * @example
 * <StarRatingInput
 *   label="Product Quality"
 *   value={rating}
 *   onChange={setRating}
 *   required
 * />
 */
const StarRatingInput: FC<StarRatingInputProps> = ({
  value,
  onChange,
  label,
  maxStars = 5,
  size = 24,
  disabled = false,
  className = '',
  required = false,
}) => {
  const [hoveredStar, setHoveredStar] = useState<number | null>(null);

  const handleClick = (rating: number) => {
    if (!disabled) {
      onChange(rating);
    }
  };

  const displayRating = hoveredStar !== null ? hoveredStar : value;

  return (
    <div className={className}>
      <label className="block text-sm font-medium text-foreground mb-2">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      <div className="flex items-center gap-1">
        {Array.from({ length: maxStars }, (_, i) => {
          const starValue = i + 1;
          const isFilled = starValue <= displayRating;

          return (
            <button
              key={starValue}
              type="button"
              onClick={() => handleClick(starValue)}
              onMouseEnter={() => !disabled && setHoveredStar(starValue)}
              onMouseLeave={() => setHoveredStar(null)}
              disabled={disabled}
              className={`transition-transform ${
                disabled ? 'cursor-not-allowed opacity-50' : 'cursor-pointer hover:scale-110'
              }`}
              aria-label={`Rate ${starValue} out of ${maxStars} stars`}
            >
              <Star
                size={size}
                className={`transition-colors ${
                  isFilled
                    ? 'text-yellow-400'
                    : 'text-gray-300 dark:text-gray-600'
                }`}
                fill={isFilled ? 'currentColor' : 'none'}
              />
            </button>
          );
        })}
        {value > 0 && (
          <span className="ml-2 text-sm text-secondary">
            {value} / {maxStars}
          </span>
        )}
      </div>
    </div>
  );
};

export default StarRatingInput;
