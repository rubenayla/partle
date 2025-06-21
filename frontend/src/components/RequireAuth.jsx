// frontend/src/components/RequireAuth.jsx
import { useEffect, useState } from "react";
import { Navigate, Outlet } from "react-router-dom";
import api from "../api/index.js";

export default function RequireAuth() {
  const [allowed, setAllowed] = useState(null);

  useEffect(() => {
    async function check() {
      const token = localStorage.getItem("token");
      if (!token) return setAllowed(false);
      try {
        await api.get("/v1/auth/me");
        setAllowed(true);
      } catch {
        localStorage.removeItem("token");
        setAllowed(false);
      }
    }
    check();
  }, []);

  if (allowed === null) return null;
  return allowed ? <Outlet /> : <Navigate to="/" replace />;
}
