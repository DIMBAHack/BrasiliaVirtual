import React, { useState, useEffect, useRef } from 'react';
import './FilterBar.css';

const filterOptions = [
  { label: 'Tudo', value: 'Tudo', color: '#ccc' },
  { label: 'Gerado por IA', value: 'GERADO POR IA', color: '#ff8c69' },
  { label: 'Plágio', value: 'PLÁGIO', color: '#7fb3d5' },
  { label: 'Fonte não confiável', value: 'FONTE NÃO CONFIÁVEL', color: '#f3cc8a' },
];

const DropdownIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M6 9L12 15L18 9" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
);

function FilterBar({ activeFilter, setActiveFilter }) {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef(null);

  const activeOption = filterOptions.find(opt => opt.value === activeFilter) || filterOptions[0];

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [dropdownRef]);

  const handleSelect = (value) => {
    setActiveFilter(value);
    setIsOpen(false);
  };

  return (
    <div className="filter-dropdown" ref={dropdownRef}>
      <button className="filter-dropdown-toggle" onClick={() => setIsOpen(!isOpen)} aria-expanded={isOpen}>
        <span className="dot" style={{ backgroundColor: activeOption.color }}></span>
        <span>{activeOption.label}</span>
        <DropdownIcon />
      </button>

      {isOpen && (
        <ul className="filter-dropdown-menu">
          {filterOptions.map(option => (
            <li 
              key={option.value} 
              className={`filter-dropdown-item ${activeFilter === option.value ? 'active' : ''}`}
              onClick={() => handleSelect(option.value)}
            >
              <span className="dot" style={{ backgroundColor: option.color }}></span>
              {option.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default FilterBar;