import { TelegramWebApp } from '../types';

declare global {
  interface Window {
    Telegram?: {
      WebApp: TelegramWebApp;
    };
  }
}

class TelegramService {
  private webApp: TelegramWebApp | null = null;
  private isInitialized = false;

  constructor() {
    this.init();
  }

  private init(): void {
    if (typeof window !== 'undefined' && window.Telegram?.WebApp) {
      this.webApp = window.Telegram.WebApp;
      this.webApp.ready();
      this.isInitialized = true;
      
      // Настраиваем тему
      this.setupTheme();
      
      // Настраиваем кнопки
      this.setupButtons();
    }
  }

  private setupTheme(): void {
    if (!this.webApp) return;

    // Применяем цвета Telegram
    const themeParams = this.webApp.themeParams;
    if (themeParams.bg_color) {
      document.documentElement.style.setProperty('--tg-bg-color', themeParams.bg_color);
    }
    if (themeParams.text_color) {
      document.documentElement.style.setProperty('--tg-text-color', themeParams.text_color);
    }
    if (themeParams.button_color) {
      document.documentElement.style.setProperty('--tg-button-color', themeParams.button_color);
    }
    if (themeParams.button_text_color) {
      document.documentElement.style.setProperty('--tg-button-text-color', themeParams.button_text_color);
    }
  }

  private setupButtons(): void {
    if (!this.webApp) return;

    // Настраиваем главную кнопку
    this.webApp.MainButton.setText('Продолжить');
    this.webApp.MainButton.hide();

    // Настраиваем кнопку "Назад"
    this.webApp.BackButton.hide();
  }

  public getWebApp(): TelegramWebApp | null {
    return this.webApp;
  }

  public isReady(): boolean {
    return this.isInitialized && this.webApp !== null;
  }

  public getUser(): TelegramWebApp['initDataUnsafe']['user'] | null {
    return this.webApp?.initDataUnsafe.user || null;
  }

  public getInitData(): string {
    return this.webApp?.initData || '';
  }

  public getTheme(): 'light' | 'dark' {
    return this.webApp?.colorScheme || 'light';
  }

  public showMainButton(text: string, onClick: () => void): void {
    if (!this.webApp) return;

    this.webApp.MainButton.setText(text);
    this.webApp.MainButton.onClick(onClick);
    this.webApp.MainButton.show();
  }

  public hideMainButton(): void {
    if (!this.webApp) return;
    this.webApp.MainButton.hide();
  }

  public enableMainButton(): void {
    if (!this.webApp) return;
    this.webApp.MainButton.enable();
  }

  public disableMainButton(): void {
    if (!this.webApp) return;
    this.webApp.MainButton.disable();
  }

  public showBackButton(onClick: () => void): void {
    if (!this.webApp) return;

    this.webApp.BackButton.onClick(onClick);
    this.webApp.BackButton.show();
  }

  public hideBackButton(): void {
    if (!this.webApp) return;
    this.webApp.BackButton.hide();
  }

  public showAlert(message: string): Promise<void> {
    return new Promise((resolve) => {
      if (!this.webApp) {
        alert(message);
        resolve();
        return;
      }

      this.webApp.showAlert(message, () => {
        resolve();
      });
    });
  }

  public showConfirm(message: string): Promise<boolean> {
    return new Promise((resolve) => {
      if (!this.webApp) {
        const result = confirm(message);
        resolve(result);
        return;
      }

      this.webApp.showConfirm(message, (confirmed) => {
        resolve(confirmed);
      });
    });
  }

  public showPopup(params: {
    title?: string;
    message: string;
    buttons?: Array<{
      id?: string;
      type?: 'default' | 'ok' | 'close' | 'cancel' | 'destructive';
      text?: string;
    }>;
  }): Promise<string | null> {
    return new Promise((resolve) => {
      if (!this.webApp) {
        const result = confirm(params.message);
        resolve(result ? 'ok' : 'cancel');
        return;
      }

      this.webApp.showPopup(params, (buttonId) => {
        resolve(buttonId);
      });
    });
  }

  public hapticFeedback(type: 'impact' | 'notification' | 'selection', style?: 'light' | 'medium' | 'heavy' | 'rigid' | 'soft' | 'error' | 'success' | 'warning'): void {
    if (!this.webApp) return;

    switch (type) {
      case 'impact':
        if (style && ['light', 'medium', 'heavy', 'rigid', 'soft'].includes(style)) {
          this.webApp.HapticFeedback.impactOccurred(style as 'light' | 'medium' | 'heavy' | 'rigid' | 'soft');
        }
        break;
      case 'notification':
        if (style && ['error', 'success', 'warning'].includes(style)) {
          this.webApp.HapticFeedback.notificationOccurred(style as 'error' | 'success' | 'warning');
        }
        break;
      case 'selection':
        this.webApp.HapticFeedback.selectionChanged();
        break;
    }
  }

  public openLink(url: string, options?: { try_instant_view?: boolean }): void {
    if (!this.webApp) {
      window.open(url, '_blank');
      return;
    }

    this.webApp.openLink(url, options);
  }

  public openTelegramLink(url: string): void {
    if (!this.webApp) {
      window.open(url, '_blank');
      return;
    }

    this.webApp.openTelegramLink(url);
  }

  public close(): void {
    if (!this.webApp) return;
    this.webApp.close();
  }

  public expand(): void {
    if (!this.webApp) return;
    this.webApp.expand();
  }

  public sendData(data: string): void {
    if (!this.webApp) return;
    this.webApp.sendData(data);
  }

  public getViewportHeight(): number {
    return this.webApp?.viewportHeight || window.innerHeight;
  }

  public getViewportStableHeight(): number {
    return this.webApp?.viewportStableHeight || window.innerHeight;
  }

  public isExpanded(): boolean {
    return this.webApp?.isExpanded || false;
  }
}

// Создаем единственный экземпляр сервиса
const telegramService = new TelegramService();

export default telegramService;
