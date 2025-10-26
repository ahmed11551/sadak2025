import React, { Component, ReactNode } from 'react';
import styled from 'styled-components';

const ErrorContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  padding: 20px;
  text-align: center;
`;

const ErrorTitle = styled.h2`
  color: #dc3545;
  margin-bottom: 16px;
`;

const ErrorMessage = styled.p`
  color: #6c757d;
  margin-bottom: 20px;
`;

const RetryButton = styled.button`
  padding: 12px 24px;
  background: var(--tg-button-color, #007bff);
  color: var(--tg-button-text-color, #ffffff);
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  
  &:hover {
    opacity: 0.9;
  }
`;

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: any) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <ErrorContainer>
          <ErrorTitle>Что-то пошло не так</ErrorTitle>
          <ErrorMessage>
            Произошла неожиданная ошибка. Пожалуйста, попробуйте обновить страницу.
          </ErrorMessage>
          <RetryButton onClick={() => window.location.reload()}>
            Обновить страницу
          </RetryButton>
        </ErrorContainer>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
