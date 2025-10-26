import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// Telegram WebApp Script
const script = document.createElement('script');
script.src = 'https://telegram.org/js/telegram-web-app.js';
script.async = true;
document.head.appendChild(script);

const root = ReactDOM.createRoot(
  document.getElementById('root') as HTMLElement
);

root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
