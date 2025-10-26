import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import '@testing-library/jest-dom';
import HomePage from '../src/pages/HomePage';
import ZakatCalculatorPage from '../src/pages/ZakatCalculatorPage';
import CampaignsPage from '../src/pages/CampaignsPage';
import SubscriptionPlansPage from '../src/pages/SubscriptionPlansPage';

// Mock Telegram WebApp
const mockTelegramWebApp = {
  ready: jest.fn(),
  expand: jest.fn(),
  close: jest.fn(),
  sendData: jest.fn(),
  openLink: jest.fn(),
  showAlert: jest.fn(),
  showConfirm: jest.fn(),
  showPopup: jest.fn(),
  MainButton: {
    setText: jest.fn(),
    onClick: jest.fn(),
    offClick: jest.fn(),
    show: jest.fn(),
    hide: jest.fn(),
    enable: jest.fn(),
    disable: jest.fn(),
    showProgress: jest.fn(),
    hideProgress: jest.fn(),
    setParams: jest.fn(),
    text: '',
    color: '',
    textColor: '',
    isVisible: false,
    isActive: true,
    isProgressVisible: false,
  },
  BackButton: {
    onClick: jest.fn(),
    offClick: jest.fn(),
    show: jest.fn(),
    hide: jest.fn(),
    isVisible: false,
  },
  HapticFeedback: {
    impactOccurred: jest.fn(),
    notificationOccurred: jest.fn(),
    selectionChanged: jest.fn(),
  },
  initData: '',
  initDataUnsafe: {
    user: {
      id: 123456789,
      first_name: 'Test',
      last_name: 'User',
      username: 'testuser',
      language_code: 'ru',
    },
    auth_date: 1234567890,
    hash: 'test_hash',
  },
  version: '6.0',
  platform: 'web',
  colorScheme: 'light',
  themeParams: {
    bg_color: '#ffffff',
    text_color: '#000000',
    hint_color: '#999999',
    link_color: '#007bff',
    button_color: '#007bff',
    button_text_color: '#ffffff',
  },
  isExpanded: true,
  viewportHeight: 600,
  viewportStableHeight: 600,
  headerColor: '#ffffff',
  backgroundColor: '#ffffff',
  isClosingConfirmationEnabled: false,
};

// Mock window.Telegram
Object.defineProperty(window, 'Telegram', {
  value: {
    WebApp: mockTelegramWebApp,
  },
  writable: true,
});

// Test wrapper component
const TestWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
      },
    },
  });

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        {children}
      </BrowserRouter>
    </QueryClientProvider>
  );
};

describe('HomePage', () => {
  test('renders main title and subtitle', () => {
    render(
      <TestWrapper>
        <HomePage />
      </TestWrapper>
    );

    expect(screen.getByText('🕌 Sadaka-Pass')).toBeInTheDocument();
    expect(screen.getByText('Платформа для пожертвований и расчета закята')).toBeInTheDocument();
  });

  test('displays statistics cards', () => {
    render(
      <TestWrapper>
        <HomePage />
      </TestWrapper>
    );

    expect(screen.getByText('1,247')).toBeInTheDocument();
    expect(screen.getByText('Пожертвований')).toBeInTheDocument();
    expect(screen.getByText('89')).toBeInTheDocument();
    expect(screen.getByText('Фондов')).toBeInTheDocument();
    expect(screen.getByText('₽2.4M')).toBeInTheDocument();
    expect(screen.getByText('Собрано')).toBeInTheDocument();
  });

  test('displays action cards', () => {
    render(
      <TestWrapper>
        <HomePage />
      </TestWrapper>
    );

    expect(screen.getByText('Разовое пожертвование')).toBeInTheDocument();
    expect(screen.getByText('Калькулятор закята')).toBeInTheDocument();
    expect(screen.getByText('Садака-подписка')).toBeInTheDocument();
    expect(screen.getByText('Целевые кампании')).toBeInTheDocument();
    expect(screen.getByText('Стать партнером')).toBeInTheDocument();
  });

  test('displays features section', () => {
    render(
      <TestWrapper>
        <HomePage />
      </TestWrapper>
    );

    expect(screen.getByText('Преимущества платформы')).toBeInTheDocument();
    expect(screen.getByText('100% прозрачность использования средств')).toBeInTheDocument();
    expect(screen.getByText('Верифицированные благотворительные фонды')).toBeInTheDocument();
  });
});

describe('ZakatCalculatorPage', () => {
  test('renders calculator title and form', () => {
    render(
      <TestWrapper>
        <ZakatCalculatorPage />
      </TestWrapper>
    );

    expect(screen.getByText('🧮 Калькулятор закята')).toBeInTheDocument();
    expect(screen.getByText('Рассчитайте размер закята на основе ваших активов')).toBeInTheDocument();
  });

  test('displays asset input fields', () => {
    render(
      <TestWrapper>
        <ZakatCalculatorPage />
      </TestWrapper>
    );

    expect(screen.getByLabelText('Наличные дома')).toBeInTheDocument();
    expect(screen.getByLabelText('Остаток на банковских счетах')).toBeInTheDocument();
    expect(screen.getByLabelText('Стоимость акций при перепродаже')).toBeInTheDocument();
    expect(screen.getByLabelText('Товары и прибыль')).toBeInTheDocument();
    expect(screen.getByLabelText('Золото и серебро (по текущей стоимости)')).toBeInTheDocument();
    expect(screen.getByLabelText('Имущество, удерживаемое в качестве инвестиций')).toBeInTheDocument();
    expect(screen.getByLabelText('Другие доходы')).toBeInTheDocument();
  });

  test('displays liability input fields', () => {
    render(
      <TestWrapper>
        <ZakatCalculatorPage />
      </TestWrapper>
    );

    expect(screen.getByLabelText('Вычесть долги')).toBeInTheDocument();
    expect(screen.getByLabelText('Вычесть расходы')).toBeInTheDocument();
  });

  test('calculates zakat in real-time', async () => {
    render(
      <TestWrapper>
        <ZakatCalculatorPage />
      </TestWrapper>
    );

    const cashInput = screen.getByLabelText('Наличные дома');
    const bankInput = screen.getByLabelText('Остаток на банковских счетах');

    fireEvent.change(cashInput, { target: { value: '100000' } });
    fireEvent.change(bankInput, { target: { value: '500000' } });

    await waitFor(() => {
      expect(screen.getByText('₽600,000')).toBeInTheDocument(); // Total assets
    });
  });

  test('shows calculate button', () => {
    render(
      <TestWrapper>
        <ZakatCalculatorPage />
      </TestWrapper>
    );

    expect(screen.getByText('Рассчитать закят')).toBeInTheDocument();
  });
});

describe('CampaignsPage', () => {
  test('renders campaigns title and tabs', () => {
    render(
      <TestWrapper>
        <CampaignsPage />
      </TestWrapper>
    );

    expect(screen.getByText('Целевые кампании')).toBeInTheDocument();
    expect(screen.getByText('Активные кампании')).toBeInTheDocument();
    expect(screen.getByText('Создать кампанию')).toBeInTheDocument();
  });

  test('switches between tabs', () => {
    render(
      <TestWrapper>
        <CampaignsPage />
      </TestWrapper>
    );

    const createTab = screen.getByText('Создать кампанию');
    fireEvent.click(createTab);

    expect(screen.getByText('Название кампании *')).toBeInTheDocument();
    expect(screen.getByText('Описание *')).toBeInTheDocument();
    expect(screen.getByText('Категория *')).toBeInTheDocument();
    expect(screen.getByText('Целевая сумма (₽) *')).toBeInTheDocument();
  });

  test('displays campaign creation form', () => {
    render(
      <TestWrapper>
        <CampaignsPage />
      </TestWrapper>
    );

    // Switch to create tab
    const createTab = screen.getByText('Создать кампанию');
    fireEvent.click(createTab);

    expect(screen.getByLabelText('Название кампании *')).toBeInTheDocument();
    expect(screen.getByLabelText('Описание *')).toBeInTheDocument();
    expect(screen.getByLabelText('Категория *')).toBeInTheDocument();
    expect(screen.getByLabelText('Целевая сумма (₽) *')).toBeInTheDocument();
    expect(screen.getByLabelText('Срок сбора')).toBeInTheDocument();
    expect(screen.getByLabelText('Ссылка на изображение (опционально)')).toBeInTheDocument();
  });

  test('shows category options', () => {
    render(
      <TestWrapper>
        <CampaignsPage />
      </TestWrapper>
    );

    // Switch to create tab
    const createTab = screen.getByText('Создать кампанию');
    fireEvent.click(createTab);

    const categorySelect = screen.getByLabelText('Категория *');
    fireEvent.click(categorySelect);

    expect(screen.getByText('Строительство мечети')).toBeInTheDocument();
    expect(screen.getByText('Помощь сиротам')).toBeInTheDocument();
    expect(screen.getByText('Медицинская помощь')).toBeInTheDocument();
    expect(screen.getByText('Образование')).toBeInTheDocument();
  });
});

describe('SubscriptionPlansPage', () => {
  test('renders subscription plans title', () => {
    render(
      <TestWrapper>
        <SubscriptionPlansPage />
      </TestWrapper>
    );

    expect(screen.getByText('Садака-подписка')).toBeInTheDocument();
    expect(screen.getByText('Регулярная милостыня для развития цифровой уммы')).toBeInTheDocument();
  });

  test('displays period selector', () => {
    render(
      <TestWrapper>
        <SubscriptionPlansPage />
      </TestWrapper>
    );

    expect(screen.getByText('Выберите период подписки')).toBeInTheDocument();
    expect(screen.getByText('1 месяц')).toBeInTheDocument();
    expect(screen.getByText('3 месяца')).toBeInTheDocument();
    expect(screen.getByText('6 месяцев')).toBeInTheDocument();
    expect(screen.getByText('12 месяцев')).toBeInTheDocument();
  });

  test('displays subscription plans', () => {
    render(
      <TestWrapper>
        <SubscriptionPlansPage />
      </TestWrapper>
    );

    expect(screen.getByText('Базовый')).toBeInTheDocument();
    expect(screen.getByText('Pro')).toBeInTheDocument();
    expect(screen.getByText('Premium')).toBeInTheDocument();
  });

  test('shows plan features', () => {
    render(
      <TestWrapper>
        <SubscriptionPlansPage />
      </TestWrapper>
    );

    expect(screen.getByText('Доступ к базовым кампаниям')).toBeInTheDocument();
    expect(screen.getByText('История пожертвований')).toBeInTheDocument();
    expect(screen.getByText('5% от подписки в благотворительность')).toBeInTheDocument();
    expect(screen.getByText('10% от подписки в благотворительность')).toBeInTheDocument();
  });

  test('displays charity information', () => {
    render(
      <TestWrapper>
        <SubscriptionPlansPage />
      </TestWrapper>
    );

    expect(screen.getByText('5% от подписки идет в благотворительность')).toBeInTheDocument();
    expect(screen.getByText('10% от подписки идет в благотворительность')).toBeInTheDocument();
  });

  test('shows plan selection buttons', () => {
    render(
      <TestWrapper>
        <SubscriptionPlansPage />
      </TestWrapper>
    );

    expect(screen.getByText('Выбрать Базовый')).toBeInTheDocument();
    expect(screen.getByText('Выбрать Pro')).toBeInTheDocument();
    expect(screen.getByText('Выбрать Premium')).toBeInTheDocument();
  });

  test('displays information sections', () => {
    render(
      <TestWrapper>
        <SubscriptionPlansPage />
      </TestWrapper>
    );

    expect(screen.getByText('Что такое садака-подписка?')).toBeInTheDocument();
    expect(screen.getByText('Преимущества подписки')).toBeInTheDocument();
  });
});

describe('Navigation', () => {
  test('navigates between pages', () => {
    render(
      <TestWrapper>
        <HomePage />
      </TestWrapper>
    );

    // Test navigation to campaigns
    const campaignsCard = screen.getByText('Целевые кампании');
    fireEvent.click(campaignsCard);

    // Should navigate to campaigns page
    expect(window.location.pathname).toBe('/campaigns');
  });
});

describe('Form Validation', () => {
  test('validates required fields in campaign creation', async () => {
    render(
      <TestWrapper>
        <CampaignsPage />
      </TestWrapper>
    );

    // Switch to create tab
    const createTab = screen.getByText('Создать кампанию');
    fireEvent.click(createTab);

    // Try to submit without filling required fields
    const submitButton = screen.getByText('Создать кампанию');
    fireEvent.click(submitButton);

    // Should show validation errors
    await waitFor(() => {
      expect(screen.getByText('Название обязательно')).toBeInTheDocument();
      expect(screen.getByText('Описание обязательно')).toBeInTheDocument();
      expect(screen.getByText('Категория обязательна')).toBeInTheDocument();
    });
  });

  test('validates amount limits in campaign creation', async () => {
    render(
      <TestWrapper>
        <CampaignsPage />
      </TestWrapper>
    );

    // Switch to create tab
    const createTab = screen.getByText('Создать кампанию');
    fireEvent.click(createTab);

    const amountInput = screen.getByLabelText('Целевая сумма (₽) *');
    
    // Test minimum amount
    fireEvent.change(amountInput, { target: { value: '500' } });
    fireEvent.click(screen.getByText('Создать кампанию'));

    await waitFor(() => {
      expect(screen.getByText('Минимум 1,000 ₽')).toBeInTheDocument();
    });

    // Test maximum amount
    fireEvent.change(amountInput, { target: { value: '15000000' } });
    fireEvent.click(screen.getByText('Создать кампанию'));

    await waitFor(() => {
      expect(screen.getByText('Максимум 10,000,000 ₽')).toBeInTheDocument();
    });
  });
});

describe('Telegram Integration', () => {
  test('initializes Telegram WebApp', () => {
    render(
      <TestWrapper>
        <HomePage />
      </TestWrapper>
    );

    expect(mockTelegramWebApp.ready).toHaveBeenCalled();
  });

  test('handles haptic feedback', () => {
    render(
      <TestWrapper>
        <HomePage />
      </TestWrapper>
    );

    const donateCard = screen.getByText('Разовое пожертвование');
    fireEvent.click(donateCard);

    expect(mockTelegramWebApp.HapticFeedback.impactOccurred).toHaveBeenCalledWith('light');
  });
});

describe('Error Handling', () => {
  test('handles API errors gracefully', async () => {
    // Mock API error
    global.fetch = jest.fn().mockRejectedValue(new Error('API Error'));

    render(
      <TestWrapper>
        <CampaignsPage />
      </TestWrapper>
    );

    // Should not crash and show loading state
    expect(screen.getByText('Загрузка кампаний...')).toBeInTheDocument();
  });
});

describe('Accessibility', () => {
  test('has proper ARIA labels', () => {
    render(
      <TestWrapper>
        <ZakatCalculatorPage />
      </TestWrapper>
    );

    const cashInput = screen.getByLabelText('Наличные дома');
    expect(cashInput).toHaveAttribute('type', 'number');
  });

  test('has proper form labels', () => {
    render(
      <TestWrapper>
        <CampaignsPage />
      </TestWrapper>
    );

    // Switch to create tab
    const createTab = screen.getByText('Создать кампанию');
    fireEvent.click(createTab);

    expect(screen.getByLabelText('Название кампании *')).toBeInTheDocument();
    expect(screen.getByLabelText('Описание *')).toBeInTheDocument();
  });
});
