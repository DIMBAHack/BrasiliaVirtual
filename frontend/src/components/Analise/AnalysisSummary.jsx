import React from 'react';
import './AnalysisSummary.css';

// Mapeamento de tipos de indícios para ícones, cores e rótulos
const findingMeta = {
  'GERADO POR IA': { icon: '🤖', color: '#ff8c69', label: 'Escrita por IA' },
  'PLÁGIO': { icon: '🔗', color: '#7fb3d5', label: 'Similaridade Online' },
  'FONTE NÃO CONFIÁVEL': { icon: '⚠️', color: '#f3cc8a', label: 'Fonte Não Confiável' },
};

function AnalysisSummary({ occurrences }) {
  // Calcula a contagem para cada tipo de ocorrência
  const summaryCounts = occurrences.reduce((acc, occurrence) => {
    const type = occurrence.tipo;
    acc[type] = (acc[type] || 0) + 1;
    return acc;
  }, {});

  const summaryItems = Object.entries(summaryCounts);

  if (summaryItems.length === 0) {
    return null; // Não renderiza a seção se não houver indícios
  }

  return (
    <section className="analysis-summary-section">
      <h3 className="summary-title">Resumo dos Indícios</h3>
      <div className="summary-cards-container">
        {summaryItems.map(([type, count]) => {
          const meta = findingMeta[type];
          if (!meta) return null;

          return (
            <div key={type} className="summary-card">
              <div className="summary-card-icon" style={{ backgroundColor: meta.color }}>
                {meta.icon}
              </div>
              <div className="summary-card-content">
                <span className="summary-card-count">{count}</span>
                <span className="summary-card-label">
                  {count > 1 ? 'Indícios de' : 'Indício de'} {meta.label}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}

export default AnalysisSummary;