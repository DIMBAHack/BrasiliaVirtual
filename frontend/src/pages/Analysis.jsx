// src/pages/Analysis.jsx
import React, { useState } from 'react';
import { useParams, Navigate } from 'react-router-dom';
import FilterBar from '../components/Analise/FilterBar';
import TextDisplay from '../components/Analise/TextDisplay';
import OccurrenceCard from '../components/Analise/OccurrenceCard';
import AnalysisSummary from '../components/Analise/AnalysisSummary';
import ReportModal from '../components/Analise/ReportModal';
import './Analysis.css';

// MOCK DATA - Em um cenário real, isso viria de uma chamada de API usando o `id`
const mockAnalysesDetails = [
  {
    id: 1,
    title: 'Análise do Relatório Trimestral Q3',
    studentName: 'Ana Carolina',
    date: '15 de Julho, 2024',
    documentParagraphs: [
      [{ type: 'normal', text: 'O relatório trimestral Q3 demonstra um crescimento sólido. ' }, { type: 'GERADO POR IA', text: 'A sinergia entre os departamentos foi um catalisador para o sucesso.' }, { type: 'normal', text: ' As vendas aumentaram 15% em comparação com o Q2.' }],
      [{ type: 'PLÁGIO', text: '"A inovação disruptiva é a chave para a liderança de mercado", como afirmado em relatórios anteriores.' }, { type: 'normal', text: ' Nossa estratégia de marketing digital foi fundamental.' }]
    ],
    allOccurrences: [
      { id: 1, tipo: "GERADO POR IA", cor: "#ff8c69", trecho: "...catalisador para o sucesso.", detalhe: "Linguagem corporativa genérica" },
      { id: 2, tipo: "PLÁGIO", cor: "#7fb3d5", trecho: "A inovação disruptiva é a chave...", detalhe: "Relatório Interno Q1 - sem citação" }
    ]
  },
  {
    id: 2,
    title: 'Tese de Doutorado - Capítulo 2',
    studentName: 'Marcos Vinícius',
    date: '11 de Julho, 2024',
    documentParagraphs: [
      [{ type: 'normal', text: 'A metodologia de pesquisa adotada foi a qualitativa. ' }, { type: 'GERADO POR IA', text: 'Este paradigma investigativo permite uma exploração profunda dos fenômenos sociais em seu contexto natural.' }, { type: 'normal', text: ' Foram realizadas entrevistas semiestruturadas.' }],
      [{ type: 'GERADO POR IA', text: 'A análise de conteúdo revelou padrões emergentes significativos.' }, { type: 'normal', text: ' Os resultados corroboram a hipótese inicial.' }],
    ],
    allOccurrences: [
      { id: 1, tipo: "GERADO POR IA", cor: "#ff8c69", trecho: "...exploração profunda dos fenômenos...", detalhe: "Tom enciclopédico uniforme" },
      { id: 2, tipo: "GERADO POR IA", cor: "#ff8c69", trecho: "...padrões emergentes significativos.", detalhe: "Linguagem acadêmica padrão" },
    ]
  },
  {
    id: 3,
    title: 'Artigo sobre Inteligência Artificial na Saúde',
    studentName: 'Beatriz Lima',
    date: '05 de Julho, 2024',
    documentParagraphs: [
      [{ type: 'normal', text: 'A fotossíntese é o processo pelo qual as plantas convertem luz solar em energia química... ' }, { type: 'GERADO POR IA', text: 'pois garante a produção de oxigênio e a fixação de carbono de forma sistemática...' }, { type: 'normal', text: ' Este processo é fundamental para a vida na Terra.' }],
      [{ type: 'normal', text: 'O processo ocorre principalmente nos cloroplastos.' }, { type: 'PLÁGIO', text: '"A reação geral pode ser simplificada..."' }, { type: 'normal', text: ' A clorofila é a molécula chave.' }],
      [{ type: 'normal', text: 'Existem dois estágios principais na fotossíntese. ' }, { type: 'FONTE NÃO CONFIÁVEL', text: 'Estudos recentes da Universidade de Stanford indicam que a eficiência quântica pode ser otimizada.' }],
      [{ type: 'normal', text: 'O ciclo de Calvin utiliza o ATP e o NADPH para converter dióxido de carbono em glicose.' }],
      [{ type: 'normal', text: 'Fatores como a intensidade da luz afetam a taxa de fotossíntese. ' }, { type: 'GERADO POR IA', text: 'A otimização desses fatores é crucial para a agricultura moderna.' }],
    ],
    allOccurrences: [
      { id: 1, tipo: "GERADO POR IA", cor: "#ff8c69", trecho: "...de forma sistemática...", detalhe: "Tom enciclopédico uniforme" },
      { id: 2, tipo: "PLÁGIO", cor: "#7fb3d5", trecho: "A reação geral pode ser simplificada...", detalhe: "Wikipedia — sem citação" },
      { id: 3, tipo: "FONTE NÃO CONFIÁVEL", cor: "#f3cc8a", trecho: "Estudos recentes da Universidade de Stanford...", detalhe: "Fonte acadêmica, mas sem link ou citação formal." },
      { id: 4, tipo: "GERADO POR IA", cor: "#ff8c69", trecho: "A otimização desses fatores é crucial...", detalhe: "Tom enciclopédico uniforme" }
    ]
  }
];

function AnalysisPage() {
  const { id } = useParams();
  const analysisData = mockAnalysesDetails.find(a => a.id === parseInt(id));

  const [showFullText, setShowFullText] = useState(true);
  const [activeFilter, setActiveFilter] = useState('Tudo');
  const [isReportModalOpen, setIsReportModalOpen] = useState(false);
  const [isGeneratingReport, setIsGeneratingReport] = useState(false);
  const [reportContent, setReportContent] = useState('');

  if (!analysisData) {
    // Redireciona para a lista de análises se o ID for inválido
    return <Navigate to="/minhasanalises" />;
  }

  const { title, studentName, documentParagraphs, allOccurrences } = analysisData;

  const filteredOccurrences = allOccurrences.filter(occurrence => {
    if (activeFilter === 'Tudo') {
      return true;
    }
    return occurrence.tipo === activeFilter;
  });

  const handleGenerateReport = async () => {
    setIsReportModalOpen(true);
    setIsGeneratingReport(true);
    setReportContent(''); // Limpa o conteúdo anterior

    // Simula uma chamada de API para gerar o relatório
    // Em um cenário real, você enviaria os dados da análise para o backend
    const summary = analysisData.allOccurrences.reduce((acc, occ) => {
      acc[occ.tipo] = (acc[occ.tipo] || 0) + 1;
      return acc;
    }, {});

    // Simulação de chamada de API
    setTimeout(() => {
      const generatedReport = `
        <h4>Guia para Conversa Construtiva</h4>
        <p><strong>Assunto:</strong> Análise do documento "${analysisData.title}"</p>
        <p><strong>Aluno(a):</strong> ${analysisData.studentName}</p>
        <hr>
        <p><strong>1. Ponto de Partida (Abordagem Positiva):</strong></p>
        <p>Inicie a conversa reconhecendo o esforço do aluno. "Olá, ${analysisData.studentName}. Obrigado por enviar o trabalho '${analysisData.title}'. Gostaria de conversar sobre alguns pontos para aprimorá-lo."</p>
        
        ${summary['GERADO POR IA'] > 0 ? `
        <p><strong>2. Abordando a Escrita Similar à IA (${summary['GERADO POR IA']} trecho(s)):</strong></p>
        <p>Apresente o indício como uma oportunidade de aprendizado sobre o uso de ferramentas. "Notei que alguns trechos têm um estilo de escrita muito polido e formal, similar ao que ferramentas de IA produzem. Essas ferramentas são ótimas para ter ideias, mas é fundamental que o trabalho final reflita sua própria voz e compreensão. Vamos revisar juntos como podemos usar a IA de forma ética para pesquisa, sem deixar que ela escreva por você."</p>
        ` : ''}

        ${summary['PLÁGIO'] > 0 ? `
        <p><strong>3. Sobre a Similaridade com Fontes Online (${summary['PLÁGIO']} trecho(s)):</strong></p>
        <p>Foque na importância da citação e da originalidade. "Identifiquei também passagens que são muito parecidas com textos encontrados online. É crucial para a integridade acadêmica que todas as fontes sejam devidamente citadas. Você pode me mostrar como fez a pesquisa para essas partes? Vamos trabalhar juntos nas técnicas de citação e paráfrase."</p>
        ` : ''}

        ${summary['FONTE NÃO CONFIÁVEL'] > 0 ? `
        <p><strong>4. Verificação de Fontes (${summary['FONTE NÃO CONFIÁVEL']} trecho(s)):</strong></p>
        <p>Discuta a importância de fontes confiáveis. "Vi que uma das fontes mencionadas pode não ser considerada uma referência acadêmica robusta. Parte do desenvolvimento da pesquisa é aprender a discernir fontes confiáveis. Que tal pesquisarmos juntos algumas bases de dados acadêmicas?"</p>
        ` : ''}

        <p><strong>5. Encerramento e Próximos Passos:</strong></p>
        <p>Termine de forma encorajadora, focando no desenvolvimento do aluno. "O objetivo desta conversa é te ajudar a crescer como pesquisador(a). Estou aqui para apoiar. Que tal você revisar esses pontos e me apresentar uma nova versão até a próxima semana?"</p>
      `;
      setReportContent(generatedReport);
      setIsGeneratingReport(false);
    }, 2000); // Simula 2 segundos de espera
  };

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
            <h2>{title}</h2>
            <p className="document-author">Enviado por: {studentName}</p>
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
            <button className="report-btn" onClick={handleGenerateReport}>
              Gerar Relatório Pedagógico
            </button>
            <FilterBar
              activeFilter={activeFilter}
              setActiveFilter={setActiveFilter}
            />
          </div>
        </header>

        <AnalysisSummary occurrences={allOccurrences} />

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

      <ReportModal
        isOpen={isReportModalOpen}
        onClose={() => setIsReportModalOpen(false)}
        isLoading={isGeneratingReport}
        reportContent={reportContent}
        studentName={studentName}
      />
    </div>
  );
}

export default AnalysisPage;