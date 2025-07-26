// frontend/src/App.tsx
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import RequireAuth from "./components/RequireAuth"; // only for actions like adding
import Home from "./pages/Home"; // new home page
import Stores from "./pages/Stores";
import Products from "./pages/Products";
import AddProduct from "./pages/AddProduct";
import AddStore from "./pages/AddStore";
import ProductDetail from "./pages/ProductDetail";

import Layout from "./components/Layout";

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          {/* public routes */}
          <Route path="/" element={<Home />} />
          <Route path="/stores" element={<Stores />} />
          <Route path="/stores/:id/products" element={<Products />} />
          <Route path="/products/:id" element={<ProductDetail />} />

          {/* actions that require login */}
          <Route element={<RequireAuth />}>
            <Route path="/products/new" element={<AddProduct />} />
            <Route path="/stores/new" element={<AddStore />} />
          </Route>

          {/* catch-all → go to home */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}
