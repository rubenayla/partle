// frontend/src/App.tsx
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
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
import Account from "./pages/Account"; // Import the new Account page
import ResetPassword from "./pages/ResetPassword"; // Import the new ResetPassword page
import { useBackendStatus } from './hooks/useBackendStatus'

import Layout from "./components/Layout";

export default function App() {
  const status = useBackendStatus()

  if (status === 'checking') {
    return <div className='p-8 text-center'>Checking backend status...</div>
  }

  if (status === 'offline') {
    return (
      <div className='flex h-screen items-center justify-center bg-gray-100'>
        <div className='text-center'>
          <h1 className='text-2xl font-bold'>⚠️ Backend offline</h1>
          <p className='mt-2 text-gray-600'>We're doing maintenance or sleeping. Please try again later.</p>
        </div>
      </div>
    )
  }

  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          {/* public routes */}
          <Route path="/" element={<Home />} />
          <Route path="/stores" element={<Stores />} />
          <Route path="/stores/:id/products" element={<Products />} />
          <Route path="/products/:id" element={<ProductDetail />} />
          <Route path="/contact" element={<Contact />} /> {/* Add the new route for Contact page */}
          <Route path="/terms" element={<Terms />} /> {/* Add the new route for Terms page */}
          <Route path="/privacy" element={<Privacy />} /> {/* Add the new route for Privacy page */}
          <Route path="/about" element={<About />} /> {/* Add the new route for About page */}
          <Route path="/reset-password" element={<ResetPassword />} /> {/* Add the new route for ResetPassword page */}

          {/* actions that require login */}
          <Route element={<RequireAuth />}>
            <Route path="/products/new" element={<AddProduct />} />
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

