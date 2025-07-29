import { useState, useEffect, ReactNode } from 'react';
import { useLocation } from 'react-router-dom';
import SearchBar from './SearchBar';
import AuthModal from './AuthModal';

interface Props {
  children: ReactNode;
}

export default function Layout({ children }: Props) {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(!!localStorage.getItem('token'));
  const [accountOpen, setAccountOpen] = useState(false);
  const location = useLocation();
  
  const isHomePage = location.pathname === '/';

  useEffect(() => {
    const id = setInterval(() => setIsLoggedIn(!!localStorage.getItem('token')), 1000);
    return () => clearInterval(id);
  }, []);

  return (
    <div className="min-h-screen w-full flex flex-col bg-background text-foreground">
      <SearchBar 
        isLoggedIn={isLoggedIn} 
        onAccountClick={() => setAccountOpen(true)}
        onSearch={isHomePage ? (window as any).homeSearchHandler : undefined}
      />
      
      {accountOpen && (
        <AuthModal 
          onClose={() => setAccountOpen(false)} 
          onSuccess={() => setIsLoggedIn(true)} 
        />
      )}
      
      <main className="flex-1 pt-24 max-w-screen-2xl mx-auto w-full px-4">
        {children}
      </main>
    </div>
  );
}
