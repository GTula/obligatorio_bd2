import React from 'react';
import { useNavigate } from 'react-router-dom';
import './Mesa.css';
import { useMesa } from '../context/MesaContext';

function Resultados() {
  const navigate = useNavigate();
  const { mesaCerrada } = useMesa();

  const resultados = [
    { partido: 'Partido A', votos: 120 },
    { partido: 'Partido B', votos: 90 },
    { partido: 'Partido C', votos: 50 },
  ];

  return (
    <div className="resultados-container">
      <h2>Escrutinio</h2>
      <table className="tabla-resultados">
        <thead>
          <tr>
            <th>Partido</th>
            <th>Votos</th>
          </tr>
        </thead>
        <tbody>
          {resultados.map((r, i) => (
            <tr key={i}>
              <td>{r.partido}</td>
              <td>{r.votos}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <button className="btn volver" onClick={() => navigate('/mesa')}>Volver</button>
    </div>
  );
}

export default Resultados;
