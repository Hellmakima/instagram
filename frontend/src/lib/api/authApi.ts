// lib/api/authApi.ts

import axios, {
  AxiosInstance,
  AxiosResponse,
  AxiosError,
  AxiosRequestConfig,
} from "axios";
import { SuccessResponse, APIErrorResponse, ErrorDetail } from "@/types/api"; // Import your interfaces

// --- Custom Error Class for the Frontend ---
// This simplifies component-level error handling
export class BackendApiError extends Error {
  public status: number;
  public serverResponse: APIErrorResponse;

  constructor(status: number, serverResponse: APIErrorResponse) {
    // Use the error message from the server response
    super(serverResponse.message);
    this.name = "BackendApiError";
    this.status = status;
    this.serverResponse = serverResponse;
    Object.setPrototypeOf(this, BackendApiError.prototype);
  }
}

// --- Axios Instance Setup ---
const AUTH_SERVER = process.env.NEXT_PUBLIC_AUTH_SERVER_URL;

export const authApi: AxiosInstance = axios.create({
  baseURL: AUTH_SERVER,
  withCredentials: true, // ✅ Essential for sending the HTTP-only refresh/CSRF cookies
  headers: {
    Accept: "application/json",
    "ngrok-skip-browser-warning": "true", // For dev tunnels
    "Content-Type": "application/json",
  },
});

// --- Response Interceptor: Handling Custom Backend Errors ---
authApi.interceptors.response.use(
  // 1. Successful HTTP status (2xx)
  (
    response: AxiosResponse<SuccessResponse<any> | APIErrorResponse>
  ): AxiosResponse<SuccessResponse<any>> => {
    // PROACTIVE SECURITY CHECK: If the server returns a 2xx status but 'success: false'
    // (which is uncommon but possible in custom wrappers), treat it as a critical error.
    if (
      response.data &&
      "success" in response.data &&
      response.data.success === false
    ) {
      // Treat this as an unexpected error structure for 2xx status
      console.error(
        "Server returned 2xx with 'success: false'. Full response:",
        response.data
      );
      throw new BackendApiError(response.status, {
        success: false,
        message: "Unexpected success=false on 2XX response.",
        error: {
          code: "UNEXPECTED_RESPONSE",
          details: JSON.stringify(response.data),
        },
      });
    }

    // Return the response, typed as the success shape
    return response as AxiosResponse<SuccessResponse<any>>;
  },
  // 2. HTTP Error Status (4xx, 5xx)
  (error: AxiosError<APIErrorResponse | any>) => {
    // a) Server responded with a known error structure (e.g., from HTTPException)
    if (
      error.response &&
      error.response.data &&
      "error" in error.response.data
    ) {
      // The response.data is the APIErrorResponse structure
      const status = error.response.status;
      const serverResponse = error.response.data as APIErrorResponse;

      // Throw the custom error for the calling function to catch
      return Promise.reject(new BackendApiError(status, serverResponse));
    }

    // b) Network Error (no response) or Unknown Error (e.g., parsing issue)
    let message = "A network error occurred or server is unreachable.";
    let status = 0; // Custom status for network issues
    let details: ErrorDetail = {
      code: "NETWORK_ERROR",
      details: error.message,
    };

    if (error.response) {
      // Unstructured or unexpected server error format (e.g., standard NGINX 502 page)
      message = `Server returned unhandled status: ${error.response.status}`;
      status = error.response.status;
      details.code = "UNSTRUCTURED_RESPONSE";
      details.details = error.response.data
        ? JSON.stringify(error.response.data).substring(0, 100) + "..."
        : "No response body.";
    }

    // Default fallback error
    const fallbackErrorResponse: APIErrorResponse = {
      success: false,
      message: message,
      error: details,
    };

    return Promise.reject(new BackendApiError(status, fallbackErrorResponse));
  }
);

// --- Type-Safe Request Wrappers (Similar to your initial design) ---

/**
 * Type-safe wrapper for API requests to the Auth Server.
 * @template T - The type of the data field inside the SuccessResponse (e.g., { token: string })
 * @template D - The data being sent in the request body (for POST/PUT) or query params (for GET).
 * @returns {Promise<SuccessResponse<T>>} The full structured success response.
 */
export async function authRequest<T = any, D = undefined>(
  method: "GET" | "POST" | "PUT" | "DELETE" | "PATCH",
  url: string,
  dataOrParams?: D,
  config?: AxiosRequestConfig
): Promise<SuccessResponse<T>> {
  const isDataMethod =
    method === "POST" || method === "PUT" || method === "PATCH";

  const requestConfig: AxiosRequestConfig = {
    method,
    url,
    // Pass data for POST/PUT, or params for GET
    data: isDataMethod ? dataOrParams : undefined,
    params: !isDataMethod ? dataOrParams : undefined,
    ...config,
  };

  // The response is now guaranteed to be a SuccessResponse<T> or an exception is thrown
  const response: AxiosResponse<SuccessResponse<T>> = await authApi.request(
    requestConfig
  );

  // Return the response data, which is the SuccessResponse<T> structure
  return response.data;
}

// --- Export Dedicated Functions (Optional, but often cleaner) ---

// e.g., type CsrfResponse = { csrf_token: string }
export function getCsrfToken<T>(
  config?: AxiosRequestConfig
): Promise<SuccessResponse<T>> {
  return authRequest<T>("GET", "/auth/csrf-token", undefined, config);
}

// e.g., type LoginResponse = { access_token: string }
export function loginUser<T, D>(
  data: D,
  config?: AxiosRequestConfig
): Promise<SuccessResponse<T>> {
  return authRequest<T, D>("POST", "/login", data, config);
}

// Export the axios instance as the default export for advanced use
export default authApi;
