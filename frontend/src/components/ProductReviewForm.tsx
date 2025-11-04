/**
 * @fileoverview ProductReviewForm component for creating/editing reviews
 * @module components/ProductReviewForm
 */

import type { FC, FormEvent } from 'react';
import { useState, useEffect } from 'react';
import type { ProductReview, ProductReviewInput } from '../types';
import StarRatingInput from './StarRatingInput';

interface ProductReviewFormProps {
  /** Existing review to edit (optional) */
  existingReview?: ProductReview | null;
  /** Callback when form is submitted */
  onSubmit: (reviewData: ProductReviewInput) => Promise<void>;
  /** Callback when form is cancelled */
  onCancel?: () => void;
  /** Whether the form is submitting */
  isSubmitting?: boolean;
  /** Additional CSS classes */
  className?: string;
}

/**
 * Form for creating or editing a product review
 *
 * @example
 * <ProductReviewForm
 *   existingReview={myReview}
 *   onSubmit={handleSubmit}
 *   onCancel={handleCancel}
 * />
 */
const ProductReviewForm: FC<ProductReviewFormProps> = ({
  existingReview,
  onSubmit,
  onCancel,
  isSubmitting = false,
  className = '',
}) => {
  const [productRating, setProductRating] = useState<number>(existingReview?.product_rating || 0);
  const [infoRating, setInfoRating] = useState<number>(existingReview?.info_rating || 0);
  const [comment, setComment] = useState<string>(existingReview?.comment || '');
  const [error, setError] = useState<string>('');

  // Update form when existingReview changes
  useEffect(() => {
    if (existingReview) {
      setProductRating(existingReview.product_rating);
      setInfoRating(existingReview.info_rating);
      setComment(existingReview.comment || '');
    }
  }, [existingReview]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError('');

    // Validate ratings
    if (productRating === 0) {
      setError('Please provide a product quality rating');
      return;
    }

    if (infoRating === 0) {
      setError('Please provide an information accuracy rating');
      return;
    }

    try {
      await onSubmit({
        product_rating: productRating,
        info_rating: infoRating,
        comment: comment.trim() || undefined,
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to submit review');
    }
  };

  const isEditing = existingReview !== null && existingReview !== undefined;

  return (
    <form onSubmit={handleSubmit} className={`bg-surface rounded-lg border border-gray-300 dark:border-gray-600 p-4 ${className}`}>
      <h3 className="text-lg font-semibold text-foreground mb-4">
        {isEditing ? 'Edit Your Review' : 'Write a Review'}
      </h3>

      {error && (
        <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg text-red-600 dark:text-red-400 text-sm">
          {error}
        </div>
      )}

      <div className="space-y-4">
        {/* Product Rating */}
        <StarRatingInput
          label="Product Quality"
          value={productRating}
          onChange={setProductRating}
          disabled={isSubmitting}
          required
        />

        {/* Info Rating */}
        <StarRatingInput
          label="Information Accuracy (Price, Specs, etc.)"
          value={infoRating}
          onChange={setInfoRating}
          disabled={isSubmitting}
          required
        />

        {/* Comment */}
        <div>
          <label htmlFor="review-comment" className="block text-sm font-medium text-foreground mb-2">
            Your Review (Optional)
          </label>
          <textarea
            id="review-comment"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            disabled={isSubmitting}
            maxLength={5000}
            rows={5}
            placeholder="Share your experience with this product and the accuracy of its information..."
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-background text-foreground placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
          />
          <p className="mt-1 text-xs text-secondary">
            {comment.length} / 5000 characters
          </p>
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-2 pt-2">
          <button
            type="submit"
            disabled={isSubmitting || productRating === 0 || infoRating === 0}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isSubmitting ? 'Submitting...' : isEditing ? 'Update Review' : 'Submit Review'}
          </button>

          {onCancel && (
            <button
              type="button"
              onClick={onCancel}
              disabled={isSubmitting}
              className="px-4 py-2 bg-gray-200 dark:bg-gray-700 text-foreground rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              Cancel
            </button>
          )}
        </div>
      </div>
    </form>
  );
};

export default ProductReviewForm;
