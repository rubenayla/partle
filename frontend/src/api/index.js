// src/api/index.js
import axios from "axios";
export default axios.create({ baseURL: "/v1" });