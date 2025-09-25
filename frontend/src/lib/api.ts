import axios from "axios";

const AUTH_SERVER = process.env.NEXT_PUBLIC_AUTH_SERVER_URL;

const api = axios.create({
  baseURL: AUTH_SERVER,
  withCredentials: true, // ✅ send cookies
  headers: {
    Accept: "application/json",
    "ngrok-skip-browser-warning": "true", // for dev tunnels
  },
});

export default api;
