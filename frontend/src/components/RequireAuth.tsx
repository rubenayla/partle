/**
 * @fileoverview RequireAuth Component - Authentication guard for protected routes
 * @module components/RequireAuth
 */
import { useEffect, useState } from 'react';
import { Navigate, Outlet } from 'react-router-dom';
import api from '../api/index';

/**
 * RequireAuth Component - Protected route wrapper
 * 
 * Validates user authentication by checking for a valid token and verifying
 * it with the backend. Redirects unauthenticated users to the home page.
 * 
 * Features:
 * - Token validation on mount
 * - Automatic token cleanup on authentication failure
 * - Loading state during authentication check
 * - Redirect to home page for unauthenticated users
 * 
 * @returns JSX element - either the protected content or navigation redirect
 * 
 * @example
 * ```tsx
 * // Protect routes that require authentication
 * <Routes>
 *   <Route path="/" element={<Home />} />
 *   <Route path="/account" element={
 *     <RequireAuth>
 *       <Account />
 *     </RequireAuth>
 *   } />
 *   <Route path="/products/new" element={
 *     <RequireAuth>
 *       <AddProduct />
 *     </RequireAuth>
 *   } />
 * </Routes>
 * ```
 */
export default function RequireAuth() {
  const [allowed, setAllowed] = useState<boolean | null>(null);

  useEffect(() => {
    /**
     * Check user authentication status
     * Validates token existence and verifies with backend
     */
    async function check(): Promise<void> {
      const token = localStorage.getItem('token');
      if (!token) {
        setAllowed(false);
        return;
      }
      
      try {
        // Verify token with backend
        await api.get('/v1/auth/me');
        setAllowed(true);
      } catch {
        // Token is invalid, clean up and deny access
        localStorage.removeItem('token');
        setAllowed(false);
      }
    }
    
    check();
  }, []);

  // Still checking authentication - show nothing (or could show spinner)
  if (allowed === null) {
    return null;
  }
  
  // Show protected content or redirect to home
  return allowed ? <Outlet /> : <Navigate to="/" replace />;
}
