// frontend/src/App.jsx
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import RequireAuth from "./components/RequireAuth";   // new guard component
import Login from "./pages/Login";                    // login form
import Stores from "./pages/Stores";                  // list + map view
import Products from "./pages/Products";

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* public route */}
        <Route path="/login" element={<Login />} />

        {/* everything below this guard needs a valid JWT */}
        <Route element={<RequireAuth />}>
          <Route path="/stores" element={<Stores />} />
          <Route path="/stores/:id/products" element={<Products />} />
          {/* add more protected routes here (store detail, parts, profile…) */}
        </Route>

        {/* catch-all → go to main page */}
        <Route path="*" element={<Navigate to="/stores" replace />} />
      </Routes>
    </BrowserRouter>
  );
}
