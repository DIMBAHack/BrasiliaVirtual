// src/components/Analysis/AutonomyScore.jsx
import './AutonomyScore.css';

const AutonomyScore = ({ percent }) => {
  // Define a cor da barra com base na porcentagem
  const getBarColor = (p) => {
    if (p > 70) return '#4caf50'; // Verde
    if (p > 40) return '#ff9800'; // Laranja
    return '#f44336'; // Vermelho
  };

  return (
    <div className="autonomy-score-container">
      <p className="score-label">Score de autonomia</p>
      <div className="progress-bg">
        <div 
          className="progress-fill" 
          style={{ 
            width: `${percent}%`, 
            backgroundColor: getBarColor(percent) 
          }}
        ></div>
      </div>
      <p className="score-desc">
        <strong>{percent}%</strong> — {percent > 50 ? 'autonomia moderada' : 'baixa autonomia'}
      </p>
    </div>
  );
};

export default AutonomyScore;