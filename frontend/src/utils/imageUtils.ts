/**
 * @fileoverview Image utility functions for handling product images, store logos, and user profile pictures
 * @module utils/imageUtils
 */

import { Product, Store, User } from '../types';

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

/**
 * Get the appropriate image source URL for a store logo
 * Returns API endpoint for database-stored logos
 *
 * @param store - Store object
 * @returns Logo URL or null if no logo available
 */
export function getStoreLogoSrc(store: Store): string | null {
  // If store has logo data stored in database, use API endpoint
  if (store.logo_filename && store.logo_content_type) {
    const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:8001';
    return `${apiBase}/v1/stores/${store.id}/logo`;
  }

  return null;
}

/**
 * Check if a store has a logo available
 *
 * @param store - Store object
 * @returns true if store has logo data
 */
export function hasStoreLogo(store: Store): boolean {
  return !!store.logo_filename;
}

/**
 * Get the appropriate image source URL for a user profile picture
 * Returns API endpoint for database-stored profile pictures
 *
 * @param user - User object
 * @returns Profile picture URL or null if no picture available
 */
export function getUserProfilePictureSrc(user: User): string | null {
  // If user has profile picture data stored in database, use API endpoint
  if (user.profile_picture_filename && user.profile_picture_content_type) {
    const apiBase = import.meta.env.VITE_API_BASE || 'http://localhost:8001';
    return `${apiBase}/v1/auth/user/${user.id}/profile-picture`;
  }

  return null;
}

/**
 * Check if a user has a profile picture available
 *
 * @param user - User object
 * @returns true if user has profile picture data
 */
export function hasUserProfilePicture(user: User): boolean {
  return !!user.profile_picture_filename;
}