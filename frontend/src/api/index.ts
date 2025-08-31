// frontend/src/api/index.ts
import axios, { AxiosResponse } from "axios";
import { logger } from "../utils/logger";

if (!import.meta.env.VITE_API_BASE) {
  throw new Error("VITE_API_BASE is not defined");
}

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE,
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token
    const token = localStorage.getItem("token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
    
    // Add request tracking
    (config as any).metadata = {
      startTime: performance.now(),
      url: config.url,
      method: config.method?.toUpperCase()
    };
    
    return config;
  },
  (error) => {
    logger.error("Request interceptor error", {
      error: error.message,
      stack: error.stack
    });
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response: AxiosResponse) => {
    const config = response.config as any;
    const duration = performance.now() - config.metadata.startTime;
    
    // Log successful API calls
    logger.logApiCall(
      config.metadata.method,
      config.metadata.url,
      response.status,
      duration
    );
    
    return response;
  },
  (error) => {
    const config = error.config as any;
    const duration = config?.metadata ? performance.now() - config.metadata.startTime : 0;
    
    // Log failed API calls
    if (config?.metadata) {
      logger.logApiCall(
        config.metadata.method,
        config.metadata.url,
        error.response?.status || 0,
        duration,
        error
      );
    }
    
    return Promise.reject(error);
  }
);

export default api;
