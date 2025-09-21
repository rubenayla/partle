/**
 * Utility helper functions for the application
 */

/**
 * Get the image source URL for a product
 * @param productId The ID of the product
 * @param imageUrl Optional external image URL
 * @returns The image source URL or null if no image available
 */
export function getProductImageSrc(productId: number, imageUrl?: string | null): string | null {
  // First check if there's an external image URL
  if (imageUrl) {
    return imageUrl;
  }

  // Otherwise, check if there's a stored image in the database
  // The backend serves product images from this endpoint
  const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:8000';
  return `${apiBase}/v1/products/${productId}/image`;
}

/**
 * Format a date string to a readable format
 * @param dateString ISO date string
 * @returns Formatted date string
 */
export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

/**
 * Format a price with currency
 * @param price The price value
 * @param currency The currency symbol or code
 * @returns Formatted price string
 */
export function formatPrice(price: number | null, currency: string | null): string {
  if (price === null) {
    return 'Price not available';
  }
  return `${price} ${currency || '€'}`;
}

/**
 * Truncate text to a maximum length
 * @param text The text to truncate
 * @param maxLength Maximum length
 * @returns Truncated text with ellipsis if needed
 */
export function truncate(text: string, maxLength: number): string {
  if (text.length <= maxLength) {
    return text;
  }
  return text.substring(0, maxLength - 3) + '...';
}