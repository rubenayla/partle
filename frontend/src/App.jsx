// frontend/src/App.jsx
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import RequireAuth from "./components/RequireAuth"; // only for actions like adding
import Home from "./pages/Home"; // new home page
import Stores from "./pages/Stores";
import Products from "./pages/Products";
import AddProduct from "./pages/AddProduct";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* public routes */}
        <Route path="/" element={<Home />} />
        <Route path="/stores" element={<Stores />} />
        <Route path="/stores/:id/products" element={<Products />} />

        {/* only adding/editing products requires login */}
        <Route element={<RequireAuth />}>
          <Route path="/products/new" element={<AddProduct />} />
        </Route>

        {/* catch-all → go to home */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
