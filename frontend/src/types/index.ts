// User Types
export interface User {
  id: number;
  telegram_id: number;
  username?: string;
  first_name?: string;
  last_name?: string;
  language_code: string;
  locale: string;
  timezone: string;
  madhab?: string;
  is_premium: boolean;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface UserCreate {
  telegram_id: number;
  username?: string;
  first_name?: string;
  last_name?: string;
  language_code?: string;
  locale?: string;
  timezone?: string;
  madhab?: string;
}

export interface UserUpdate {
  username?: string;
  first_name?: string;
  last_name?: string;
  language_code?: string;
  locale?: string;
  timezone?: string;
  madhab?: string;
}

// Fund Types
export interface Fund {
  id: number;
  name: string;
  short_desc?: string;
  country_code: string;
  purposes?: string[];
  logo_url?: string;
  website?: string;
  social_links?: Record<string, any>;
  partner_enabled: boolean;
  verified: boolean;
  active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface FundCreate {
  name: string;
  short_desc?: string;
  country_code: string;
  purposes?: string[];
  logo_url?: string;
  website?: string;
  social_links?: Record<string, any>;
  partner_enabled?: boolean;
}

// Donation Types
export interface Donation {
  id: number;
  user_id: number;
  fund_id: number;
  amount: number;
  currency: string;
  purpose?: string;
  payment_method: string;
  status: 'pending' | 'completed' | 'failed' | 'refunded';
  payment_id?: string;
  transaction_id?: string;
  created_at: string;
  updated_at?: string;
}

export interface DonationCreate {
  fund_id: number;
  amount: number;
  currency?: string;
  purpose?: string;
  payment_method: string;
}

export interface DonationInitResponse {
  donation_id: number;
  amount: number;
  currency: string;
  payment_url: string;
  status: string;
}

// Simple Donation Request Types
export interface SimpleDonationRequest {
  name: string;
  phone: string;
  email?: string;
  amount: string;
  currency?: string;
  fund_id?: number;
  purpose?: string;
  message?: string;
}

export interface SimpleDonationResponse {
  success: boolean;
  message: string;
  request_id: number;
  data: {
    name: string;
    phone: string;
    email?: string;
    amount: number;
    currency: string;
    fund_id?: number;
    purpose?: string;
    created_at: string;
  };
}

// Subscription Types
export interface Subscription {
  id: number;
  user_id: number;
  fund_id: number;
  amount: number;
  currency: string;
  frequency: 'daily' | 'weekly' | 'monthly';
  purpose?: string;
  payment_method: string;
  subscription_id?: string;
  status: 'active' | 'paused' | 'cancelled';
  next_payment_date?: string;
  created_at: string;
  updated_at?: string;
}

export interface SubscriptionCreate {
  fund_id: number;
  amount: number;
  currency?: string;
  frequency: 'daily' | 'weekly' | 'monthly';
  purpose?: string;
  payment_method: string;
}

export interface SubscriptionInitResponse {
  subscription_id: number;
  amount: number;
  currency: string;
  frequency: string;
  next_payment_date: string;
  status: string;
}

// Zakat Types
export interface ZakatCalculation {
  id: number;
  user_id: number;
  cash_at_home: number;
  bank_accounts: number;
  shares_value: number;
  goods_profit: number;
  gold_silver_value: number;
  property_investments: number;
  other_income: number;
  debts: number;
  expenses: number;
  total_assets: number;
  total_liabilities: number;
  zakatable_amount: number;
  nisab_amount: number;
  zakat_amount: number;
  is_paid: boolean;
  payment_id?: string;
  created_at: string;
  updated_at?: string;
}

export interface ZakatCalculationCreate {
  cash_at_home?: number;
  bank_accounts?: number;
  shares_value?: number;
  goods_profit?: number;
  gold_silver_value?: number;
  property_investments?: number;
  other_income?: number;
  debts?: number;
  expenses?: number;
}

export interface ZakatPayResponse {
  zakat_id: number;
  amount: number;
  currency: string;
  payment_url: string;
  status: string;
}

// Partner Application Types
export interface PartnerApplication {
  id: number;
  organization_name: string;
  contact_person: string;
  email: string;
  phone?: string;
  website?: string;
  description: string;
  purposes?: string[];
  documents?: Record<string, any>;
  status: 'pending' | 'approved' | 'rejected';
  reviewed_by?: number;
  review_notes?: string;
  created_at: string;
  updated_at?: string;
}

export interface PartnerApplicationCreate {
  organization_name: string;
  contact_person: string;
  email: string;
  phone?: string;
  website?: string;
  description: string;
  purposes?: string[];
  documents?: Record<string, any>;
}

// Campaign Types
export interface Campaign {
  id: number;
  owner_id: number;
  fund_id?: number;
  title: string;
  description: string;
  category: string;
  goal_amount: number;
  collected_amount: number;
  country_code: string;
  status: 'pending' | 'active' | 'completed' | 'cancelled';
  end_date?: string;
  banner_url?: string;
  participants_count: number;
  created_at: string;
  updated_at?: string;
}

export interface CampaignCreate {
  fund_id?: number;
  title: string;
  description: string;
  category: string;
  goal_amount: number;
  country_code: string;
  end_date?: string;
  banner_url?: string;
}

export interface CampaignUpdate {
  title?: string;
  description?: string;
  category?: string;
  goal_amount?: number;
  end_date?: string;
  banner_url?: string;
  status?: string;
}

// Subscription Plan Types
export interface SubscriptionPlan {
  id: number;
  name: string;
  display_name: string;
  description?: string;
  price_monthly: number;
  price_3months?: number;
  price_6months?: number;
  price_12months?: number;
  charity_percentage: number;
  features?: string[];
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

export interface SubscriptionPlanCreate {
  name: string;
  display_name: string;
  description?: string;
  price_monthly: number;
  price_3months?: number;
  price_6months?: number;
  price_12months?: number;
  charity_percentage: number;
  features?: string[];
}

// API Response Types
export interface ApiResponse<T = any> {
  data?: T;
  message?: string;
  error?: string;
  detail?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}

// Telegram WebApp Types
export interface TelegramWebApp {
  initData: string;
  initDataUnsafe: {
    user?: {
      id: number;
      first_name: string;
      last_name?: string;
      username?: string;
      language_code?: string;
    };
    auth_date: number;
    hash: string;
  };
  version: string;
  platform: string;
  colorScheme: 'light' | 'dark';
  themeParams: {
    bg_color?: string;
    text_color?: string;
    hint_color?: string;
    link_color?: string;
    button_color?: string;
    button_text_color?: string;
  };
  isExpanded: boolean;
  viewportHeight: number;
  viewportStableHeight: number;
  headerColor: string;
  backgroundColor: string;
  isClosingConfirmationEnabled: boolean;
  BackButton: {
    isVisible: boolean;
    onClick: (callback: () => void) => void;
    offClick: (callback: () => void) => void;
    show: () => void;
    hide: () => void;
  };
  MainButton: {
    text: string;
    color: string;
    textColor: string;
    isVisible: boolean;
    isActive: boolean;
    isProgressVisible: boolean;
    setText: (text: string) => void;
    onClick: (callback: () => void) => void;
    offClick: (callback: () => void) => void;
    show: () => void;
    hide: () => void;
    enable: () => void;
    disable: () => void;
    showProgress: (leaveActive?: boolean) => void;
    hideProgress: () => void;
    setParams: (params: {
      text?: string;
      color?: string;
      text_color?: string;
      is_active?: boolean;
      is_visible?: boolean;
    }) => void;
  };
  HapticFeedback: {
    impactOccurred: (style: 'light' | 'medium' | 'heavy' | 'rigid' | 'soft') => void;
    notificationOccurred: (type: 'error' | 'success' | 'warning') => void;
    selectionChanged: () => void;
  };
  ready: () => void;
  expand: () => void;
  close: () => void;
  sendData: (data: string) => void;
  openLink: (url: string, options?: { try_instant_view?: boolean }) => void;
  openTelegramLink: (url: string) => void;
  openInvoice: (url: string, callback?: (status: string) => void) => void;
  showPopup: (params: {
    title?: string;
    message: string;
    buttons?: Array<{
      id?: string;
      type?: 'default' | 'ok' | 'close' | 'cancel' | 'destructive';
      text?: string;
    }>;
  }, callback?: (buttonId: string) => void) => void;
  showAlert: (message: string, callback?: () => void) => void;
  showConfirm: (message: string, callback?: (confirmed: boolean) => void) => void;
  showScanQrPopup: (params: {
    text?: string;
  }, callback?: (text: string) => void) => void;
  closeScanQrPopup: () => void;
  readTextFromClipboard: (callback?: (text: string) => void) => void;
  requestWriteAccess: (callback?: (granted: boolean) => void) => void;
  requestContact: (callback?: (granted: boolean) => void) => void;
}
