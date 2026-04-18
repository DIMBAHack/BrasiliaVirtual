// src/components/Header/Header.jsx
import React, { useState } from 'react';
import './Header.css';
import UploadModal from './pages/UploadModal';

function Header({ isSidebarOpen, toggleSidebar }) {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleNewAnalysis = () => {
    setIsModalOpen(true);
  };

  return (
    <>
      <header className="app-header">
        <div className="header-content">
          <div className="header-left">
            <button
              className={`sidebar-toggle-btn ${isSidebarOpen ? 'open' : 'closed'}`}
              onClick={toggleSidebar}
              aria-label={isSidebarOpen ? "Fechar menu" : "Abrir menu"}
            >
              <span className="hamburger-icon"></span>
            </button>

            <div className="header-logo">
              <span className="logo-icon">BV</span>
              <h2>Brasília<span>Virtual</span></h2>
            </div>
          </div>

          <div className="header-right">
            <button className="new-analysis-btn" onClick={handleNewAnalysis}>
              <span className="icon-plus">+</span>
              Nova Análise
            </button>
          </div>
        </div>
      </header>
      <UploadModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
    </>
  );
}

export default Header;