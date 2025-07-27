import { useState, useEffect, ReactNode } from 'react';
import SearchBar from './SearchBar';
import AuthModal from './AuthModal';

interface Props {
  children: ReactNode;
}

export default function Layout({ children }: Props) {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(!!localStorage.getItem('token'));
  const [accountOpen, setAccountOpen] = useState(false);

  useEffect(() => {
    const id = setInterval(() => setIsLoggedIn(!!localStorage.getItem('token')), 1000);
    return () => clearInterval(id);
  }, []);

  return (
    <div className="min-h-screen w-screen flex flex-col bg-background text-foreground">
      <SearchBar isLoggedIn={isLoggedIn} onAccountClick={() => setAccountOpen(true)} />
      {accountOpen && (
        <AuthModal onClose={() => setAccountOpen(false)} onSuccess={() => setIsLoggedIn(true)} />
      )}
      <main className="flex-1 pt-[96px]">{children}</main>
    </div>
  );
}
