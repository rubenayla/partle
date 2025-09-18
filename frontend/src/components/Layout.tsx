import { useState, useEffect, ReactNode } from 'react';
import { useLocation } from 'react-router-dom';
import SearchBar from './SearchBar';
import AuthModal from './AuthModal';

interface Props {
  children: ReactNode;
  setTheme: (theme: 'light' | 'dark' | 'system') => void;
  currentTheme: 'light' | 'dark' | 'system';
}

/**
 * Layout Component - Global page wrapper
 * 
 * IMPORTANT: This component should only be used ONCE at the App level.
 * Individual pages should NOT import or wrap themselves with Layout.
 * 
 * Responsibilities:
 * - Provides fixed SearchBar (top on desktop, bottom on mobile)
 * - Handles global auth modals and state
 * - Manages consistent spacing to clear fixed SearchBar
 * - Contains max-w-width container and horizontal padding for all pages
 * 
 * Usage:
 * - App.tsx wraps the entire Router with <Layout>
 * - Page components are rendered as {children} inside Layout's <main>
 * - Pages should never use Layout directly - they're already inside it
 */
export default function Layout({ children, setTheme, currentTheme }: Props) {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(!!localStorage.getItem('token'));
  const [accountOpen, setAccountOpen] = useState(false);
  const location = useLocation();

  const isHomePage = location.pathname === '/';

  useEffect(() => {
    const id = setInterval(() => setIsLoggedIn(!!localStorage.getItem('token')), 1000);
    return () => clearInterval(id);
  }, []);

  return (
    <div className="min-h-screen w-full bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
      <SearchBar
        isLoggedIn={isLoggedIn}
        onAccountClick={() => setAccountOpen(true)}
        onSearch={isHomePage ? (params: any) => {
          if ((window as any).homeSearchHandler) {
            (window as any).homeSearchHandler(params);
          }
        } : undefined}
        currentTheme={currentTheme}
        setTheme={setTheme}
      />

      {accountOpen && (
        <AuthModal
          onClose={() => setAccountOpen(false)}
          onSuccess={() => setIsLoggedIn(true)}
        />
      )}

      {/* Main content area with spacing to clear fixed SearchBar */}
      <main className="mt-0 sm:mt-[72px] pt-16 sm:pt-6 pb-[140px] sm:pb-6 max-w-screen-2xl mx-auto w-full px-4">
        {children}
      </main>
    </div>
  );
}
