import { useNavigate } from 'react-router-dom';
import './HomePageContent.css';

function HomePageContent() {
  const navigate = useNavigate();

  return (
    <div className="home-page-content">
      <section className="hero-section">
        <div className="hero-content">
          <h1>DMD Análise</h1>
          <p className="subtitle">Plataforma inteligente para detecção de integridade acadêmica</p>
          <p className="description">
            Identifique IA, plágio e verifique autenticidade de trabalhos com precisão
          </p>
          
          <button className="btn btn-primary" onClick={() => navigate('/login')}>
            Começar
          </button>
        </div>
      </section>
    </div>
  );
}

export default HomePageContent;