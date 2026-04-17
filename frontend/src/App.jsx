// src/App.jsx
import { useLocation } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import AppRoutes from './AppRoutes';
import './App.css';

function App() {
  const location = useLocation();

  // Define as rotas onde a Sidebar NÃO deve aparecer
  const hideSidebar = location.pathname === '/';

  return (
    <div className={`app-layout ${hideSidebar ? 'no-sidebar' : ''}`}>
      {/* Renderização Condicional: Só renderiza se não for a home */}
      {!hideSidebar && <Sidebar />}
      
      <main className="content-area">
        <AppRoutes />
      </main>
    </div>
  );
}

export default App;