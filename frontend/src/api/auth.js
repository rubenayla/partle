// src/api/auth.js
import api from "./client";

export async function register(email, password) {
  return api.post("/auth/register", { email, password });
}

export async function login(email, password) {
  const form = new FormData();
  form.append("username", email);
  form.append("password", password);

  const { data } = await api.post("/auth/login", form, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  localStorage.setItem("partle_token", data.access_token);
  return data;
}

export async function currentUser() {
  return api.get("/auth/me").then((r) => r.data);
}
