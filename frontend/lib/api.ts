import axios from 'axios';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized - redirect to login
      if (typeof window !== 'undefined') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

// API endpoints
export const authApi = {
  login: (username: string, password: string) =>
    api.post('/api/auth/login/', { username, password }),
  logout: () => api.post('/api/auth/logout/'),
  getCurrentUser: () => api.get('/api/auth/user/'),
};

export const postsApi = {
  list: () => api.get('/posts'),
  get: (id: number) => api.get(`/posts/${id}`),
  create: (data: FormData) => api.post('/posts', data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  update: (id: number, data: FormData) => api.patch(`/posts/${id}`, data, {
    headers: { 'Content-Type': 'multipart/form-data' },
  }),
  delete: (id: number) => api.delete(`/posts/${id}`),
  publish: (id: number) => api.post(`/posts/${id}/publish`),
};

export const capabilitiesApi = {
  get: (contentType: 'TEXT' | 'PHOTO' | 'VIDEO') =>
    api.get(`/capabilities?content_type=${contentType}`),
  validate: (data: any) => api.post('/capabilities/validate', data),
};

export type ContentType = 'TEXT' | 'PHOTO' | 'VIDEO';

export interface PlatformAvailability {
  platform: string;
  available: boolean;
  reason: string | null;
  accounts: AccountAvailability[];
  requires_action?: boolean;
  action_hint?: string;
}

export interface AccountAvailability {
  social_account_id: number;
  display_name: string;
  available: boolean;
  reason: string | null;
  requires_action?: boolean;
  action_hint?: string;
}

export interface Post {
  id: number;
  content_type: ContentType;
  caption: string;
  hashtags: string[];
  image_file?: string;
  video_file?: string;
  media_metadata?: Record<string, any>;
  created_at: string;
  targets?: PostTarget[];
}

export interface PostTarget {
  id: number;
  social_account_id: number;
  status: 'selected' | 'queued' | 'rejected' | 'published';
  last_error?: string;
}

