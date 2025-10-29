import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';
import styled, { ThemeProvider } from 'styled-components';
import { GlobalStyle, theme } from './theme';
import telegramService from './services/telegram';
import { User } from './types';

// Pages
import HomePage from './pages/HomePage';
import FundsPage from './pages/FundsPage';
import DonationPage from './pages/DonationPage';
import SubscriptionPage from './pages/SubscriptionPage';
import SubscriptionPlansPage from './pages/SubscriptionPlansPage';
import CampaignsPage from './pages/CampaignsPage';
import ZakatCalculatorPage from './pages/ZakatCalculatorPage';
import ProfilePage from './pages/ProfilePage';
import PartnerApplicationPage from './pages/PartnerApplicationPage';

// Components
import LoadingSpinner from './components/LoadingSpinner';
import ErrorBoundary from './components/ErrorBoundary';

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

  .container {
    max-width: 100%;
    margin: 0 auto;
    padding: 0 16px;
  }

  .btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 500;
    text-decoration: none;
    cursor: pointer;
    transition: all 0.2s ease;
    background-color: var(--tg-button-color, #007bff);
    color: var(--tg-button-text-color, #ffffff);
    
    &:hover {
      opacity: 0.9;
    }
    
    &:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
    
    &.btn-secondary {
      background-color: #6c757d;
    }
    
    &.btn-success {
      background-color: #28a745;
    }
    
    &.btn-danger {
      background-color: #dc3545;
    }
    
    &.btn-outline {
      background-color: transparent;
      border: 2px solid var(--tg-button-color, #007bff);
      color: var(--tg-button-color, #007bff);
    }
  }

  .card {
    background: var(--tg-bg-color, #ffffff);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  .form-group {
    margin-bottom: 16px;
  }

  .form-label {
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
    color: var(--tg-text-color, #000000);
  }

  .form-input {
    width: 100%;
    padding: 12px;
    border: 2px solid #e9ecef;
    border-radius: 8px;
    font-size: 16px;
    background-color: var(--tg-bg-color, #ffffff);
    color: var(--tg-text-color, #000000);
    
    &:focus {
      outline: none;
      border-color: var(--tg-button-color, #007bff);
    }
  }

  .text-center {
    text-align: center;
  }

  .text-muted {
    color: #6c757d;
  }

  .mb-1 { margin-bottom: 8px; }
  .mb-2 { margin-bottom: 16px; }
  .mb-3 { margin-bottom: 24px; }
  .mb-4 { margin-bottom: 32px; }

  .mt-1 { margin-top: 8px; }
  .mt-2 { margin-top: 16px; }
  .mt-3 { margin-top: 24px; }
  .mt-4 { margin-top: 32px; }
`;

// Theme
const theme = {
  colors: {
    primary: '#007bff',
    secondary: '#6c757d',
    success: '#28a745',
    danger: '#dc3545',
    warning: '#ffc107',
    info: '#17a2b8',
    light: '#f8f9fa',
    dark: '#343a40',
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
  },
  borderRadius: {
    sm: '4px',
    md: '8px',
    lg: '12px',
    xl: '16px',
  },
};

// App Container
const AppContainer = styled.div`
  min-height: 100vh;
  background-color: var(--tg-bg-color, #ffffff);
`;

const App: React.FC = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [user, setUser] = useState<User | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const initializeApp = async () => {
      try {
        // Ждем инициализации Telegram WebApp
        if (!telegramService.isReady()) {
          // Если не в Telegram, используем mock данные для разработки
          console.log('Running in development mode');
          setIsLoading(false);
          return;
        }

        // Получаем данные пользователя из Telegram
        const telegramUser = telegramService.getUser();
        if (!telegramUser) {
          throw new Error('Telegram user data not available');
        }

        // Здесь можно добавить логику создания/получения пользователя из API
        // const userData = await userApi.getByTelegramId(telegramUser.id);
        // setUser(userData.data);

        setIsLoading(false);
      } catch (err) {
        console.error('App initialization error:', err);
        setError(err instanceof Error ? err.message : 'Unknown error');
        setIsLoading(false);
      }
    };

    initializeApp();
  }, []);

  if (isLoading) {
    return (
      <AppContainer>
        <LoadingSpinner />
      </AppContainer>
    );
  }

  if (error) {
    return (
      <AppContainer>
        <div className="container">
          <div className="card text-center">
            <h2>Ошибка загрузки</h2>
            <p className="text-muted">{error}</p>
            <button 
              className="btn" 
              onClick={() => window.location.reload()}
            >
              Попробовать снова
            </button>
          </div>
        </div>
      </AppContainer>
    );
  }

  return (
    <ErrorBoundary>
      <ThemeProvider theme={theme}>
        <QueryClientProvider client={queryClient}>
          <GlobalStyle />
          <Router>
            <AppContainer>
              <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/funds" element={<FundsPage />} />
                <Route path="/donation/:fundId" element={<DonationPage />} />
                <Route path="/subscription/:fundId" element={<SubscriptionPage />} />
                <Route path="/subscription-plans" element={<SubscriptionPlansPage />} />
                <Route path="/campaigns" element={<CampaignsPage />} />
                <Route path="/campaign/:campaignId" element={<CampaignsPage />} />
                <Route path="/zakat" element={<ZakatCalculatorPage />} />
                <Route path="/profile" element={<ProfilePage />} />
                <Route path="/partner" element={<PartnerApplicationPage />} />
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </AppContainer>
          </Router>
          <Toaster
            position="top-center"
            toastOptions={{
              duration: 4000,
              style: {
                background: 'var(--tg-bg-color, #ffffff)',
                color: 'var(--tg-text-color, #000000)',
                border: '1px solid #e9ecef',
              },
            }}
          />
        </QueryClientProvider>
      </ThemeProvider>
    </ErrorBoundary>
  );
};

export default App;
