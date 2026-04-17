// src/components/Analise/OccurrenceCard.jsx
import './OccurrenceCard.css';

function OccurrenceCard({ tipo, trecho, detalhe, cor }) {
  return (
    <div 
      className="occurrence-card" 
      style={{ '--accent-color': cor }} // Passa a cor para o CSS
    >
      <span className="card-label">{tipo}</span>
      <p className="card-trecho">"{trecho}"</p>
      <p className="card-detalhe">{detalhe}</p>
    </div>
  );
}

export default OccurrenceCard;