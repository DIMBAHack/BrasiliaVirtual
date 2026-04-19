// src/pages/Home.jsx
import { useState } from 'react';
import { GoogleLogin } from '@react-oauth/google';
import { useNavigate, Link } from 'react-router-dom';
import './home.css';

function Home() {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleGoogleSuccess = (credentialResponse) => {
    console.log("Login realizado com sucesso! Token:", credentialResponse.credential);
    // Integração pra API
    navigate('/minhasanalises'); 
  };

  const handleGoogleError = () => {
    alert('Erro ao tentar logar com o Google.');
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Tentando login com:", { email, password });
    // TODO: Lógica de login com email/senha aqui
    // Se sucesso:
    navigate('/minhasanalises');
  };

  return (
    <div className="home-overlay">
      <div className="login-modal">
        <form className="modal-body" onSubmit={handleSubmit}>
          <h3>Bem-vindo!</h3>
          <p>Entre com seus dados para continuar.</p>

          <div className="form-group">
            <label htmlFor="email">Email</label>
            <input 
              type="email" 
              id="email" 
              value={email} 
              onChange={(e) => setEmail(e.target.value)} 
              placeholder="seuemail@exemplo.com"
              required 
            />
          </div>

          <div className="form-group">
            <div className="label-wrapper">
              <label htmlFor="password">Senha</label>
              <Link to="/esqueci-senha" className="forgot-password-link">Esqueci senha</Link>
            </div>
            <input 
              type="password" 
              id="password" 
              value={password} 
              onChange={(e) => setPassword(e.target.value)} 
              placeholder="Sua senha"
              required 
            />
          </div>

          <button type="submit" className="login-btn">Entrar</button>

          <div className="separator">
            <span className="separator-line"></span>
            <span className="separator-text">ou</span>
            <span className="separator-line"></span>
          </div>
          
          <div className="google-btn-wrapper">
            <GoogleLogin
              onSuccess={handleGoogleSuccess}
              onError={handleGoogleError}
              shape="pill"
              theme="outline"
              size="large"
              text="signin_with"
              locale="pt-BR"
            />
          </div>
        </form>

        <footer className="modal-footer">
          <p>Não tem uma conta? <Link to="/cadastro" className="signup-link">Cadastre-se</Link></p>
        </footer>
      </div>
    </div>
  );
}

export default Home;