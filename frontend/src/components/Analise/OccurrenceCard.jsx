// src/components/Analise/OccurrenceCard.jsx
import { useState } from 'react';
import './OccurrenceCard.css';

function OccurrenceCard({ tipo, trecho, detalhe, cor }) {
  const [open, setOpen] = useState(false);

  return (
    <>
      <div
        className="occurrence-card"
        style={{ '--accent-color': cor }}
        onClick={() => setOpen(true)}
        role="button"
        tabIndex={0}
        onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') setOpen(true); }}
        aria-label={`Abrir detalhe da ocorrência: ${tipo}`}
      >
        <span className="card-label">{tipo}</span>
        <p className="card-trecho">"{trecho}"</p>
        <p className="card-detalhe">{detalhe}</p>
      </div>

      {open && (
        <div className="occurrence-modal-overlay" onClick={() => setOpen(false)}>
          <div className="occurrence-modal" role="dialog" aria-modal="true" aria-labelledby="occurrence-title" onClick={(e) => e.stopPropagation()}>
            <header className="occurrence-modal-header">
              <h2 id="occurrence-title">{tipo}</h2>
              <button className="occurrence-modal-close" onClick={() => setOpen(false)} aria-label="Fechar">×</button>
            </header>

            <div className="occurrence-modal-body">
              <h3 className="modal-section-title">Trecho</h3>
              <blockquote className="modal-trecho">{trecho}</blockquote>

              <h3 className="modal-section-title">Detalhes</h3>
              <p className="modal-detalhe">{detalhe}</p>
            </div>

            <footer className="occurrence-modal-footer">
              <button className="btn btn-secondary" onClick={() => setOpen(false)}>Fechar</button>
            </footer>
          </div>
        </div>
      )}
    </>
  );
}

export default OccurrenceCard;