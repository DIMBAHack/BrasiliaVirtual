import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { useNavigate } from 'react-router-dom';
import './UploadModal.css';

const UploadIcon = () => (
  <svg width="64" height="64" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M12 16.5V3M12 3L16.5 7.5M12 3L7.5 7.5" stroke="#0062ff" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M21 12V19.5C21 20.3284 20.3284 21 19.5 21H4.5C3.67157 21 3 20.3284 3 19.5V12" stroke="#0062ff" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
  </svg>
);

function UploadModal({ isOpen, onClose }) {
  const [file, setFile] = useState(null);
  const [authorName, setAuthorName] = useState('');
  const [documentTitle, setDocumentTitle] = useState('');
  const navigate = useNavigate();

  const onDrop = useCallback(acceptedFiles => {
    if (acceptedFiles && acceptedFiles.length > 0) {
      setFile(acceptedFiles[0]);
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/plain': ['.txt'],
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    },
    maxFiles: 1
  });

  const handleAnalyse = () => {
    if (file && authorName && documentTitle) {
      // Em um app real, aqui você faria a chamada para a API com os dados do formulário.
      // A API retornaria um ID de análise, que seria usado para navegar para a página de resultados.
      console.log("Iniciando análise:", file.name, "Autor:", authorName, "Título:", documentTitle);
      
      // Fecha o modal e navega para a tela de carregamento, passando os dados via state.
      onClose();
      navigate('/analisando', { state: { documentTitle, authorName } });
    }
  };

  const handleClose = () => {
    setFile(null);
    setAuthorName('');
    setDocumentTitle('');
    onClose();
  };

  if (!isOpen) {
    return null;
  }

  return (
    <div className="modal-overlay" onClick={handleClose}>
      <div className="modal-content" onClick={e => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Iniciar Nova Análise</h2>
          <button className="close-btn" onClick={handleClose}>&times;</button>
        </div>
        <div className="modal-body">
          <div className="form-group">
            <label htmlFor="authorName">Nome do Autor</label>
            <input
              type="text"
              id="authorName"
              value={authorName}
              onChange={(e) => setAuthorName(e.target.value)}
              placeholder="Digite o nome do autor do documento"
            />
          </div>
          <div className="form-group">
            <label htmlFor="documentTitle">Título do Documento</label>
            <input
              type="text"
              id="documentTitle"
              value={documentTitle}
              onChange={(e) => setDocumentTitle(e.target.value)}
              placeholder="Ex: Relatório Trimestral Q3"
            />
          </div>
          <div {...getRootProps({ className: `dropzone ${isDragActive ? 'active' : ''}` })}>
            <input {...getInputProps()} />
            <div className="dropzone-content">
              <UploadIcon />
              {file ? (
                <div className="file-info"><p><strong>Arquivo:</strong> {file.name}</p></div>
              ) : (
                <p>Arraste e solte o arquivo aqui, ou <strong>clique para selecionar</strong></p>
              )}
              <div className="file-types"><p>Formatos suportados: TXT, PDF, DOCX</p></div>
            </div>
          </div>
        </div>
        <div className="modal-footer">
          <button className="cancel-btn" onClick={handleClose}>Cancelar</button>
          <button className="analyse-btn" onClick={handleAnalyse} disabled={!file || !authorName || !documentTitle}>Analisar</button>
        </div>
      </div>
    </div>
  );
}

export default UploadModal;