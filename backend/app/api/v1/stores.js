// src/api/stores.js
import api from "./client";

export const listStores = () => api.get("/v1/stores").then((r) => r.data);

export const createStore = (payload) =>
  api.post("/v1/stores", payload).then((r) => r.data);
