// src/services/api.js
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8080",
  //baseURL: import.meta.env.VITE_API_BASE_URL || "/api",
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
