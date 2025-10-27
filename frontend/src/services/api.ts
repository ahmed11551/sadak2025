import axios, { AxiosResponse } from 'axios';
import {
  User,
  UserCreate,
  UserUpdate,
  Fund,
  FundCreate,
  Donation,
  DonationCreate,
  DonationInitResponse,
  SimpleDonationRequest,
  SimpleDonationResponse,
  Subscription,
  SubscriptionCreate,
  SubscriptionInitResponse,
  ZakatCalculation,
  ZakatCalculationCreate,
  ZakatPayResponse,
  PartnerApplication,
  PartnerApplicationCreate,
  ApiResponse,
  PaginatedResponse
} from '../types';

// API Base Configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.reload();
    }
    return Promise.reject(error);
  }
);

// User API
export const userApi = {
  create: (userData: UserCreate): Promise<AxiosResponse<User>> =>
    api.post('/api/v1/users/', userData),
  
  getById: (userId: number): Promise<AxiosResponse<User>> =>
    api.get(`/api/v1/users/${userId}`),
  
  getByTelegramId: (telegramId: number): Promise<AxiosResponse<User>> =>
    api.get(`/api/v1/users/telegram/${telegramId}`),
  
  update: (userId: number, userData: UserUpdate): Promise<AxiosResponse<User>> =>
    api.put(`/api/v1/users/${userId}`, userData),
  
  getDonations: (userId: number): Promise<AxiosResponse<Donation[]>> =>
    api.get(`/api/v1/users/${userId}/donations`),
  
  getSubscriptions: (userId: number): Promise<AxiosResponse<Subscription[]>> =>
    api.get(`/api/v1/users/${userId}/subscriptions`),
};

// Fund API
export const fundApi = {
  getAll: (params?: {
    country_code?: string;
    purpose?: string;
    verified_only?: boolean;
    active_only?: boolean;
    limit?: number;
    offset?: number;
  }): Promise<AxiosResponse<Fund[]>> =>
    api.get('/api/v1/funds/', { params }),
  
  getById: (fundId: number): Promise<AxiosResponse<Fund>> =>
    api.get(`/api/v1/funds/${fundId}`),
  
  create: (fundData: FundCreate): Promise<AxiosResponse<Fund>> =>
    api.post('/api/v1/funds/', fundData),
  
  update: (fundId: number, fundData: Partial<FundCreate>): Promise<AxiosResponse<Fund>> =>
    api.put(`/api/v1/funds/${fundId}`, fundData),
  
  search: (query: string, params?: {
    country_code?: string;
    limit?: number;
  }): Promise<AxiosResponse<Fund[]>> =>
    api.get('/api/v1/funds/search/', { 
      params: { q: query, ...params } 
    }),
};

// Donation API
export const donationApi = {
  init: (donationData: DonationCreate): Promise<AxiosResponse<DonationInitResponse>> =>
    api.post('/api/v1/donations/init', donationData),
  
  confirm: (donationId: number, paymentData: any): Promise<AxiosResponse<ApiResponse>> =>
    api.post(`/api/v1/donations/${donationId}/confirm`, paymentData),
  
  getById: (donationId: number): Promise<AxiosResponse<Donation>> =>
    api.get(`/api/v1/donations/${donationId}`),
  
  getUserDonations: (userId: number, params?: {
    limit?: number;
    offset?: number;
  }): Promise<AxiosResponse<Donation[]>> =>
    api.get(`/api/v1/donations/user/${userId}`, { params }),
  
  refund: (donationId: number): Promise<AxiosResponse<ApiResponse>> =>
    api.post(`/api/v1/donations/${donationId}/refund`),
  
  createSimpleRequest: (data: SimpleDonationRequest): Promise<AxiosResponse<SimpleDonationResponse>> =>
    api.post('/api/v1/donations/simple-request', data),
};

// Subscription API
export const subscriptionApi = {
  init: (subscriptionData: SubscriptionCreate): Promise<AxiosResponse<SubscriptionInitResponse>> =>
    api.post('/api/v1/subscriptions/init', subscriptionData),
  
  getById: (subscriptionId: number): Promise<AxiosResponse<Subscription>> =>
    api.get(`/api/v1/subscriptions/${subscriptionId}`),
  
  update: (subscriptionId: number, subscriptionData: Partial<SubscriptionCreate>): Promise<AxiosResponse<Subscription>> =>
    api.patch(`/api/v1/subscriptions/${subscriptionId}`, subscriptionData),
  
  pause: (subscriptionId: number): Promise<AxiosResponse<ApiResponse>> =>
    api.post(`/api/v1/subscriptions/${subscriptionId}/pause`),
  
  resume: (subscriptionId: number): Promise<AxiosResponse<ApiResponse>> =>
    api.post(`/api/v1/subscriptions/${subscriptionId}/resume`),
  
  cancel: (subscriptionId: number): Promise<AxiosResponse<ApiResponse>> =>
    api.post(`/api/v1/subscriptions/${subscriptionId}/cancel`),
  
  getUserSubscriptions: (userId: number, statusFilter?: string): Promise<AxiosResponse<Subscription[]>> =>
    api.get(`/api/v1/subscriptions/user/${userId}`, {
      params: statusFilter ? { status_filter: statusFilter } : {}
    }),
};

// Zakat API
export const zakatApi = {
  calculate: (userId: number, zakatData: ZakatCalculationCreate): Promise<AxiosResponse<ZakatCalculation>> =>
    api.post(`/api/v1/zakat/calc?user_id=${userId}`, zakatData),
  
  pay: (zakatId: number, paymentMethod: string): Promise<AxiosResponse<ZakatPayResponse>> =>
    api.post('/api/v1/zakat/pay', {
      zakat_id: zakatId,
      payment_method: paymentMethod
    }),
  
  confirmPayment: (zakatId: number, paymentData: any): Promise<AxiosResponse<ApiResponse>> =>
    api.post(`/api/v1/zakat/${zakatId}/confirm`, paymentData),
  
  getUserHistory: (userId: number): Promise<AxiosResponse<ZakatCalculation[]>> =>
    api.get(`/api/v1/zakat/user/${userId}`),
  
  getCurrentNisab: (): Promise<AxiosResponse<{
    nisab_amount: number;
    currency: string;
    zakat_rate: number;
    description: string;
  }>> =>
    api.get('/api/v1/zakat/nisab'),
};

// Partner API
export const partnerApi = {
  createApplication: (applicationData: PartnerApplicationCreate): Promise<AxiosResponse<PartnerApplication>> =>
    api.post('/api/v1/partners/applications', applicationData),
  
  getApplications: (params?: {
    status_filter?: string;
    limit?: number;
    offset?: number;
  }): Promise<AxiosResponse<PartnerApplication[]>> =>
    api.get('/api/v1/partners/applications', { params }),
  
  getApplicationById: (applicationId: number): Promise<AxiosResponse<PartnerApplication>> =>
    api.get(`/api/v1/partners/applications/${applicationId}`),
  
  updateApplication: (applicationId: number, applicationData: Partial<PartnerApplicationCreate>, reviewerId: number): Promise<AxiosResponse<PartnerApplication>> =>
    api.patch(`/api/v1/partners/applications/${applicationId}`, {
      ...applicationData,
      reviewer_id: reviewerId
    }),
  
  approveApplication: (applicationId: number, reviewerId: number): Promise<AxiosResponse<ApiResponse>> =>
    api.post(`/api/v1/partners/applications/${applicationId}/approve`, {
      reviewer_id: reviewerId
    }),
  
  rejectApplication: (applicationId: number, reviewerId: number, reviewNotes: string): Promise<AxiosResponse<ApiResponse>> =>
    api.post(`/api/v1/partners/applications/${applicationId}/reject`, {
      reviewer_id: reviewerId,
      review_notes: reviewNotes
    }),
};

// Health Check
export const healthApi = {
  check: (): Promise<AxiosResponse<{
    status: string;
    database: string;
    timestamp: string;
  }>> =>
    api.get('/health'),
};

export default api;
