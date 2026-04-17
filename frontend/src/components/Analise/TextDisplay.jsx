// src/components/Analysis/TextDisplay.jsx
import './TextDisplay.css';

const TextDisplay = ({ textContent }) => {
  return (
    <div className="text-display-container">
      <p>
        A fotossíntese é o processo pelo qual as plantas convertem luz solar em energia química... 
        <span className="hl-ia">
          pois garante a produção de oxigênio e a fixação de carbono...
          <span className="tag-inline">IA</span>
        </span>
      </p>
      {/* Aqui viriam os outros parágrafos com as classes hl-plagio e hl-fonte */}
    </div>
  );
};

export default TextDisplay;