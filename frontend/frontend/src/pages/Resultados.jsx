import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Mesa.css';
import { useMesa } from '../context/MesaContext';
import { ResultadosService } from '../services/resultadosService';

function Resultados() {
  const navigate = useNavigate();
  const { mesaCerrada, mesaData } = useMesa();
  const [resultados, setResultados] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [tipoEleccion, setTipoEleccion] = useState(null);

  useEffect(() => {
    if (!mesaCerrada || !mesaData.numMesa) {
      navigate('/mesa');
      return;
    }

    cargarResultados();
  }, [mesaCerrada, mesaData, navigate]);

  const cargarResultados = async () => {
    try {
      setLoading(true);
      setError(null);

      // Obtener tipo de elección
      const tipo = await ResultadosService.getTipoEleccion(mesaData.idEleccion);
      setTipoEleccion(tipo);

      // Obtener votos normales
      const votos = await ResultadosService.getVotosNormales(
        mesaData.numMesa,
        mesaData.idEleccion,
        mesaData.fecha
      );

      setResultados(votos);
    } catch (err) {
      setError(err.message);
      console.error('Error cargando resultados:', err);
    } finally {
      setLoading(false);
    }
  };

  const renderResultados = () => {
    if (loading) {
      return <div className="loading">Cargando resultados...</div>;
    }

    if (error) {
      return <div className="error">Error: {error}</div>;
    }

    if (resultados.length === 0) {
      return <div className="no-data">No hay votos registrados</div>;
    }

    // Renderizar según el tipo de elección
    if (tipoEleccion === 3) {
      // Plebiscito
      return (
        <table className="tabla-resultados">
          <thead>
            <tr>
              <th>Opción</th>
              <th>Votos</th>
            </tr>
          </thead>
          <tbody>
            {resultados.map((r, i) => (
              <tr key={i}>
                <td>{r.valor}</td>
                <td>{r.total_votos}</td>
              </tr>
            ))}
          </tbody>
        </table>
      );
    } else {
      // Otras elecciones (con partidos)
      return (
        <table className="tabla-resultados">
          <thead>
            <tr>
              <th>Partido</th>
              <th>Lista ID</th>
              <th>Votos</th>
            </tr>
          </thead>
          <tbody>
            {resultados.map((r, i) => (
              <tr key={i}>
                <td>{r.partido}</td>
                <td>{r.lista_id}</td>
                <td>{r.total_votos}</td>
              </tr>
            ))}
          </tbody>
        </table>
      );
    }
  };

  const getTotalVotos = () => {
    return resultados.reduce((total, r) => total + r.total_votos, 0);
  };

  const getTipoEleccionNombre = () => {
    const tipos = {
      1: 'Presidencial',
      2: 'Ballotage',
      3: 'Plebiscito',
      4: 'Municipal'
    };
    return tipos[tipoEleccion] || 'Desconocido';
  };

  return (
    <div className="resultados-container">
      <div className="resultados-header">
        <h2>Escrutinio - Mesa {mesaData.numMesa}</h2>
        <div className="info-eleccion">
          <p><strong>Tipo:</strong> {getTipoEleccionNombre()}</p>
          <p><strong>Fecha:</strong> {mesaData.fecha}</p>
          <p><strong>Total de votos:</strong> {getTotalVotos()}</p>
        </div>
      </div>

      <div className="resultados-content">
        {renderResultados()}
      </div>

      <div className="resultados-actions">
        <button className="btn refresh" onClick={cargarResultados}>
          Actualizar
        </button>
        <button className="btn volver" onClick={() => navigate('/mesa')}>
          Volver
        </button>
      </div>
    </div>
  );
}

export default Resultados;
