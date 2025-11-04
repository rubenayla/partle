/**
 * @fileoverview ProductReviewCard component for displaying product reviews
 * @module components/ProductReviewCard
 */

import type { FC } from 'react';
import type { ProductReview } from '../types';
import StarRating from './StarRating';
import { User, Calendar, Edit, Trash2 } from 'lucide-react';

interface ProductReviewCardProps {
  /** Review data to display */
  review: ProductReview;
  /** Whether the current user owns this review */
  isOwner?: boolean;
  /** Callback when edit button is clicked */
  onEdit?: (review: ProductReview) => void;
  /** Callback when delete button is clicked */
  onDelete?: (reviewId: number) => void;
  /** Additional CSS classes */
  className?: string;
}

/**
 * Display a product review with ratings and comment
 *
 * @example
 * <ProductReviewCard
 *   review={review}
 *   isOwner={currentUser?.id === review.user_id}
 *   onEdit={handleEdit}
 *   onDelete={handleDelete}
 * />
 */
const ProductReviewCard: FC<ProductReviewCardProps> = ({
  review,
  isOwner = false,
  onEdit,
  onDelete,
  className = '',
}) => {
  const displayName = review.user?.username || review.user?.email?.split('@')[0] || 'Anonymous';
  const reviewDate = new Date(review.created_at).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  const isEdited = review.updated_at !== review.created_at;

  return (
    <div className={`bg-surface rounded-lg border border-gray-300 dark:border-gray-600 p-4 ${className}`}>
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
            <User className="h-4 w-4 text-gray-600 dark:text-gray-400" />
          </div>
          <div>
            <p className="font-medium text-foreground">{displayName}</p>
            <div className="flex items-center gap-1 text-xs text-secondary">
              <Calendar className="h-3 w-3" />
              <span>{reviewDate}</span>
              {isEdited && <span className="text-gray-400">(edited)</span>}
            </div>
          </div>
        </div>

        {/* Action buttons for owner */}
        {isOwner && (
          <div className="flex items-center gap-2">
            {onEdit && (
              <button
                onClick={() => onEdit(review)}
                className="p-1 text-secondary hover:text-foreground transition-colors"
                title="Edit review"
              >
                <Edit className="h-4 w-4" />
              </button>
            )}
            {onDelete && (
              <button
                onClick={() => onDelete(review.id)}
                className="p-1 text-secondary hover:text-red-600 transition-colors"
                title="Delete review"
              >
                <Trash2 className="h-4 w-4" />
              </button>
            )}
          </div>
        )}
      </div>

      {/* Ratings */}
      <div className="space-y-2 mb-3">
        <StarRating
          rating={review.product_rating}
          label="Product Quality:"
          showNumber
          size={16}
        />
        <StarRating
          rating={review.info_rating}
          label="Info Accuracy:"
          showNumber
          size={16}
        />
      </div>

      {/* Comment */}
      {review.comment && (
        <p className="text-foreground text-sm leading-relaxed whitespace-pre-wrap">
          {review.comment}
        </p>
      )}

      {/* Helpful count (if > 0) */}
      {review.helpful_count > 0 && (
        <div className="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
          <p className="text-xs text-secondary">
            {review.helpful_count} {review.helpful_count === 1 ? 'person' : 'people'} found this helpful
          </p>
        </div>
      )}
    </div>
  );
};

export default ProductReviewCard;
