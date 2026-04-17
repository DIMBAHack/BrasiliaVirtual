// src/components/Sidebar/Sidebar.jsx
import { NavLink, useNavigate } from 'react-router-dom';
import { googleLogout } from '@react-oauth/google'; // Importe para limpar a sessão do Google
import './Sidebar.css';

function Sidebar() {
  const navigate = useNavigate();

  // Função preparada para a API e Redirecionamento
  const handleLogout = async () => {
    try {
      // 1. Chamada para sua API futura (Python/FastAPI)
      // await api.post('/auth/logout'); 
      
      console.log("Encerrando sessão...");

      // 2. Limpa o login do Google no navegador
      googleLogout();

      // 3. Limpa dados locais (LocalStorage, Cookies, Estados)
      localStorage.removeItem('user_token'); // Exemplo de limpeza de token
      
      // 4. Redireciona para a Home
      navigate('/');
      
    } catch (error) {
      console.error("Erro ao deslogar:", error);
    }
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <span className="logo-icon">BV</span>
        <h2>Brasília<span>Virtual</span></h2>
      </div>

      <nav className="sidebar-nav">
        <NavLink to="/analise" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
          <span className="nav-dot"></span>
          Nova Análise
        </NavLink>
        
        <NavLink to="/historico" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
          <span className="nav-dot"></span>
          Histórico
        </NavLink>
      </nav>

      <div className="sidebar-footer">
        <div className="user-info">
          <div className="user-avatar">I</div>
          <p>Igor Oliveira</p>
        </div>
        
        {/* Acionando a função no clique */}
        <button className="logout-btn" onClick={handleLogout}>
          Sair
        </button>
      </div>
    </aside>
  );
}

export default Sidebar;