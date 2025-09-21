/**
 * @fileoverview Authentication utility functions
 * Provides helper functions for managing authentication tokens
 */

/**
 * Get the authentication token from localStorage
 * @returns The JWT token or null if not found
 */
export function getAuthToken(): string | null {
  return localStorage.getItem('token');
}

/**
 * Set the authentication token in localStorage
 * @param token - The JWT token to store
 */
export function setAuthToken(token: string): void {
  localStorage.setItem('token', token);
}

/**
 * Remove the authentication token from localStorage
 */
export function removeAuthToken(): void {
  localStorage.removeItem('token');
}

/**
 * Check if the user is authenticated
 * @returns True if a token exists, false otherwise
 */
export function isAuthenticated(): boolean {
  return !!getAuthToken();
}