import './MyAnalysesPage.css';
import { useState } from 'react';
import AnalysisCard from './AnalysisCard';
import UploadModal from './UploadModal';

// Dados fictícios para os cards
const mockAnalyses = [
  {
    id: 1,
    title: 'Análise do Relatório Trimestral Q3',
    date: '15 de Julho, 2024',
    studentName: 'Ana Carolina',
    iaScore: 85,
    plagiarismScore: 10,
  },
  {
    id: 2,
    title: 'Tese de Doutorado - Capítulo 2',
    date: '11 de Julho, 2024',
    studentName: 'Marcos Vinícius',
    iaScore: 92,
    plagiarismScore: 5,
  },
  {
    id: 3,
    title: 'Artigo sobre Inteligência Artificial na Saúde',
    date: '05 de Julho, 2024',
    studentName: 'Beatriz Lima',
    iaScore: 78,
    plagiarismScore: 22,
  },
];

function MyAnalysesPage() {
  // TODO: Substitua este estado por uma lógica real para verificar se há análises
  const [analyses, setAnalyses] = useState(mockAnalyses); 

  const [isModalOpen, setIsModalOpen] = useState(false);

  return (
    <div className={`my-analyses-page ${analyses.length > 0 ? 'has-analyses' : ''}`}>
      <div className="analyses-container">
        <div className="page-header">
          <h2 className="page-title">Minhas Análises</h2>
          <button className="new-analysis-btn" onClick={() => setIsModalOpen(true)}>
            <span className="icon-plus">+</span>
            Nova Análise
          </button>
        </div>

        {analyses.length > 0 ? (
          <div className="analyses-grid">
            {analyses.map(analysis => (
              <AnalysisCard key={analysis.id} {...analysis} />
            ))}
          </div>
        ) : (
          <div className="no-analyses-placeholder">
            <p className="no-analyses-text">Nenhuma análise realizada</p>
          </div>
        )}
      </div>

      <UploadModal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} />
    </div>
  );
}

export default MyAnalysesPage;