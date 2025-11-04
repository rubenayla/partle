/**
 * @fileoverview StarRating component for displaying star ratings
 * @module components/StarRating
 */

import type { FC } from 'react';
import { Star } from 'lucide-react';

interface StarRatingProps {
  /** Rating value (0-5) */
  rating: number;
  /** Maximum number of stars (default: 5) */
  maxStars?: number;
  /** Size of stars in pixels (default: 16) */
  size?: number;
  /** Show rating number next to stars (default: false) */
  showNumber?: boolean;
  /** Additional CSS classes */
  className?: string;
  /** Label to show before the rating */
  label?: string;
}

/**
 * Display a star rating (read-only)
 *
 * @example
 * <StarRating rating={4.5} showNumber />
 * <StarRating rating={3} label="Quality:" />
 */
const StarRating: FC<StarRatingProps> = ({
  rating,
  maxStars = 5,
  size = 16,
  showNumber = false,
  className = '',
  label,
}) => {
  const stars = [];
  const roundedRating = Math.round(rating * 2) / 2; // Round to nearest 0.5

  for (let i = 1; i <= maxStars; i++) {
    const fillPercentage = Math.min(Math.max(roundedRating - (i - 1), 0), 1);

    stars.push(
      <div key={i} className="relative inline-block" style={{ width: size, height: size }}>
        {/* Background (empty) star */}
        <Star
          size={size}
          className="absolute text-gray-300 dark:text-gray-600"
          fill="currentColor"
        />
        {/* Foreground (filled) star - clipped to fillPercentage */}
        <div
          className="absolute overflow-hidden"
          style={{ width: `${fillPercentage * 100}%` }}
        >
          <Star
            size={size}
            className="text-yellow-400"
            fill="currentColor"
          />
        </div>
      </div>
    );
  }

  return (
    <div className={`flex items-center gap-1 ${className}`}>
      {label && <span className="text-sm text-secondary mr-1">{label}</span>}
      <div className="flex items-center gap-0.5">
        {stars}
      </div>
      {showNumber && (
        <span className="text-sm text-secondary ml-1">
          {rating.toFixed(1)}
        </span>
      )}
    </div>
  );
};

export default StarRating;
