// frontend/src/api/index.js
import axios from "axios";

if (!import.meta.env.VITE_API_BASE) {
  throw new Error("VITE_API_BASE is not defined");
}

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export default api;