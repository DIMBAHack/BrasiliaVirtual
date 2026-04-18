import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom'; // Importe aqui
import { GoogleOAuthProvider } from '@react-oauth/google';
import App from './App';
import './index.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <GoogleOAuthProvider clientId="SEU_CLIENT_ID_REAL_AQUI"> {/* Substitua pelo seu Client ID real */}
      {/* O BrowserRouter deve envolver o App todo */}
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </GoogleOAuthProvider>
  </React.StrictMode>
);