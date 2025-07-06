import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Mesa.css';
import { useMesa } from '../context/MesaContext';
import { ResultadosService } from '../services/resultadosService';

function Resultados() {
  const navigate = useNavigate();
  const { mesaCerrada, mesaData } = useMesa();
  const [resultados, setResultados] = useState(null);
  const [votosAnulados, setVotosAnulados] = useState(0);
  const [votosBlanco, setVotosBlanco] = useState(0);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [tablaActiva, setTablaActiva] = useState('lista-partido'); // 'lista-partido', 'partido', 'partido-candidato', 'ganadores-departamento'

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

      const datos = await ResultadosService.getVotosNormales(
        mesaData.numMesa,
        mesaData.idEleccion,
        mesaData.fecha
      );

      setResultados(datos);
      setVotosAnulados(datos.votos_anulados || 0);
      setVotosBlanco(datos.votos_blanco || 0);

    } catch (err) {
      setError(err.message);
      console.error('Error cargando resultados:', err);
    } finally {
      setLoading(false);
    }
  };

  const getTotalVotos = () => {
    if (!resultados) return 0;
    return resultados.total_votos;
  };

  const getTipoEleccionNombre = () => {
    if (!resultados) return 'Desconocido';
    
    const tipos = {
      1: 'Presidencial',
      2: 'Ballotage',
      3: 'Plebiscito',
      4: 'Municipal'
    };
    return tipos[resultados.tipo_eleccion] || 'Desconocido';
  };

  const renderTablaPlebiscito = () => {
    if (!resultados.votos_plebiscito || resultados.votos_plebiscito.length === 0) {
      return <div className="no-data">No hay votos registrados</div>;
    }

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
          {resultados.votos_plebiscito.map((voto, index) => (
            <tr key={index}>
              <td>{voto.valor}</td>
              <td>{voto.cant_votos}</td>
              <td>{voto.porcentaje}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  const renderTablaListaPartido = () => {
    if (!resultados.tabla_lista_partido || resultados.tabla_lista_partido.length === 0) {
      return <div className="no-data">No hay votos registrados</div>;
    }

    return (
      <table className="tabla-resultados">
        <thead>
          <tr>
            <th>Lista</th>
            <th>Partido</th>
            <th>Cant. Votos</th>
            <th>Porcentaje</th>
          </tr>
        </thead>
        <tbody>
          {resultados.tabla_lista_partido.map((item, index) => (
            <tr key={index} className={item.lista_id === 'En Blanco' ? 'voto-blanco' : item.lista_id === 'Anulado' ? 'voto-anulado' : ''}>
              <td>{item.lista_id}</td>
              <td>{item.partido}</td>
              <td>{item.cant_votos}</td>
              <td>{item.porcentaje}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  const renderTablaPartido = () => {
    if (!resultados.tabla_partido || resultados.tabla_partido.length === 0) {
      return <div className="no-data">No hay votos registrados</div>;
    }

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
          {resultados.tabla_partido.map((item, index) => (
            <tr key={index} className={item.partido === 'En Blanco' ? 'voto-blanco' : item.partido === 'Anulado' ? 'voto-anulado' : ''}>
              <td>{item.partido}</td>
              <td>{item.cant_votos}</td>
              <td>{item.porcentaje}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  const renderTablaPartidoCandidato = () => {
    if (!resultados.tabla_partido_candidato || resultados.tabla_partido_candidato.length === 0) {
      return <div className="no-data">No hay votos registrados</div>;
    }

    return (
      <table className="tabla-resultados">
        <thead>
          <tr>
            <th>Partido</th>
            <th>Candidato</th>
            <th>Cant. Votos</th>
            <th>Porcentaje</th>
          </tr>
        </thead>
        <tbody>
          {resultados.tabla_partido_candidato.map((item, index) => (
            <tr key={index} className={item.partido === 'En Blanco' ? 'voto-blanco' : item.partido === 'Anulado' ? 'voto-anulado' : ''}>
              <td>{item.partido}</td>
              <td>{item.candidato}</td>
              <td>{item.cant_votos}</td>
              <td>{item.porcentaje}%</td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  const renderTablaGanadoresDepartamento = () => {
    if (!resultados.tabla_ganadores_departamento || resultados.tabla_ganadores_departamento.length === 0) {
      return <div className="no-data">No hay datos de departamentos disponibles</div>;
    }

    return (
      <table className="tabla-resultados">
        <thead>
          <tr>
            <th>Departamento</th>
            <th>Partido Ganador</th>
            <th>Lista</th>
            <th>Votos</th>
            <th>Total Depto.</th>
            <th>Porcentaje</th>
          </tr>
        </thead>
        <tbody>
          {resultados.tabla_ganadores_departamento.map((item, index) => (
            <tr key={index} className="ganador-departamento">
              <td><strong>{item.departamento}</strong></td>
              <td>{item.partido_ganador}</td>
              <td>{item.lista_id}</td>
              <td>{item.cant_votos}</td>
              <td>{item.total_votos_depto}</td>
              <td><strong>{item.porcentaje}%</strong></td>
            </tr>
          ))}
        </tbody>
      </table>
    );
  };

  const renderContenidoTablas = () => {
    if (loading) {
      return <div className="loading">Cargando resultados...</div>;
    }

    if (error) {
      return <div className="error">Error: {error}</div>;
    }

    if (!resultados) {
      return <div className="no-data">No hay datos disponibles</div>;
    }

    // Para plebiscito, solo mostrar una tabla
    if (resultados.tipo_eleccion === 3) {
      return (
        <div className="resultados-content">
          <h3>Resultados del Plebiscito</h3>
          {renderTablaPlebiscito()}
        </div>
      );
    }

    // Para otras elecciones, mostrar las cuatro tablas con pestañas
    return (
      <div className="resultados-content">
        {/* Pestañas */}
        <div className="tabs-container">
          <button 
            className={`tab ${tablaActiva === 'lista-partido' ? 'active' : ''}`}
            onClick={() => setTablaActiva('lista-partido')}
          >
            Por Lista
          </button>
          <button 
            className={`tab ${tablaActiva === 'partido' ? 'active' : ''}`}
            onClick={() => setTablaActiva('partido')}
          >
            Por Partido
          </button>
          <button 
            className={`tab ${tablaActiva === 'partido-candidato' ? 'active' : ''}`}
            onClick={() => setTablaActiva('partido-candidato')}
          >
            Por Candidato
          </button>
          <button 
            className={`tab ${tablaActiva === 'ganadores-departamento' ? 'active' : ''}`}
            onClick={() => setTablaActiva('ganadores-departamento')}
          >
            Ganadores por Depto.
          </button>
        </div>

        {/* Contenido de las tablas */}
        <div className="tab-content">
          {tablaActiva === 'lista-partido' && (
            <div>
              <h3>Resultados por Lista y Partido</h3>
              {renderTablaListaPartido()}
            </div>
          )}
          
          {tablaActiva === 'partido' && (
            <div>
              <h3>Resultados por Partido</h3>
              {renderTablaPartido()}
            </div>
          )}
          
          {tablaActiva === 'partido-candidato' && (
            <div>
              <h3>Resultados por Partido y Candidato</h3>
              {renderTablaPartidoCandidato()}
            </div>
          )}

          {tablaActiva === 'ganadores-departamento' && (
            <div>
              <h3>Ganadores por Departamento</h3>
              {renderTablaGanadoresDepartamento()}
            </div>
          )}
        </div>
      </div>
    );
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

      {/* Resumen de votos */}
      {resultados && (
        <div className="resumen-votos">
          <div className="resumen-card">
            <h4>Votos Válidos</h4>
            <p className="numero-grande">{resultados.votos_normales || 0}</p>
          </div>
          <div className="resumen-card">
            <h4>Votos Anulados</h4>
            <p className="numero-grande">{votosAnulados}</p>
          </div>
          <div className="resumen-card">
            <h4>Votos en Blanco</h4>
            <p className="numero-grande">{votosBlanco}</p>
          </div>
          <div className="resumen-card total">
            <h4>Total General</h4>
            <p className="numero-grande">{getTotalVotos()}</p>
          </div>
        </div>
      )}

      {/* Contenido principal */}
      {renderContenidoTablas()}

      {/* Acciones */}
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
