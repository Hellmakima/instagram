// lib/types/api.ts

// Matches the backend's ErrorDetail Pydantic model
export interface ErrorDetail {
  code: string;
  details: string;
}

// Matches the backend's APIErrorResponse Pydantic model
export interface APIErrorResponse {
  success: false; // Must be false for error response
  message: string;
  error: ErrorDetail;
}

// Matches the backend's SuccessMessageResponse Pydantic model
// T is the type for the 'data' field, which is a dict in your FastAPI model
export interface SuccessResponse<T = {}> {
  success: true; // Must be true for success response
  message: string;
  data: T;
}

// A union type for all possible top-level server responses
export type ServerResponse<T = {}> = SuccessResponse<T> | APIErrorResponse;
