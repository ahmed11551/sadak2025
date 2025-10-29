import styled from 'styled-components';

const Button = styled.button<{ variant?: 'primary' | 'secondary' | 'danger'; disabled?: boolean }>`
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 12px 20px;
  border-radius: 8px;
  border: 0;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  background: ${({ variant }) =>
    variant === 'secondary'
      ? 'transparent'
      : variant === 'danger'
      ? '#dc3545'
      : 'var(--tg-button-color, #007bff)'};
  color: ${({ variant }) => (variant === 'secondary' ? 'var(--tg-text-color, #000000)' : 'var(--tg-button-text-color, #ffffff)')};
  border: ${({ variant }) => (variant === 'secondary' ? '2px solid #e9ecef' : 'none')};

  &:hover { opacity: 0.9; }
  &:disabled { opacity: 0.6; cursor: not-allowed; }
`;

export default Button;


