import { useState, useEffect, ReactNode } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import SearchBar from './SearchBar';
import AuthModal from './AuthModal';
import type { ProductSearchParams } from '../types';

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
  const navigate = useNavigate();

  const isHomePage = location.pathname === '/';

  useEffect(() => {
    const id = setInterval(() => setIsLoggedIn(!!localStorage.getItem('token')), 1000);
    return () => clearInterval(id);
  }, []);

  // Listen for custom event to open auth modal
  useEffect(() => {
    const handleOpenAuthModal = () => setAccountOpen(true);
    window.addEventListener('openAuthModal', handleOpenAuthModal);
    return () => window.removeEventListener('openAuthModal', handleOpenAuthModal);
  }, []);

  const handleSearch = (params: ProductSearchParams) => {
    // Build URL search params
    const searchParams = new URLSearchParams();

    if (params.query) searchParams.set('q', params.query);
    if (params.searchType !== 'products') searchParams.set('type', params.searchType);
    if (params.priceMin > 0) searchParams.set('minPrice', params.priceMin.toString());
    if (params.priceMax !== 500) searchParams.set('maxPrice', params.priceMax.toString());
    if (params.selectedTags?.length) searchParams.set('tags', params.selectedTags.join(','));
    if (params.selectedStores?.length) searchParams.set('stores', params.selectedStores.join(','));
    if (params.sortBy && params.sortBy !== 'created_at') searchParams.set('sort', params.sortBy);
    if (params.userLat) searchParams.set('lat', params.userLat.toString());
    if (params.userLon) searchParams.set('lon', params.userLon.toString());

    const queryString = searchParams.toString();
    const newPath = queryString ? `/?${queryString}` : '/';

    if (isHomePage) {
      // On home page, update URL and trigger search
      navigate(newPath, { replace: true });
      if ((window as any).homeSearchHandler) {
        (window as any).homeSearchHandler(params);
      }
    } else {
      // On any other page, navigate to home with search params
      navigate(newPath);
    }
  };

  return (
    <div className="min-h-screen w-full bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
      <SearchBar
        isLoggedIn={isLoggedIn}
        onAccountClick={() => setAccountOpen(true)}
        onSearch={handleSearch}
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
