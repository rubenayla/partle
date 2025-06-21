// backend/src/api/v1/stores.js
import api from "./client"; // TODO UPDATE

export const listStores = () => api.get("/v1/stores/").then((r) => r.data);

export const createStore = (payload) =>
  api.post("/v1/stores/", payload).then((r) => r.data);
