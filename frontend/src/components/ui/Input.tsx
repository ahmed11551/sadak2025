import styled from 'styled-components';

export const Label = styled.label`
  font-size: 14px;
  font-weight: 600;
  color: var(--tg-text-color, #000000);
`;

const Input = styled.input`
  padding: 12px 16px;
  border: 2px solid #e9ecef;
  border-radius: 12px;
  font-size: 16px;
  background: var(--tg-bg-color, #ffffff);
  color: var(--tg-text-color, #000000);
  transition: border-color 0.2s;

  &:focus { outline: none; border-color: #007bff; }
  &:disabled { background: #f8f9fa; cursor: not-allowed; }
`;

export default Input;


