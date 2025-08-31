/**
 * @fileoverview Authentication hook and context provider for managing user state
 * @module hooks/useAuth
 */
import { useState, useEffect, createContext, useContext, ReactNode } from 'react';
import { currentUser, login, register } from '../api/auth';
import { User, AuthContextValue } from '../types';

/** Authentication context with default null value */
const AuthCtx = createContext<AuthContextValue | null>(null);

/**
 * Props for the AuthProvider component
 */
interface AuthProviderProps {
  /** Child components to wrap with auth context */
  children: ReactNode;
}

/**
 * Authentication Provider Component
 * 
 * Provides authentication context to the entire application tree.
 * Handles initial authentication state loading from localStorage token.
 * 
 * @param props - Component props
 * @returns JSX element wrapping children with auth context
 * 
 * @example
 * ```tsx
 * function App() {
 *   return (
 *     <AuthProvider>
 *       <Router>
 *         <Routes>...
 *         </Routes>
 *       </Router>
 *     </AuthProvider>
 *   );
 * }
 * ```
 */
export const AuthProvider = ({ children }: AuthProviderProps) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  useEffect(() => {
    // Initializing auth state
    const token = localStorage.getItem('token');
    if (!token) {
      // No token found, user not logged in
      setUser(null);
      setIsLoading(false);
      return;
    }

    console.log('AuthProvider: Token found, checking current user');
    currentUser()
      .then((userData: User) => {
        console.log('AuthProvider: User logged in:', userData?.email);
        setUser(userData);
      })
      .catch((error: any) => {
        console.log('AuthProvider: Token invalid, removing:', error.response?.status);
        localStorage.removeItem('token');
        setUser(null);
      })
      .finally(() => {
        console.log('AuthProvider: Auth initialization complete');
        setIsLoading(false);
      });
  }, []);

  /**
   * Sign in a user with email and password
   * 
   * @param email - User's email address
   * @param password - User's password
   * @throws {Error} When login fails
   */
  const signIn = async (email: string, password: string): Promise<void> => {
    await login(email, password);
    const u = await currentUser();
    setUser(u);
  };

  /**
   * Log out the current user
   * Removes token from localStorage and clears user state
   */
  const logout = (): void => {
    localStorage.removeItem('token');
    setUser(null);
  };

  const value: AuthContextValue = {
    user,
    isLoading,
    login: signIn,
    logout,
    register
  };

  return <AuthCtx.Provider value={value}>{children}</AuthCtx.Provider>;
};

/**
 * Authentication Hook
 * 
 * Provides access to authentication context throughout the application.
 * Must be used within an AuthProvider.
 * 
 * @returns Authentication context value
 * @throws {Error} When used outside of AuthProvider
 * 
 * @example
 * ```tsx
 * function UserProfile() {
 *   const { user, isLoading, logout } = useAuth();
 *   
 *   if (isLoading) return <div>Loading...</div>;
 *   if (!user) return <div>Please log in</div>;
 *   
 *   return (
 *     <div>
 *       <h1>Welcome, {user.email}</h1>
 *       <button onClick={logout}>Logout</button>
 *     </div>
 *   );
 * }
 * ```
 */
export const useAuth = (): AuthContextValue => {
  const context = useContext(AuthCtx);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
