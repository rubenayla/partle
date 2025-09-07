// frontend/src/App.tsx
import { BrowserRouter, Routes, Route, Navigate, useLocation } from "react-router-dom";
import { useEffect } from "react";
import RequireAuth from "./components/RequireAuth"; // only for actions like adding
import Home from "./pages/Home"; // new home page
import Stores from "./pages/Stores";
import Products from "./pages/Products";
import AddProduct from "./pages/AddProduct";
import AddStore from "./pages/AddStore";
import ProductDetail from "./pages/ProductDetail";
import Contact from "./pages/Contact"; // Import the new Contact page
import Terms from "./pages/Terms"; // Import the new Terms page
import Privacy from "./pages/Privacy"; // Import the new Privacy page
import About from "./pages/About"; // Import the new About page
import Documentation from "./pages/Documentation"; // Import the new Documentation page
import Account from "./pages/Account"; // Import the new Account page
import ResetPassword from "./pages/ResetPassword"; // Import the new ResetPassword page
import CompleteProfile from "./pages/CompleteProfile"; // Import the new CompleteProfile page
import MyProducts from "./pages/MyProducts"; // Import the new MyProducts page
import { useBackendStatus } from './hooks/useBackendStatus'
import { useTheme } from './hooks/useTheme';
import { trackPageView } from './utils/analytics';

import Layout from "./components/Layout";

function PageTracker() {
  const location = useLocation();
  
  useEffect(() => {
    trackPageView(location.pathname);
  }, [location]);
  
  return null;
}

export default function App() {
  const status = useBackendStatus()
  const [theme, setTheme] = useTheme();

  if (status === 'checking') {
    return <div className='p-8 text-center'>Checking backend status...</div>
  }

  if (status === 'offline') {
    return (
      <div className='flex h-screen items-center justify-center bg-gray-100 dark:bg-gray-900'>
        <div className='text-center'>
          <h1 className='text-2xl font-bold text-gray-900 dark:text-white'>⚠️ Backend offline</h1>
          <p className='mt-2 text-gray-600 dark:text-gray-300'>We're doing maintenance or sleeping. Please try again later.</p>
        </div>
      </div>
    )
  }

  return (
    <BrowserRouter>
      <PageTracker />
      {/* Global Layout wrapper - provides SearchBar, spacing, and container for ALL pages */}
      <Layout setTheme={setTheme} currentTheme={theme}>
        <Routes>
          {/* public routes */}
          <Route path="/" element={<Home />} />
          <Route path="/stores" element={<Stores />} />
          <Route path="/stores/:id/products" element={<Products />} />
          <Route path="/products/:id" element={<ProductDetail />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/terms" element={<Terms />} />
          <Route path="/privacy" element={<Privacy />} />
          <Route path="/about" element={<About />} />
          <Route path="/documentation" element={<Documentation />} />
          <Route path="/reset-password" element={<ResetPassword />} />
          <Route path="/complete-profile" element={<CompleteProfile />} />

          {/* actions that require login */}
          <Route element={<RequireAuth />}>
            <Route path="/products/new" element={<AddProduct />} />
            <Route path="/products/my" element={<MyProducts />} />
            <Route path="/stores/new" element={<AddStore />} />
            <Route path="/account" element={<Account />} />
          </Route>

          {/* catch-all → go to home */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}

