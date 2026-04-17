// src/pages/Analysis.jsx
import React from 'react';
import FilterBar from '../components/Analise/FilterBar';
import TextDisplay from '../components/Analise/TextDisplay';
import OccurrenceCard from '../components/Analise/OccurrenceCard';
import AutonomyScore from '../components/Analise/AutonomyScore';
import './Analysis.css';

function AnalysisPage() {
  const textContent = (
    <div className="text-content-wrapper">
      <p>
        A fotossíntese é o processo pelo qual as plantas convertem luz solar em energia química... 
        <span className="hl-ia">
          pois garante a produção de oxigênio e a fixação de carbono de forma sistemática...
          <span className="tag-inline">IA</span>
        </span>
      </p>
      <p>
        O processo ocorre principalmente nos cloroplastos das células vegetais.
        <span className="hl-plagio">
          "A reação geral pode ser simplificada..."
          <span className="tag-inline">PLÁGIO</span>
        </span>
      </p>
    </div>
  );

  return (
    <div className="analysis-screen">
      <div className="analysis-container">
        <header className="analysis-header">
          <div className="header-info">
            <h2>Painel de Análise</h2>
            <p>Verificador de IA</p>
          </div>
          <FilterBar />
        </header>

        <main className="analysis-main">
          {/* Lado Esquerdo */}
          <section className="text-section">
            <TextDisplay textContent={textContent} />
          </section>
          
          {/* Lado Direito */}
          <aside className="side-panel">
            <div className="occurrences-header">
              <h3>Ocorrências Detectadas</h3>
              <div className="divider-small"></div>
            </div>
            
            <div className="cards-stack">
              <OccurrenceCard 
                tipo="GERADO POR IA" 
                cor="#ff8c69"
                trecho="...de forma sistemática..."
                detalhe="Tom enciclopédico uniforme"
              />
              <OccurrenceCard 
                tipo="PLÁGIO" 
                cor="#007bff"
                trecho="A reação geral pode ser simplificada..."
                detalhe="Wikipedia — sem citação"
              />
            </div>

            <div className="score-section">
              <AutonomyScore percent={55} />
            </div>
          </aside>
        </main>
      </div>
    </div>
  );
}

export default AnalysisPage;