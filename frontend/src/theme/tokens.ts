export const colors = {
  primary: '#007bff',
  primaryDark: '#0056b3',
  secondary: '#6c757d',
  success: '#28a745',
  danger: '#dc3545',
  warning: '#ffc107',
  info: '#17a2b8',
  light: '#f8f9fa',
  dark: '#343a40',
  border: '#e9ecef',
  text: 'var(--tg-text-color, #000000)',
  background: 'var(--tg-bg-color, #ffffff)'
};

export const spacing = {
  xs: '4px',
  sm: '8px',
  md: '16px',
  lg: '24px',
  xl: '32px'
};

export const radii = {
  sm: '4px',
  md: '8px',
  lg: '12px',
  xl: '16px'
};

export const typography = {
  fontFamily: `-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue', sans-serif`,
  baseSize: '16px'
};

export type DesignTokens = {
  colors: typeof colors;
  spacing: typeof spacing;
  radii: typeof radii;
  typography: typeof typography;
};

export const tokens: DesignTokens = { colors, spacing, radii, typography };


