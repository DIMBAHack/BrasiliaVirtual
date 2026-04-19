// src/pages/Analysis.jsx
import React, { useState } from 'react';
import FilterBar from '../components/Analise/FilterBar';
import TextDisplay from '../components/Analise/TextDisplay';
import OccurrenceCard from '../components/Analise/OccurrenceCard';
import './Analysis.css';

function AnalysisPage() {
  const [showFullText, setShowFullText] = useState(true);
  const [activeFilter, setActiveFilter] = useState('Tudo');

  // Estrutura de dados para o conteúdo do texto e suas ocorrências
  const documentParagraphs = [
    [ // Parágrafo 1
      { type: 'normal', text: 'A fotossíntese é o processo pelo qual as plantas convertem luz solar em energia química... ' },
      { type: 'GERADO POR IA', text: 'pois garante a produção de oxigênio e a fixação de carbono de forma sistemática...' },
      { type: 'normal', text: ' Este processo é fundamental para a vida na Terra, pois além de produzir o oxigênio que respiramos, também serve como base para a maioria das cadeias alimentares.' }
    ],
    [ // Parágrafo 2
      { type: 'normal', text: 'O processo ocorre principalmente nos cloroplastos das células vegetais.' },
      { type: 'PLÁGIO', text: '"A reação geral pode ser simplificada..."' },
      { type: 'normal', text: ' A clorofila, pigmento verde presente nos cloroplastos, é a molécula chave que absorve a energia luminosa.' }
    ],
    [ // Parágrafo 3
      { type: 'normal', text: 'Existem dois estágios principais na fotossíntese: as reações dependentes de luz e o ciclo de Calvin. Nas reações de luz, a energia solar é capturada para produzir ATP e NADPH. ' },
      { type: 'FONTE NÃO CONFIÁVEL', text: 'Estudos recentes da Universidade de Stanford indicam que a eficiência quântica pode ser otimizada em laboratório.' },
    ],
    [ // Parágrafo 4
      { type: 'normal', text: 'O ciclo de Calvin, por sua vez, utiliza o ATP e o NADPH para converter dióxido de carbono em glicose, que a planta usa como alimento. Este ciclo é uma série complexa de reações bioquímicas que ocorrem no estroma dos cloroplastos.' }
    ],
    [ // Parágrafo 5
      { type: 'normal', text: 'Fatores como a intensidade da luz, a concentração de dióxido de carbono e a temperatura podem afetar a taxa de fotossíntese. ' },
      { type: 'GERADO POR IA', text: 'A otimização desses fatores é crucial para a agricultura moderna e para o desenvolvimento de biocombustíveis sustentáveis.' },
    ],
    [ // Parágrafo 6
      { type: 'normal', text: 'Em resumo, a fotossíntese não é apenas um processo biológico, mas um pilar que sustenta ecossistemas inteiros e influencia o clima global. A compreensão aprofundada de seus mecanismos continua a ser uma área de pesquisa ativa e de grande importância para o futuro da humanidade.' }
    ]
  ];

  const allOccurrences = [
    { id: 1, tipo: "GERADO POR IA", cor: "#ff8c69", trecho: "...de forma sistemática...", detalhe: "Tom enciclopédico uniforme" },
    { id: 2, tipo: "PLÁGIO", cor: "#7fb3d5", trecho: "A reação geral pode ser simplificada...", detalhe: "Wikipedia — sem citação" },
    { id: 3, tipo: "FONTE NÃO CONFIÁVEL", cor: "#f3cc8a", trecho: "Estudos recentes da Universidade de Stanford...", detalhe: "Fonte acadêmica, mas sem link ou citação formal." },
    { id: 4, tipo: "GERADO POR IA", cor: "#ff8c69", trecho: "A otimização desses fatores é crucial...", detalhe: "Tom enciclopédico uniforme" }
  ];

  const filteredOccurrences = allOccurrences.filter(occurrence => {
    if (activeFilter === 'Tudo') {
      return true;
    }
    return occurrence.tipo === activeFilter;
  });

  // Renderiza o conteúdo do texto dinamicamente com base no filtro ativo
  const textContent = documentParagraphs.map((paragraph, pIndex) => (
    <p key={pIndex}>
      {paragraph.map((segment, sIndex) => {
        const isHighlightable = segment.type !== 'normal';
        const showHighlight = activeFilter === 'Tudo' || activeFilter === segment.type;

        if (isHighlightable && showHighlight) {
          let className = '';
          let tagText = '';
          if (segment.type === 'GERADO POR IA') {
            className = 'hl-ia';
            tagText = 'IA';
          } else if (segment.type === 'PLÁGIO') {
            className = 'hl-plagio';
            tagText = 'PLÁGIO';
          } else if (segment.type === 'FONTE NÃO CONFIÁVEL') {
            className = 'hl-fonte';
            tagText = 'FONTE';
          }
          
          return (
            <span key={sIndex} className={className}>
              {segment.text}
              <span className="tag-inline">{tagText}</span>
            </span>
          );
        }
        return <span key={sIndex}>{segment.text}</span>;
      })}
    </p>
  ));

  return (
    <div className="analysis-screen">
      <div className="analysis-container">
        <header className="analysis-header">
          <div className="header-info">
            <h2>Painel de Análise</h2>
          </div>
          <div className="header-actions">
            <div className="view-toggle">
              <span className="toggle-label">Texto Completo</span>
              <label className="switch">
                <input
                  type="checkbox"
                  checked={showFullText}
                  onChange={() => setShowFullText((prev) => !prev)}
                />
                <span className="slider"></span>
              </label>
            </div>
            <FilterBar
              activeFilter={activeFilter}
              setActiveFilter={setActiveFilter}
            />
          </div>
        </header>

        <main className={`analysis-main ${!showFullText ? 'occurrences-only-view' : ''}`}>
          {/* Lado Esquerdo */}
          {showFullText && (
            <section className="text-section">
              <TextDisplay textContent={textContent} />
            </section>
          )}
          
          {/* Lado Direito */}
          <aside className="side-panel">
            <div className="occurrences-header">
              <h3>Indícios Detectados</h3>
              <div className="divider-small"></div>
            </div>
            
            <div className="cards-stack">
              {filteredOccurrences.map(occ => (
                <OccurrenceCard
                  key={occ.id}
                  tipo={occ.tipo}
                  cor={occ.cor}
                  trecho={occ.trecho}
                  detalhe={occ.detalhe}
                />
              ))}
            </div>
          </aside>
        </main>
      </div>
    </div>
  );
}

export default AnalysisPage;