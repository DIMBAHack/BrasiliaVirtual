import React from 'react';
import './AnalysisCard.css';

// Componente para a barra de pontuação
const ScoreBar = ({ label, score, color }) => (
  <div className="score-bar-container">
    <div className="score-bar-labels">
      <span>{label}</span>
      <span>{score}%</span>
    </div>
    <div className="score-bar-background">
      <div className="score-bar-fill" style={{ width: `${score}%`, backgroundColor: color }}></div>
    </div>
  </div>
);

function AnalysisCard({ title, date, studentName, iaScore, plagiarismScore }) {
  return (
    <div className="analysis-card">
      <div className="card-header">
        <h3 className="card-title">{title}</h3>
        <div className="card-meta">
          <span className="card-date">{date}</span>
          {studentName && (
            <span className="card-student">{studentName}</span>
          )}
        </div>
      </div>
      <div className="card-body">
        <ScoreBar label="Autenticidade IA" score={iaScore} color="#0062ff" />
        <ScoreBar label="Plágio Detectado" score={plagiarismScore} color="#ff4d4d" />
      </div>
      <div className="card-footer">
        <a href="/analise" className="card-link">Ver Análise Completa</a>
      </div>
    </div>
  );
}

export default AnalysisCard;