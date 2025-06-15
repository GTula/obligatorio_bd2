import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Mesa.css';
import { useMesa } from '../context/MesaContext';

function VotantesMesa() {
  const navigate = useNavigate();
  const { mesaAbierta } = useMesa();

  const votantes = [
    { nombre: 'Juan Pérez', documento: '4.123.456-7', votó: false },
    { nombre: 'María García', documento: '5.234.567-8', votó: true },
    // más votantes...
  ];

  return (
    <div className="votantes-container">
      <h2>Lista de Votantes</h2>
      <ul className="votante-lista">
        {votantes.map((v, i) => (
          <li key={i} className={`votante ${v.votó ? 'voto' : ''}`}>
            <span>{v.nombre} ({v.documento})</span>
            {mesaAbierta && (
              <button className="btn-voto">{v.votó ? '✅ Votó' : '🗳️ Marcar como votó'}</button>
            )}
          </li>
        ))}
      </ul>
      <button className="btn volver" onClick={() => navigate('/mesa')}>Volver</button>
    </div>
  );
}

export default VotantesMesa;
