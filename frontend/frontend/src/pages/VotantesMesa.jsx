import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Mesa.css';
import './Votantes.css';
import { useMesa } from '../context/MesaContext';
import { VotantesService } from '../services/votantesService';

function Votantes() {
  const navigate = useNavigate();
  const { mesaAbierta } = useMesa();
  
  const [votantes, setVotantes] = useState([]);
  const [estadisticas, setEstadisticas] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Estados para búsqueda
  const [busqueda, setBusqueda] = useState({
    serie: '',
    numero: ''
  });
  const [votanteEncontrado, setVotanteEncontrado] = useState(null);
  const [buscando, setBuscando] = useState(false);
  
  // Estados para filtros
  const [filtro, setFiltro] = useState('todos');
  const [busquedaTexto, setBusquedaTexto] = useState('');
  
  // Datos de la mesa
  const [mesaData, setMesaData] = useState({
    numMesa: null,
    idCircuito: null,
    idEleccion: null,
    fecha: null
  });

  useEffect(() => {
  // Verificar que la mesa esté abierta
  if (!mesaAbierta) {
    navigate('/mesa');
    return;
  }

  // Obtener datos de la mesa con fallbacks
  const mesaId = localStorage.getItem('mesa_id');
  const idEleccion = localStorage.getItem('id_eleccion') || '1';
  const idCircuito = localStorage.getItem('id_circuito');
  
  console.log('🔍 VotantesMesa - Datos obtenidos:', {
    mesaId,
    idEleccion,
    idCircuito,
    localStorage_completo: { ...localStorage }
  });
  
  // Validar que tenemos todos los datos necesarios
  if (!mesaId || !idCircuito) {
    console.error('❌ Faltan datos de la mesa:', { mesaId, idCircuito });
    setError('Faltan datos de la mesa. Vuelva a la página principal.');
    setLoading(false);
    return;
  }
  
  const mesaDataParsed = {
    numMesa: parseInt(mesaId),
    idCircuito: parseInt(idCircuito),
    idEleccion: parseInt(idEleccion)
  };
  
  console.log('✅ Mesa data parseada:', mesaDataParsed);
  
  // Verificar que los valores no sean NaN
  if (isNaN(mesaDataParsed.idCircuito) || isNaN(mesaDataParsed.idEleccion)) {
    console.error('❌ IDs inválidos:', mesaDataParsed);
    setError('Datos de mesa inválidos. Vuelva a la página principal.');
    setLoading(false);
    return;
  }
  
  setMesaData(mesaDataParsed);
  cargarVotantes(mesaDataParsed.idCircuito, mesaDataParsed.idEleccion);
}, [mesaAbierta, navigate]);


  const cargarVotantes = async (idCircuito, idEleccion) => {
    try {
      setLoading(true);
      setError(null);
      
      const data = await VotantesService.getVotantesHabilitados(idCircuito, idEleccion);
      setVotantes(data.votantes);
      setEstadisticas(data.estadisticas);
    } catch (err) {
      setError(err.message);
      console.error('Error cargando votantes:', err);
    } finally {
      setLoading(false);
    }
  };

  // Función corregida para abrir tótem
  const abrirTotem = () => {
    if (!mesaData.numMesa || !mesaData.idCircuito || !mesaData.idEleccion) {
      alert('Faltan datos de la mesa. Intente recargar la página.');
      return;
    }

    // Construir URL con parámetros
    const params = new URLSearchParams({
      numMesa: mesaData.numMesa,
      idCircuito: mesaData.idCircuito,
      idEleccion: mesaData.idEleccion,
      fecha: mesaData.fecha || ''
    });

    const urlTotem = `/votar?${params.toString()}`;
    
    console.log('🗳️ Abriendo tótem con URL:', urlTotem);
    console.log('Datos enviados:', mesaData);
    
    // Abrir en nueva pestaña
    window.open(urlTotem, '_blank', 'width=1200,height=800,scrollbars=yes,resizable=yes');
  };

  const buscarVotante = async () => {
    if (!busqueda.serie || !busqueda.numero) {
      alert('Ingrese serie y número de credencial');
      return;
    }

    try {
      setBuscando(true);
      const votante = await VotantesService.buscarVotante(
        busqueda.serie,
        busqueda.numero,
        mesaData.idCircuito,
        mesaData.idEleccion
      );
      
      if (votante) {
        setVotanteEncontrado(votante);
      } else {
        alert('Votante no encontrado o no habilitado para este circuito');
        setVotanteEncontrado(null);
      }
    } catch (err) {
      alert(`Error: ${err.message}`);
      setVotanteEncontrado(null);
    } finally {
      setBuscando(false);
    }
  };

  const marcarComoVotado = async (votante, observado = false) => {
    if (votante.ya_voto) {
      alert('Este votante ya fue marcado como votado');
      return;
    }

    const confirmar = window.confirm(
      `¿Confirma marcar como votado a:\n${votante.nombre} ${votante.apellido}\nCI: ${votante.ci_ciudadano}?`
    );

    if (!confirmar) return;

    try {
      await VotantesService.marcarComoVotado(
        votante.serie_credencial,
        votante.numero_credencial,
        mesaData.idCircuito,
        mesaData.idEleccion,
        observado
      );

      alert('Votante marcado como votado exitosamente');
      
      // Recargar lista
      await cargarVotantes(mesaData.idCircuito, mesaData.idEleccion);
      
      // Limpiar búsqueda
      setVotanteEncontrado(null);
      setBusqueda({ serie: '', numero: '' });
      
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  };

  const desmarcarVotado = async (votante) => {
    if (!votante.ya_voto) {
      alert('Este votante no está marcado como votado');
      return;
    }

    const confirmar = window.confirm(
      `¿Confirma DESMARCAR el voto de:\n${votante.nombre} ${votante.apellido}\nCI: ${votante.ci_ciudadano}?\n\nEsta acción debe usarse solo para correcciones.`
    );

    if (!confirmar) return;

    try {
      await VotantesService.desmarcarVotado(
        votante.serie_credencial,
        votante.numero_credencial,
        mesaData.idCircuito,
        mesaData.idEleccion
      );

      alert('Voto desmarcado exitosamente');
      
      // Recargar lista
      await cargarVotantes(mesaData.idCircuito, mesaData.idEleccion);
      
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  };

  const votantesFiltrados = votantes.filter(votante => {
    // Filtro por estado
    if (filtro === 'votaron' && !votante.ya_voto) return false;
    if (filtro === 'pendientes' && votante.ya_voto) return false;
    
    // Filtro por texto
    if (busquedaTexto) {
      const texto = busquedaTexto.toLowerCase();
      return (
        votante.nombre.toLowerCase().includes(texto) ||
        votante.apellido.toLowerCase().includes(texto) ||
        votante.ci_ciudadano.includes(texto) ||
        votante.serie_credencial.toLowerCase().includes(texto) ||
        votante.numero_credencial.includes(texto)
      );
    }
    
    return true;
  });

  if (loading) {
    return <div className="loading">Cargando lista de votantes...</div>;
  }

  if (error) {
    return (
      <div className="error-container">
        <h3>Error</h3>
        <p>{error}</p>
        <button onClick={() => navigate('/mesa')} className="btn volver">
          Volver a Mesa
        </button>
      </div>
    );
  }

  return (
    <div className="votantes-container">
      <div className="votantes-header">
        <h2>Lista de Votantes - Mesa {mesaData.numMesa}</h2>
        <div className="header-buttons">
          <button onClick={abrirTotem} className="btn blue">
            🗳️ Abrir Tótem de Votación
          </button>
          <button onClick={() => navigate('/mesa')} className="btn volver">
            Volver
          </button>
        </div>
      </div>

      {/* Debug info */}
      <div className="debug-info" style={{ marginBottom: '20px', padding: '10px', backgroundColor: '#f0f0f0', fontSize: '12px' }}>
        <h4>Datos de la Mesa:</h4>
        <p>Mesa: {mesaData.numMesa} | Circuito: {mesaData.idCircuito} | Elección: {mesaData.idEleccion} </p>
        <p>URL Tótem: /votar?numMesa={mesaData.numMesa}&idCircuito={mesaData.idCircuito}&idEleccion={mesaData.idEleccion}</p>
      </div>

      {/* Estadísticas */}
      <div className="estadisticas">
        <div className="stat-card">
          <h3>Habilitados</h3>
          <p className="stat-number">{estadisticas.total_habilitados || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Votaron</h3>
          <p className="stat-number votaron">{estadisticas.total_votaron || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Pendientes</h3>
          <p className="stat-number pendientes">{estadisticas.pendientes || 0}</p>
        </div>
      </div>

      {/* Búsqueda por credencial */}
      <div className="busqueda-credencial">
        <h3>Buscar por Credencial</h3>
        <div className="busqueda-form">
          <input
            type="text"
            placeholder="Serie (ej: A)"
            value={busqueda.serie}
            onChange={(e) => setBusqueda({...busqueda, serie: e.target.value.toUpperCase()})}
            maxLength="5"
          />
          <input
            type="text"
            placeholder="Número (ej: 1001)"
            value={busqueda.numero}
            onChange={(e) => setBusqueda({...busqueda, numero: e.target.value})}
            maxLength="5"
          />
          <button 
            onClick={buscarVotante} 
            disabled={buscando}
            className="btn buscar"
          >
            {buscando ? 'Buscando...' : 'Buscar'}
          </button>
        </div>

        {/* Resultado de búsqueda */}
        {votanteEncontrado && (
          <div className="votante-encontrado">
            <h4>Votante Encontrado:</h4>
            <div className="votante-info">
              <p><strong>Nombre:</strong> {votanteEncontrado.nombre} {votanteEncontrado.apellido}</p>
              <p><strong>CI:</strong> {votanteEncontrado.ci_ciudadano}</p>
              <p><strong>Credencial:</strong> {votanteEncontrado.serie_credencial}-{votanteEncontrado.numero_credencial}</p>
              <p><strong>Estado:</strong> 
                <span className={votanteEncontrado.ya_voto ? 'ya-voto' : 'pendiente'}>
                  {votanteEncontrado.ya_voto ? 'Ya votó' : 'Pendiente'}
                </span>
              </p>
            </div>
            <div className="votante-acciones">
              {!votanteEncontrado.ya_voto ? (
                <>
                  <button 
                    onClick={() => marcarComoVotado(votanteEncontrado, false)}
                    className="btn marcar-normal"
                  >
                    Marcar como Votado
                  </button>
                  <button 
                    onClick={() => marcarComoVotado(votanteEncontrado, true)}
                    className="btn marcar-observado"
                  >
                    Marcar como Observado
                  </button>
                </>
              ) : (
                <button 
                  onClick={() => desmarcarVotado(votanteEncontrado)}
                  className="btn desmarcar"
                >
                  Desmarcar Voto
                </button>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Filtros y búsqueda en lista */}
      <div className="filtros">
        <div className="filtros-estado">
          <button 
            className={filtro === 'todos' ? 'active' : ''}
            onClick={() => setFiltro('todos')}
          >
            Todos
          </button>
          <button 
            className={filtro === 'pendientes' ? 'active' : ''}
            onClick={() => setFiltro('pendientes')}
          >
            Pendientes
          </button>
          <button 
            className={filtro === 'votaron' ? 'active' : ''}
            onClick={() => setFiltro('votaron')}
          >
            Votaron
          </button>
        </div>
        <input
          type="text"
          placeholder="Buscar por nombre, CI o credencial..."
          value={busquedaTexto}
          onChange={(e) => setBusquedaTexto(e.target.value)}
          className="busqueda-texto"
        />
      </div>

      {/* Lista de votantes */}
      <div className="lista-votantes">
        <div className="votantes-count">
          Mostrando {votantesFiltrados.length} de {votantes.length} votantes
        </div>
        
        <div className="votantes-grid">
          {votantesFiltrados.map((votante, index) => (
            <div key={index} className={`votante-card ${votante.ya_voto ? 'votado' : 'pendiente'}`}>
                            <div className="votante-header">
                <h4>{votante.nombre} {votante.apellido}</h4>
                <span className={`estado ${votante.ya_voto ? 'votado' : 'pendiente'}`}>
                  {votante.ya_voto ? '✓ Votó' : '○ Pendiente'}
                  {votante.observado && ' (Obs.)'}
                </span>
              </div>
              <div className="votante-details">
                <p><strong>CI:</strong> {votante.ci_ciudadano}</p>
                <p><strong>Credencial:</strong> {votante.serie_credencial}-{votante.numero_credencial}</p>
                <p><strong>Fecha Nac:</strong> {new Date(votante.fecha_nac).toLocaleDateString()}</p>
              </div>
              <div className="votante-acciones">
                {!votante.ya_voto ? (
                  <>
                    <button 
                      onClick={() => marcarComoVotado(votante, false)}
                      className="btn-small marcar"
                    >
                      Marcar Voto
                    </button>
                    <button 
                      onClick={() => marcarComoVotado(votante, true)}
                      className="btn-small observado"
                    >
                      Observado
                    </button>
                  </>
                ) : (
                  <button 
                    onClick={() => desmarcarVotado(votante)}
                    className="btn-small desmarcar"
                  >
                    Desmarcar
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default Votantes;

