/**
 * Utility functions for product display
 */

import { Product } from '../types';

/**
 * Get the display identifier for a product (SKU if available, otherwise #ID)
 * @param product - The product object
 * @returns The formatted identifier string
 */
export function getProductIdentifier(product: Product): string {
  if (product.sku) {
    return product.sku;
  }
  return `#${product.id}`;
}

/**
 * Get a formatted product identifier with label
 * @param product - The product object
 * @returns The formatted identifier with appropriate label
 */
export function getProductIdentifierWithLabel(product: Product): string {
  if (product.sku) {
    return `SKU: ${product.sku}`;
  }
  return `ID: #${product.id}`;
}

/**
 * Check if product has a custom SKU
 * @param product - The product object
 * @returns True if product has a custom SKU
 */
export function hasCustomSKU(product: Product): boolean {
  return !!product.sku;
}