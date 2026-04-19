import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './AnalysisLoadingPage.css';

// Mensagens que simulam os passos da análise do backend (ia_service.py)
const loadingSteps = [
  "Iniciando motor DMBAnálise...",
  "Coletando referências de IA...",
  "Carregando modelo de perplexidade (GPT-2)...",
  "Analisando trecho 1...",
  "Verificando similaridade online...",
  "Analisando trecho 2...",
  "Compilando resultados...",
  "Quase pronto!",
];

function AnalysisLoadingPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const [currentStep, setCurrentStep] = useState(0);

  const { documentTitle, authorName } = location.state || { documentTitle: 'Novo Documento', authorName: 'Desconhecido' };

  useEffect(() => {
    // Simula a progressão das etapas de carregamento
    const stepInterval = setInterval(() => {
      setCurrentStep(prevStep => {
        if (prevStep < loadingSteps.length - 1) {
          return prevStep + 1;
        }
        return prevStep; // Mantém na última etapa
      });
    }, 1000); // Muda a cada 1 segundo

    // Simula o tempo total da análise
    const analysisTimeout = setTimeout(() => {
      clearInterval(stepInterval);
      // Em um app real, o ID viria da resposta da API.
      // Aqui, vamos usar um ID fixo para o exemplo e redirecionar.
      const newAnalysisId = 1; 
      navigate(`/analise/${newAnalysisId}`);
    }, loadingSteps.length * 1000 + 500); // Tempo total

    return () => {
      clearInterval(stepInterval);
      clearTimeout(analysisTimeout);
    };
  }, [navigate]);

  return (
    <div className="loading-screen">
      <div className="loading-content">
        <div className="scanner-animation"></div>
        <h1 className="loading-title">Analisando Documento</h1>
        <p className="loading-subtitle">"{documentTitle}" por {authorName}</p>
        <div className="loading-steps">
          <p>{loadingSteps[currentStep]}</p>
        </div>
      </div>
    </div>
  );
}

export default AnalysisLoadingPage;