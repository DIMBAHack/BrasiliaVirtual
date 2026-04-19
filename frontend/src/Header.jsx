// src/components/Header/Header.jsx
import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './Header.css';

function Header({ isSidebarOpen, toggleSidebar }) {
  const navigate = useNavigate();
  const location = useLocation();

  // Determina se está na página inicial ou login
  const isHomeOrLogin = location.pathname === '/' || location.pathname === '/login';

  return (
    <>
      <header className={`app-header ${location.pathname === '/' ? 'home-header' : ''}`}>
        <div className="header-content">
          <div className="header-left">
            {/* Botão hamburger só aparece se não for home/login */}
            {!isHomeOrLogin && (
              <button
                className={`sidebar-toggle-btn ${isSidebarOpen ? 'open' : 'closed'}`}
                onClick={toggleSidebar}
                aria-label={isSidebarOpen ? "Fechar menu" : "Abrir menu"}
              >
                <span className="hamburger-icon"></span>
              </button>
            )}

            <div className="header-logo" onClick={() => navigate('/')} role="button" tabIndex="0" aria-label="Ir para a página inicial">
              <h2>DMB<span>Análise</span></h2>
            </div>
          </div>

          <div className="header-right">
            {/* Na página inicial, mostra botão de login */}
            {location.pathname === '/' && (
              <button className="login-btn" onClick={() => navigate('/login')}>
                Fazer Login
              </button>
            )}
            
            {/* Em outras páginas, o botão de nova análise foi movido para o corpo da página */}
          </div>
        </div>
      </header>
      
    </>
  );
}

export default Header;