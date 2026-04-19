// src/components/Sidebar/Sidebar.jsx
import { NavLink, useNavigate } from 'react-router-dom';
import { googleLogout } from '@react-oauth/google'; // Importe para limpar a sessão do Google
import './Sidebar.css';

// As props 'isSidebarOpen' e 'toggleSidebar' não são mais necessárias aqui.
// O estado de abertura/fechamento é gerenciado pelo componente pai (App.jsx)
// através de classes no elemento '.app-layout'.
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
    // A classe 'sidebar-closed' foi removida. A animação de esconder/mostrar
    // é controlada pela classe '.sidebar-closed-layout' no elemento pai '.app-layout'
    // (definido em App.jsx e estilizado em App.css). Isso centraliza a lógica
    // de layout e evita conflitos de estilo.
    <aside className="sidebar">
      <nav className="sidebar-nav">
        <NavLink to="/minhasanalises" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
          <span className="nav-dot"></span>
          Minhas Análises
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