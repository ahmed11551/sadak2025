import { createGlobalStyle } from 'styled-components';
import { tokens } from './tokens';

export const GlobalStyle = createGlobalStyle`
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: ${tokens.typography.fontFamily};
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    background-color: ${tokens.colors.background};
    color: ${tokens.colors.text};
    line-height: 1.6;
  }
  #root { min-height: 100vh; display: flex; flex-direction: column; }
`;

export const theme = {
  colors: tokens.colors,
  spacing: tokens.spacing,
  borderRadius: tokens.radii
};

export type AppTheme = typeof theme;


