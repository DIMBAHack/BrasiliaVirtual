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

  // Define as rotas onde a Sidebar NÃO deve aparecer
  const hideSidebar = location.pathname === '/';

  const toggleSidebar = () => {
    setIsSidebarOpen(prev => !prev);
  };

  return (
    <div className={`app-layout ${hideSidebar ? 'no-sidebar-path' : ''} ${!isSidebarOpen && !hideSidebar ? 'sidebar-closed-layout' : ''}`}>
      {/* Renderiza o Header e a Sidebar apenas se não for uma rota de esconder */}
      {!hideSidebar && <Header isSidebarOpen={isSidebarOpen} toggleSidebar={toggleSidebar} />}
      {/* Renderiza a Sidebar apenas se não for uma rota de esconder (ex: login) */}
      {!hideSidebar && <Sidebar />}
      <main className="content-area">
        <AppRoutes />
      </main>
    </div>
  );
}

export default App;