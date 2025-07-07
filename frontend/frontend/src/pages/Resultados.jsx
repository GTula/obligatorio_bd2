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
  
  const [mostrarObservados, setMostrarObservados] = useState(false);
  
  const [tablaActiva, setTablaActiva] = useState('lista-partido');

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

      // Cargar votos SOLO normales por defecto
      const votos = await ResultadosService.getVotosSoloNormales(
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

  const alternarTipoVotos = async () => {
    try {
      setLoading(true);
      
      let votos;
      if (mostrarObservados) {
        // Cambiar a solo normales
        votos = await ResultadosService.getVotosSoloNormales(
          mesaData.numMesa,
          mesaData.idEleccion,
          mesaData.fecha
        );
      } else {
        // Cambiar a incluir observados
        votos = await ResultadosService.getVotosConObservados(
          mesaData.numMesa,
          mesaData.idEleccion,
          mesaData.fecha
        );
      }
      
      setResultados(votos);
      setMostrarObservados(!mostrarObservados);
      
    } catch (err) {
      setError(err.message);
      console.error('Error alternando tipo de votos:', err);
    } finally {
      setLoading(false);
    }
  };

  const renderTablaActiva = () => {
    if (loading) {
      return <div className="loading">Cargando resultados...</div>;
    }

    if (error) {
      return <div className="error">Error: {error}</div>;
    }

    if (!resultados || Object.keys(resultados).length === 0) {
      return <div className="no-data">No hay votos registrados</div>;
    }

    // Para plebiscitos
    if (tipoEleccion === 3) {
      return (
        <table className="tabla-resultados">
          <thead>
            <tr>
              <th>Opción</th>
              <th>Votos</th>
              <th>Porcentaje</th>
            </tr>
          </thead>
          <tbody>
            {resultados.votos_plebiscito?.map((r, i) => (
              <tr key={i}>
                <td>{r.valor}</td>
                <td>{r.cant_votos}</td>
                <td>{r.porcentaje}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      );
    }

    switch (tablaActiva) {
      case 'lista-partido':
        return (
          <table className="tabla-resultados">
            <thead>
              <tr>
                <th>Lista ID</th>
                <th>Partido</th>
                <th>Votos</th>
                <th>Porcentaje</th>
              </tr>
            </thead>
            <tbody>
              {resultados.tabla_lista_partido?.map((r, i) => (
                <tr key={i}>
                  <td>{r.lista_id}</td>
                  <td>{r.partido}</td>
                  <td>{r.cant_votos}</td>
                  <td>{r.porcentaje}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        );

      case 'partido':
        return (
          <table className="tabla-resultados">
            <thead>
              <tr>
                <th>Partido</th>
                <th>Votos</th>
                <th>Porcentaje</th>
              </tr>
            </thead>
            <tbody>
              {resultados.tabla_partido?.map((r, i) => (
                <tr key={i}>
                  <td>{r.partido}</td>
                  <td>{r.cant_votos}</td>
                  <td>{r.porcentaje}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        );

      case 'candidatos':
        return (
          <table className="tabla-resultados">
            <thead>
              <tr>
                <th>Partido</th>
                <th>Candidato</th>
                <th>Votos</th>
                <th>Porcentaje</th>
              </tr>
            </thead>
            <tbody>
              {resultados.tabla_partido_candidato?.map((r, i) => (
                <tr key={i}>
                  <td>{r.partido}</td>
                  <td>{r.candidato}</td>
                  <td>{r.cant_votos}</td>
                  <td>{r.porcentaje}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        );

      case 'departamentos':
        return (
          <table className="tabla-resultados">
            <thead>
              <tr>
                <th>Departamento</th>
                <th>Partido Ganador</th>
                <th>Lista ID</th>
                <th>Votos</th>
                <th>Porcentaje</th>
              </tr>
            </thead>
            <tbody>
              {resultados.tabla_ganadores_departamento?.map((r, i) => (
                <tr key={i}>
                  <td>{r.departamento}</td>
                  <td>{r.partido_ganador}</td>
                  <td>{r.lista_id}</td>
                  <td>{r.cant_votos}</td>
                  <td>{r.porcentaje}%</td>
                </tr>
              ))}
            </tbody>
          </table>
        );

      default:
        return <div>Seleccione una pestaña</div>;
    }
  };

  const getTotalVotos = () => {
    return resultados.total_votos || 0;
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
          <p><strong>Mostrando:</strong> 
            <span className={mostrarObservados ? 'con-observados' : 'solo-normales'}>
              {mostrarObservados ? ' Todos los votos (incluye observados)' : ' Solo votos normales'}
            </span>
          </p>
        </div>
      </div>

      {/* Cards cuadradas una al lado de la otra */}
      <section className="stats-section">
        <div className="card">
          <h3>Total Votos</h3>
          <p className="stat-number">{getTotalVotos()}</p>
        </div>
        <div className="card">
          <h3>Votos Válidos</h3>
          <p className="stat-number validos">{resultados.votos_normales || 0}</p>
        </div>
        <div className="card">
          <h3>Votos en Blanco</h3>
          <p className="stat-number blanco">{resultados.votos_blanco || 0}</p>
        </div>
        <div className="card">
          <h3>Votos Anulados</h3>
          <p className="stat-number anulados">{resultados.votos_anulados || 0}</p>
        </div>
      </section>

      {/* Botón para alternar tipo de votos */}
      <div className="toggle-section">
        <button 
          className={`btn toggle-votos ${mostrarObservados ? 'observados' : 'normales'}`}
          onClick={alternarTipoVotos}
          disabled={loading}
        >
          {mostrarObservados ? '📊 Ver Solo Normales' : '⚠️ Incluir Observados'}
        </button>
      </div>

      {/* Pestañas para las tablas (solo si no es plebiscito) */}
      {tipoEleccion !== 3 && (
        <div className="tabs-container">
          <div className="tabs">
            <button 
              className={`tab ${tablaActiva === 'lista-partido' ? 'active' : ''}`}
              onClick={() => setTablaActiva('lista-partido')}
            >
              Lista - Partido
            </button>
            <button 
              className={`tab ${tablaActiva === 'partido' ? 'active' : ''}`}
              onClick={() => setTablaActiva('partido')}
            >
              Por Partido
            </button>
            <button 
              className={`tab ${tablaActiva === 'candidatos' ? 'active' : ''}`}
              onClick={() => setTablaActiva('candidatos')}
            >
              Candidatos
            </button>
            <button 
              className={`tab ${tablaActiva === 'departamentos' ? 'active' : ''}`}
              onClick={() => setTablaActiva('departamentos')}
            >
              Departamentos
            </button>
          </div>
        </div>
      )}

      {/* Contenido de la tabla activa */}
      <div className="resultados-content">
        {renderTablaActiva()}
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
