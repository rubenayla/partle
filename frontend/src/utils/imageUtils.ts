/**
 * @fileoverview Image utility functions for handling product images
 * @module utils/imageUtils
 */

import { Product } from '../types';

/**
 * Get the appropriate image source URL for a product
 * Returns API endpoint for database-stored images
 * 
 * @param product - Product object
 * @returns Image URL or null if no image available
 */
export function getProductImageSrc(product: Product): string | null {
  // If product has image data stored in database, use API endpoint
  if (product.image_filename && product.image_content_type) {
    const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:8001';
    return `${apiBase}/v1/products/${product.id}/image`;
  }
  
  return null;
}

/**
 * Check if a product has any image available
 * 
 * @param product - Product object
 * @returns true if product has image data
 */
export function hasProductImage(product: Product): boolean {
  return !!product.image_filename;
}