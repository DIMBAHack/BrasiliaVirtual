// src/components/Analysis/FilterBar.jsx
import './FilterBar.css';

const FilterBar = () => {
  const filters = [
    { label: 'Tudo', color: '#fff', active: true },
    { label: 'Gerado por IA', color: '#ff8c69' },
    { label: 'Plágio', color: '#7fb3d5' },
    { label: 'Fonte não confiável', color: '#f3cc8a' },
    { label: 'Neutro', color: '#a0a0a0' },
  ];

  return (
    <div className="filter-bar">
      <span>Mostrar:</span>
      {filters.map((f, i) => (
        <button 
          key={i} 
          className={`filter-btn ${f.active ? 'active' : ''}`}
          style={{ '--btn-color': f.color }}
        >
          <span className="dot" style={{ backgroundColor: f.color }}></span>
          {f.label}
        </button>
      ))}
    </div>
  );
};

export default FilterBar;