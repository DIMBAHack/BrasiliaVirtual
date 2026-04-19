import React from 'react';
import { useNavigate } from 'react-router-dom';
import './home.css'; // Estilos para o modal de login
import './HomePageContent.css'; // Estilos para o conteúdo da página inicial

function HomePage() {
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    // Lógica de autenticação aqui
    // Após o login bem-sucedido:
    navigate('/minhasanalises');
  };

  return (
    <div className="home-page-content">
      <section className="hero-section">
        <div className="hero-content">
          <h1>Análise Inteligente de Documentos</h1>
          <p className="subtitle">Detecte plágio e uso de IA com precisão e rapidez.</p>
          <p className="description">
            Nossa ferramenta avançada oferece uma análise detalhada para garantir a integridade acadêmica e profissional de seus documentos.
          </p>
          
          <div className="login-modal">
            <div className="modal-header">
              <h1>Acessar Plataforma</h1>
              <div className="divider"></div>
            </div>
            <form className="modal-body" onSubmit={handleLogin}>
              <div className="form-group">
                <label htmlFor="email">Email</label>
                <input type="email" id="email" placeholder="seuemail@dominio.com" required />
              </div>
              <div className="form-group">
                <div className="label-wrapper">
                  <label htmlFor="password">Senha</label>
                  <a href="#" className="forgot-password-link">Esqueceu?</a>
                </div>
                <input type="password" id="password" placeholder="Sua senha" required />
              </div>
              <button type="submit" className="login-btn">Entrar</button>
            </form>
            <div className="modal-footer">
              <p>
                Não tem uma conta? 
                <a href="#" className="signup-link">Cadastre-se</a>
              </p>
            </div>
          </div>

        </div>
      </section>
    </div>
  );
}

export default HomePage;