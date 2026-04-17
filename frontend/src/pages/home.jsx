// src/pages/Home.jsx
import { GoogleLogin } from '@react-oauth/google';
import { useNavigate } from 'react-router-dom';
import './home.css';

function Home() {
  const navigate = useNavigate();

  const handleSuccess = (credentialResponse) => {
    console.log("Login realizado com sucesso! Token:", credentialResponse.credential);
    // Integração pra API
    navigate('/analise'); 
  };

  const handleError = () => {
    alert('Erro ao tentar logar com o Google.');
  };

  return (
    <div className="home-overlay">
      <div className="login-modal">
        <header className="modal-header">   
          <h1>Verificador de IA</h1>
          <div className="divider"></div>
        </header>
        
        <div className="modal-body">
          <h3>Bem-vindo!</h3>
          <p>Entre com sua conta Google para iniciar sua análise de documento.</p>
          
          <div className="google-btn-wrapper">
            <GoogleLogin
              onSuccess={handleSuccess}
              onError={handleError}
              shape="pill"
              theme="outline"
              size="large"
              text="signin_with"
              locale="pt-BR"
            />
          </div>
        </div>

        <footer className="modal-footer">
        </footer>
      </div>
    </div>
  );
}

export default Home;