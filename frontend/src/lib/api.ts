// lib/api.ts
import axios, { AxiosResponse, AxiosRequestConfig } from "axios";

// 1. Define a consistent response shape for API calls (optional but good practice)
// This is the shape the *server* wraps the actual data in (e.g., your CsrfResponse/LoginResponse types)
interface ServerResponse<T> {
  data: T;
  message?: string;
  success?: boolean;
}

const AUTH_SERVER = process.env.NEXT_PUBLIC_AUTH_SERVER_URL;

const api = axios.create({
  baseURL: AUTH_SERVER,
  withCredentials: true, // ✅ send cookies
  headers: {
    Accept: "application/json",
    "ngrok-skip-browser-warning": "true", // for dev tunnels
  },
});

/**
 * Type-safe wrapper for API GET requests.
 * @template T - The expected response type (e.g., CsrfResponse).
 * @template P - The expected query params type (optional).
 * @param {string} url - The endpoint URL.
 * @param {P} [params] - Optional query parameters.
 * @param {AxiosRequestConfig} [config] - Optional Axios request config.
 * @returns {Promise<T>} The data from the API response.
 */
export async function typedGet<T, P = undefined>(
  url: string,
  params?: P,
  config?: AxiosRequestConfig
): Promise<T> {
  const response: AxiosResponse<T> = await api.get(url, { ...config, params });

  // NOTE: If your backend wraps the data, you might need to return response.data
  // If T is already the full server response shape, T is returned directly.
  return response.data;
}

/**
 * Type-safe wrapper for API POST requests.
 * @template T - The expected response type (e.g., LoginResponse).
 * @template D - The data being sent in the request body.
 * @param {string} url - The endpoint URL.
 * @param {D} data - The request body data.
 * @param {AxiosRequestConfig} [config] - Optional Axios request config.
 * @returns {Promise<T>} The data from the API response.
 */
export async function typedPost<T, D = undefined>(
  url: string,
  data?: D,
  config?: AxiosRequestConfig
): Promise<T> {
  // Use T as the type for the response data
  const response: AxiosResponse<T> = await api.post(url, data, config);

  // NOTE: If your backend wraps the data, you might need to return response.data
  // If T is already the full server response shape, T is returned directly.
  return response.data;
}

// Export the axios instance as the default export
export default api;
