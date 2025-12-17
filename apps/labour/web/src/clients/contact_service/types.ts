export interface CreateContactMessageRequest {
  token: string;
  category: string;
  email: string;
  name: string;
  message: string;
  data?: Record<string, string>;
}

export interface ApiResponse<T = unknown> {
  success: boolean;
  data?: T;
  error?: string;
}

export type ContactResponse = ApiResponse<void>;
