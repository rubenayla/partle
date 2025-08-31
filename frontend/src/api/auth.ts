/**
 * @fileoverview Authentication API functions for user management
 * @module auth
 */

import { AxiosResponse } from 'axios';
import api from './index';

/**
 * Authentication token response from login endpoint
 */
interface LoginResponse {
  /** JWT access token for authenticated requests */
  access_token: string;
  /** Token type, typically "bearer" */
  token_type: string;
  /** Token expiration time in seconds */
  expires_in?: number;
}

/**
 * User registration request payload
 */
interface RegisterRequest {
  /** User's email address */
  email: string;
  /** User's password (will be hashed server-side) */
  password: string;
}

/**
 * User profile information returned from API
 */
interface User {
  /** Unique user identifier */
  id: number;
  /** User's email address */
  email: string;
  /** Whether the user's email has been verified */
  is_verified?: boolean;
  /** Timestamp when the user account was created */
  created_at?: string;
  /** Timestamp when the user account was last updated */
  updated_at?: string;
}

/**
 * Password change request payload
 */
interface ChangePasswordRequest {
  /** Current password for verification */
  current_password: string;
  /** New password to set */
  new_password: string;
}

/**
 * Password reset request payload
 */
interface PasswordResetRequest {
  /** Email address to send reset instructions to */
  email: string;
}

/**
 * Authenticates a user with email and password
 * 
 * Stores the received JWT token in localStorage for subsequent
 * authenticated requests. The token is automatically included
 * in API requests via the axios interceptor.
 * 
 * @example
 * ```tsx
 * try {
 *   const response = await login('user@example.com', 'password123');
 *   console.log('Login successful:', response.access_token);
 *   // Token is now stored and user is authenticated
 * } catch (error) {
 *   console.error('Login failed:', error.response?.data?.detail);
 * }
 * ```
 * 
 * @param email - User's email address
 * @param password - User's password
 * @returns Promise resolving to authentication response with token
 * @throws {Error} When login fails due to invalid credentials or server error
 */
export async function login(email: string, password: string): Promise<LoginResponse> {
  // FastAPI expects form-encoded data for OAuth2 login
  const body = new URLSearchParams({ 
    username: email, // OAuth2 standard uses 'username' field
    password 
  });
  
  const response: AxiosResponse<LoginResponse> = await api.post('/v1/auth/login', body, {
    headers: { 
      'Content-Type': 'application/x-www-form-urlencoded' 
    },
  });
  
  // Store JWT token for subsequent authenticated requests
  localStorage.setItem('token', response.data.access_token);
  
  return response.data;
}

/**
 * Registers a new user account
 * 
 * Creates a new user account with the provided email and password.
 * Password will be securely hashed on the server side.
 * 
 * @example
 * ```tsx
 * try {
 *   await register('newuser@example.com', 'securePassword123');
 *   console.log('Registration successful');
 * } catch (error) {
 *   console.error('Registration failed:', error.response?.data?.detail);
 * }
 * ```
 * 
 * @param email - New user's email address
 * @param password - New user's password (min 8 characters recommended)
 * @returns Promise that resolves when registration is complete
 * @throws {Error} When registration fails (email taken, invalid format, etc.)
 */
export async function register(email: string, password: string): Promise<AxiosResponse> {
  const payload: RegisterRequest = { email, password };
  return api.post('/v1/auth/register', payload);
}

/**
 * Requests a password reset for the given email address
 * 
 * Sends a password reset email to the user if the email exists in the system.
 * For security reasons, this endpoint typically returns success even for
 * non-existent emails to prevent email enumeration attacks.
 * 
 * @example
 * ```tsx
 * try {
 *   await requestReset('user@example.com');
 *   console.log('Reset email sent (if account exists)');
 * } catch (error) {
 *   console.error('Reset request failed:', error);
 * }
 * ```
 * 
 * @param email - Email address to send reset instructions to
 * @returns Promise that resolves when reset request is processed
 */
export async function requestReset(email: string): Promise<AxiosResponse> {
  const payload: PasswordResetRequest = { email };
  return api.post('/v1/auth/request-password-reset', payload);
}

/**
 * Fetches the current authenticated user's profile information
 * 
 * Requires a valid JWT token in localStorage. Returns user profile
 * data including email, verification status, and account timestamps.
 * 
 * @example
 * ```tsx
 * try {
 *   const user = await currentUser();
 *   console.log('Current user:', user.email);
 * } catch (error) {
 *   console.error('Not authenticated or session expired');
 *   // Redirect to login
 * }
 * ```
 * 
 * @returns Promise resolving to current user's profile data
 * @throws {Error} When user is not authenticated or token is invalid
 */
export async function currentUser(): Promise<User> {
  const response: AxiosResponse<User> = await api.get('/v1/auth/me');
  return response.data;
}

/**
 * Permanently deletes the current user's account
 * 
 * This is a destructive operation that cannot be undone. All user data
 * including products, stores, and preferences will be permanently removed.
 * 
 * @example
 * ```tsx
 * if (confirm('Are you sure? This cannot be undone.')) {
 *   try {
 *     await deleteAccount();
 *     console.log('Account deleted successfully');
 *     // Clear local storage and redirect to home
 *     localStorage.removeItem('token');
 *   } catch (error) {
 *     console.error('Failed to delete account:', error);
 *   }
 * }
 * ```
 * 
 * @returns Promise that resolves when account is deleted
 * @throws {Error} When deletion fails or user is not authenticated
 */
export async function deleteAccount(): Promise<AxiosResponse> {
  return api.delete('/v1/auth/account');
}

/**
 * Changes the current user's password
 * 
 * Requires the current password for verification before setting the new one.
 * This ensures account security even if someone gains temporary access
 * to a logged-in session.
 * 
 * @example
 * ```tsx
 * try {
 *   await changePassword('oldPassword123', 'newSecurePassword456');
 *   console.log('Password changed successfully');
 * } catch (error) {
 *   if (error.response?.status === 400) {
 *     console.error('Current password is incorrect');
 *   } else {
 *     console.error('Password change failed:', error);
 *   }
 * }
 * ```
 * 
 * @param currentPassword - Current password for verification
 * @param newPassword - New password to set
 * @returns Promise that resolves when password is changed
 * @throws {Error} When current password is wrong or change fails
 */
export async function changePassword(
  currentPassword: string, 
  newPassword: string
): Promise<AxiosResponse> {
  const payload: ChangePasswordRequest = {
    current_password: currentPassword,
    new_password: newPassword,
  };
  return api.post('/v1/auth/change-password', payload);
}