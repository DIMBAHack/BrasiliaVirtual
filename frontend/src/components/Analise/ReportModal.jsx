import React from 'react';
import './ReportModal.css';

const LoadingSpinner = () => (
  <div className="spinner-container">
    <div className="spinner"></div>
    <p>Gerando sugestões com base na análise...</p>
  </div>
);

const ReportModal = ({ isOpen, onClose, isLoading, reportContent, studentName }) => {
  if (!isOpen) {
    return null;
  }

  const handleCopy = () => {
    const textToCopy = document.querySelector('.report-modal-body')?.innerText;
    if (textToCopy) {
      navigator.clipboard.writeText(textToCopy)
        .then(() => alert('Relatório copiado para a área de transferência!'))
        .catch(err => console.error('Erro ao copiar texto: ', err));
    }
  };

  return (
    <div className="report-modal-overlay" onClick={onClose}>
      <div className="report-modal-content" onClick={e => e.stopPropagation()}>
        <div className="report-modal-header">
          <h3>Relatório Pedagógico</h3>
          <button className="report-modal-close-btn" onClick={onClose}>&times;</button>
        </div>
        <div className="report-modal-body">
          {isLoading ? (
            <LoadingSpinner />
          ) : (
            <div dangerouslySetInnerHTML={{ __html: reportContent }} />
          )}
        </div>
        <div className="report-modal-footer">
          <button className="report-modal-btn-secondary" onClick={onClose}>
            Fechar
          </button>
          <button 
            className="report-modal-btn-primary" 
            onClick={handleCopy}
            disabled={isLoading}
          >
            Copiar Relatório
          </button>
        </div>
      </div>
    </div>
  );
};

export default ReportModal;