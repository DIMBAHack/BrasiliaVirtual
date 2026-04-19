// src/App.jsx
import { useLocation } from 'react-router-dom';
import { useState } from 'react';
import Header from './Header';
import Sidebar from './components/Sidebar';
import AppRoutes from './AppRoutes';
import './App.css';

function App() {
  const location = useLocation();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false); // Inicia o menu fechado

  // Define as rotas onde a Sidebar NÃO deve aparecer (home e login)
  const hideSidebar = location.pathname === '/' || location.pathname === '/login';
  const hideHeader = location.pathname === '/login';

  const toggleSidebar = () => {
    setIsSidebarOpen(prev => !prev);
  };

  return (
    <div className={`app-layout ${hideSidebar ? 'no-sidebar-path' : ''} ${hideHeader ? 'no-header' : ''} ${!isSidebarOpen && !hideSidebar ? 'sidebar-closed-layout' : ''}`}>
      {/* Header aparece em todas as rotas exceto login */}
      {!hideHeader && <Header isSidebarOpen={isSidebarOpen} toggleSidebar={toggleSidebar} />}
      {/* Renderiza a Sidebar apenas se não for uma rota de esconder (ex: login e home) */}
      {!hideSidebar && <Sidebar />}
      <main className="content-area">
        <AppRoutes />
      </main>
    </div>
  );
}

export default App;