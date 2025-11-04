/**
 * @fileoverview ReviewsSection component for displaying product reviews
 * @module components/ReviewsSection
 */

import type { FC } from 'react';
import { useState, useEffect } from 'react';
import type { ProductReview, ProductReviewInput, ProductRatingSummary } from '../types';
import { useAuth } from '../hooks/useAuth';
import StarRating from './StarRating';
import ProductReviewCard from './ProductReviewCard';
import ProductReviewForm from './ProductReviewForm';
import { MessageSquare, AlertCircle } from 'lucide-react';

interface ReviewsSectionProps {
  /** Product ID to show reviews for */
  productId: number;
  /** Additional CSS classes */
  className?: string;
}

/**
 * Complete reviews section with ratings summary, review list, and review form
 *
 * @example
 * <ReviewsSection productId={product.id} />
 */
const ReviewsSection: FC<ReviewsSectionProps> = ({ productId, className = '' }) => {
  const { user } = useAuth();
  const [reviews, setReviews] = useState<ProductReview[]>([]);
  const [ratingSummary, setRatingSummary] = useState<ProductRatingSummary | null>(null);
  const [myReview, setMyReview] = useState<ProductReview | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showForm, setShowForm] = useState(false);
  const [error, setError] = useState<string>('');

  const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

  // Fetch reviews and rating summary
  useEffect(() => {
    const fetchReviews = async () => {
      setIsLoading(true);
      setError('');

      try {
        // Fetch reviews
        const reviewsRes = await fetch(`${API_BASE}/v1/products/${productId}/reviews`);
        if (!reviewsRes.ok) throw new Error('Failed to fetch reviews');
        const reviewsData = await reviewsRes.json();
        setReviews(reviewsData);

        // Fetch rating summary
        const summaryRes = await fetch(`${API_BASE}/v1/products/${productId}/ratings`);
        if (!summaryRes.ok) throw new Error('Failed to fetch rating summary');
        const summaryData = await summaryRes.json();
        setRatingSummary(summaryData);

        // Fetch user's own review if logged in
        if (user) {
          const myReviewRes = await fetch(`${API_BASE}/v1/products/${productId}/reviews/my`, {
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`,
            },
          });
          if (myReviewRes.ok) {
            const myReviewData = await myReviewRes.json();
            setMyReview(myReviewData);
          }
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load reviews');
      } finally {
        setIsLoading(false);
      }
    };

    fetchReviews();
  }, [productId, user, API_BASE]);

  const handleSubmitReview = async (reviewData: ProductReviewInput) => {
    setIsSubmitting(true);
    setError('');

    try {
      const token = localStorage.getItem('token');
      if (!token) throw new Error('Please log in to submit a review');

      const method = myReview ? 'PUT' : 'POST';
      const url = myReview
        ? `${API_BASE}/v1/products/${productId}/reviews/${myReview.id}`
        : `${API_BASE}/v1/products/${productId}/reviews`;

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify(reviewData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to submit review');
      }

      const newReview = await response.json();

      // Update state
      setMyReview(newReview);
      setShowForm(false);

      // Refresh reviews list
      const reviewsRes = await fetch(`${API_BASE}/v1/products/${productId}/reviews`);
      if (reviewsRes.ok) {
        const reviewsData = await reviewsRes.json();
        setReviews(reviewsData);
      }

      // Refresh rating summary
      const summaryRes = await fetch(`${API_BASE}/v1/products/${productId}/ratings`);
      if (summaryRes.ok) {
        const summaryData = await summaryRes.json();
        setRatingSummary(summaryData);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to submit review');
      throw err; // Re-throw to let form handle it
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleDeleteReview = async (reviewId: number) => {
    if (!confirm('Are you sure you want to delete your review?')) return;

    try {
      const token = localStorage.getItem('token');
      if (!token) throw new Error('Please log in to delete a review');

      const response = await fetch(
        `${API_BASE}/v1/products/${productId}/reviews/${reviewId}`,
        {
          method: 'DELETE',
          headers: {
            'Authorization': `Bearer ${token}`,
          },
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to delete review');
      }

      // Update state
      setMyReview(null);
      setReviews(reviews.filter((r) => r.id !== reviewId));

      // Refresh rating summary
      const summaryRes = await fetch(`${API_BASE}/v1/products/${productId}/ratings`);
      if (summaryRes.ok) {
        const summaryData = await summaryRes.json();
        setRatingSummary(summaryData);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete review');
    }
  };

  if (isLoading) {
    return (
      <div className={`animate-pulse ${className}`}>
        <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/3 mb-4"></div>
        <div className="h-32 bg-gray-200 dark:bg-gray-700 rounded mb-4"></div>
        <div className="h-48 bg-gray-200 dark:bg-gray-700 rounded"></div>
      </div>
    );
  }

  const hasReviews = reviews.length > 0;

  return (
    <div className={className}>
      <h2 className="text-2xl font-bold text-foreground mb-4 flex items-center gap-2">
        <MessageSquare className="h-6 w-6" />
        Reviews & Ratings
      </h2>

      {error && (
        <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg flex items-start gap-2">
          <AlertCircle className="h-5 w-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
          <p className="text-red-600 dark:text-red-400 text-sm">{error}</p>
        </div>
      )}

      {/* Rating Summary */}
      {ratingSummary && hasReviews && (
        <div className="bg-surface rounded-lg border border-gray-300 dark:border-gray-600 p-4 mb-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <p className="text-sm text-secondary mb-2">Overall Ratings</p>
              <StarRating
                rating={ratingSummary.average_product_rating || 0}
                label="Product Quality:"
                showNumber
                size={20}
                className="mb-2"
              />
              <StarRating
                rating={ratingSummary.average_info_rating || 0}
                label="Info Accuracy:"
                showNumber
                size={20}
              />
            </div>
            <div className="text-right md:text-left">
              <p className="text-3xl font-bold text-foreground">
                {ratingSummary.total_reviews}
              </p>
              <p className="text-sm text-secondary">
                {ratingSummary.total_reviews === 1 ? 'Review' : 'Reviews'}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Write Review Button / Form */}
      {user && !myReview && !showForm && (
        <button
          onClick={() => setShowForm(true)}
          className="mb-6 w-full md:w-auto px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
        >
          Write a Review
        </button>
      )}

      {showForm && user && (
        <ProductReviewForm
          existingReview={myReview}
          onSubmit={handleSubmitReview}
          onCancel={() => setShowForm(false)}
          isSubmitting={isSubmitting}
          className="mb-6"
        />
      )}

      {/* User's Own Review (if exists and not editing) */}
      {myReview && !showForm && (
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-foreground mb-3">Your Review</h3>
          <ProductReviewCard
            review={myReview}
            isOwner={true}
            onEdit={() => setShowForm(true)}
            onDelete={handleDeleteReview}
          />
        </div>
      )}

      {/* Other Reviews */}
      {hasReviews && (
        <div>
          <h3 className="text-lg font-semibold text-foreground mb-3">
            {myReview ? 'Other Reviews' : 'Customer Reviews'}
          </h3>
          <div className="space-y-4">
            {reviews
              .filter((review) => review.id !== myReview?.id)
              .map((review) => (
                <ProductReviewCard key={review.id} review={review} />
              ))}
          </div>
        </div>
      )}

      {/* No Reviews Message */}
      {!hasReviews && (
        <div className="text-center py-12 bg-surface rounded-lg border border-gray-300 dark:border-gray-600">
          <MessageSquare className="h-12 w-12 text-gray-400 mx-auto mb-3" />
          <p className="text-secondary text-lg mb-2">No reviews yet</p>
          <p className="text-secondary text-sm">Be the first to review this product!</p>
        </div>
      )}

      {/* Login Prompt */}
      {!user && (
        <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg text-center">
          <p className="text-sm text-foreground">
            Please{' '}
            <button
              onClick={() => {
                // Dispatch custom event to open auth modal
                window.dispatchEvent(new CustomEvent('openAuthModal'));
              }}
              className="text-blue-600 hover:underline cursor-pointer font-medium"
            >
              log in
            </button>{' '}
            to write a review
          </p>
        </div>
      )}
    </div>
  );
};

export default ReviewsSection;
