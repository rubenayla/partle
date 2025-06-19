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

export async function fidoLoginBegin(email) {
  const { data } = await api.post("/auth/fido/login/begin", { email });
  return decodeFidoOptions(data);
}

export async function fidoLoginFinish(payload) {
  const { data } = await api.post("/auth/fido/login/finish", toBase64(payload));
  localStorage.setItem("partle_token", data.access_token);
  return data;
}

export async function fidoRegisterBegin() {
  const { data } = await api.post("/auth/fido/register/begin");
  return decodeFidoOptions(data);
}

export async function fidoRegisterFinish(payload) {
  return api.post("/auth/fido/register/finish", toBase64(payload));
}

function toBase64(obj) {
  const enc = (v) => btoa(String.fromCharCode(...new Uint8Array(v)));
  const out = {};
  for (const k in obj) out[k] = enc(obj[k]);
  return out;
}

function decodeFidoOptions(options) {
  const dec = (v) => Uint8Array.from(atob(v), (c) => c.charCodeAt(0));
  const walk = (o) => {
    if (Array.isArray(o)) return o.map(walk);
    if (o && typeof o === "object") {
      const res = {};
      for (const k in o) {
        res[k] =
          k === "challenge" || k === "user" || k === "id"
            ? dec(o[k])
            : walk(o[k]);
      }
      return res;
    }
    return o;
  };
  return walk(options);
}
