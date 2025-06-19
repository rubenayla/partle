import { Navigate, Outlet } from "react-router-dom";

export default function RequireAuth() {
  const token = localStorage.getItem("token");
  return token ? <Outlet /> : <Navigate to="/account" replace />;
}
