import React from 'react';
import { useNavigate } from 'react-router-dom';
import './AnalysisCard.css';

// Mapeamento de tipos de indícios para cores e ícones para consistência visual
const findingMeta = {
  'Escrita similar à IA': { icon: '🤖', color: '#ff8c69' },
  'Similaridade com fontes online': { icon: '🔗', color: '#7fb3d5' },
  'Fonte potencialmente não confiável': { icon: '⚠️', color: '#f3cc8a' },
};

function AnalysisCard({ id, title, date, studentName, findings }) {
  const navigate = useNavigate();

  // Navega para a página de análise detalhada ao clicar
  const handleCardClick = () => {
    navigate(`/analise/${id}`); // Rota para a página de análise detalhada
  };

  return (
    <div className="analysis-card" onClick={handleCardClick} role="button" tabIndex="0">
      <div className="card-header">
        <h3 className="card-title">{title}</h3>
        <span className="card-date">{date}</span>
      </div>
      <div className="card-body">
        <p className="card-student">Enviado por: {studentName}</p>
        
        <div className="findings-section">
          <h4 className="findings-title">Indícios Detectados:</h4>
          {findings && findings.length > 0 ? (
            <ul className="findings-list">
              {findings.map((finding, index) => (
                <li key={index} className="finding-item">
                  <span 
                    className="finding-icon" 
                    style={{ backgroundColor: findingMeta[finding.type]?.color || '#ccc' }}
                    aria-label={finding.type}
                  >
                    {findingMeta[finding.type]?.icon}
                  </span>
                  <span className="finding-text">
                    {finding.count} trecho(s) com características de <strong>{finding.type}</strong>
                  </span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="no-findings-text">Nenhum indício notável detectado.</p>
          )}
        </div>
      </div>
      <div className="card-footer">
        <span className="view-details-link">Ver detalhes</span>
      </div>
    </div>
  );
}

export default AnalysisCard;