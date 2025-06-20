// src/api/auth.js
import api from "./client";

export async function login(email, password) {
  const body = new URLSearchParams({ username: email, password });
  const { data } = await api.post("/v1/auth/login", body, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  localStorage.setItem("token", data.access_token);
  return data;
}

export async function register(email, password) {
  return api.post("/v1/auth/register", { email, password });
}

export async function requestReset(email) {
  return api.post("/v1/auth/request-password-reset", { email });
}

export async function currentUser() {
  return api.get("/v1/auth/me").then((r) => r.data);
}
