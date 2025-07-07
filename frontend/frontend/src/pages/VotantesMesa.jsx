import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Mesa.css';
import './Votantes.css';
import { useMesa } from '../context/MesaContext';
import { VotantesService } from '../services/votantesService';
import escudo from '../assets/escudo_uruguay.png';


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
  cargarVotantes(mesaDataParsed.idEleccion);
}, [mesaAbierta, navigate]);


  const cargarVotantes = async (idEleccion) => {
    try {
      setLoading(true);
      setError(null);
      
      // Cambio aquí: obtener todos los votantes de la elección
      const data = await VotantesService.getTodosLosVotantes(idEleccion);
      setVotantes(data.votantes);
      setEstadisticas(data.estadisticas);
    } catch (err) {
      setError(err.message);
      console.error('Error cargando votantes:', err);
    } finally {
      setLoading(false);
    }
  };

  // Actualizar la función abrirTotem:
  const abrirTotem = (observado = false) => {
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

    // Seleccionar la ruta correcta según el tipo
    const ruta = observado ? '/votar-observado' : '/votar';
    const urlTotem = `${ruta}?${params.toString()}`;
    
    console.log(`🗳️ Abriendo tótem ${observado ? 'OBSERVADO' : 'NORMAL'} con URL:`, urlTotem);
    console.log('Datos enviados:', { ...mesaData, observado });
    
    // Abrir en nueva pestaña
    const windowTitle = observado ? 'Tótem Observado' : 'Tótem Normal';
    window.open(urlTotem, '_blank', `width=1200,height=800,scrollbars=yes,resizable=yes,title=${windowTitle}`);
  };

  const buscarVotante = async () => {
    if (!busqueda.serie || !busqueda.numero) {
      alert('Ingrese serie y número de credencial');
      return;
    }

    try {
      setBuscando(true);
      const votante = await VotantesService.buscarVotanteGlobal(
        busqueda.serie,
        busqueda.numero,
        mesaData.idEleccion
      );
      
      if (votante) {
        setVotanteEncontrado(votante);
      } else {
        alert('Votante no encontrado');
        setVotanteEncontrado(null);
      }
    } catch (err) {
      alert(`Error: ${err.message}`);
      setVotanteEncontrado(null);
    } finally {
      setBuscando(false);
    }
  };

  const marcarComoVotado = async (votante) => {
    if (votante.ya_voto) {
      alert('Este votante ya fue marcado como votado');
      return;
    }

    // Determinar automáticamente si es observado
    const esObservado = votante.id_circuito_asignado !== mesaData.idCircuito;
    const tipoVoto = esObservado ? 'OBSERVADO' : 'NORMAL';

    const confirmar = window.confirm(
      `¿Confirma marcar como votado a:\n${votante.nombre} ${votante.apellido}\nCI: ${votante.ci_ciudadano}\n\nTipo de voto: ${tipoVoto}\n(Circuito asignado: ${votante.id_circuito_asignado}, Mesa actual: ${mesaData.idCircuito})`
    );

    if (!confirmar) return;

    try {
      await VotantesService.marcarComoVotado(
        votante.serie_credencial,
        votante.numero_credencial,
        mesaData.idCircuito, // Circuito donde vota (mesa actual)
        mesaData.idEleccion,
        esObservado
      );

      alert(`Votante marcado como votado exitosamente (${tipoVoto})`);
      
      // Recargar lista
      await cargarVotantes(mesaData.idEleccion);
      
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
      await cargarVotantes(mesaData.idEleccion);
      
    } catch (err) {
      alert(`Error: ${err.message}`);
    }
  };

  const votantesFiltrados = votantes.filter(votante => {
    // Filtro por estado
    if (filtro === 'votaron' && !votante.ya_voto) return false;
    if (filtro === 'pendientes' && votante.ya_voto) return false;
    if (filtro === 'observados' && (!votante.ya_voto || !votante.observado)) return false;
    if (filtro === 'normales' && (!votante.ya_voto || votante.observado)) return false;
    
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
        <div className="header-left">
          <div className="logo">
            <img src={escudo} alt="Escudo de Uruguay" />
            <div className="logo-text">
              <h3>CORTE ELECTORAL</h3>
              <small>República Oriental del Uruguay</small>
            </div>
          </div>
        </div>
        
        <div className="header-center">
          <h2>Lista de Votantes - Mesa {mesaData.numMesa}</h2>
          <small>Circuito {mesaData.idCircuito}</small>
        </div>
        
        <div className="header-right">
          <div className="header-buttons">
            <button onClick={() => abrirTotem(false)} className="btn blue">
              🗳️ Abrir Tótem Normal
            </button>
            <button onClick={() => abrirTotem(true)} className="btn orange">
              ⚠️ Abrir Tótem Observado
            </button>
            <button onClick={() => navigate('/mesa')} className="btn volver">
              Volver
            </button>
          </div>
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
          <h3>Total Votantes</h3>
          <p className="stat-number">{estadisticas.total_votantes || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Votaron</h3>
          <p className="stat-number votaron">{estadisticas.total_votaron || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Normales</h3>
          <p className="stat-number normales">{estadisticas.votos_normales || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Observados</h3>
          <p className="stat-number observados">{estadisticas.votos_observados || 0}</p>
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
              <p><strong>Circuito Asignado:</strong> {votanteEncontrado.id_circuito_asignado}</p>
              <p><strong>Mesa Actual:</strong> {mesaData.idCircuito}</p>
              <p><strong>Tipo de Voto:</strong> 
                <span className={votanteEncontrado.id_circuito_asignado === mesaData.idCircuito ? 'voto-normal' : 'voto-observado'}>
                  {votanteEncontrado.id_circuito_asignado === mesaData.idCircuito ? 'NORMAL' : 'OBSERVADO'}
                </span>
              </p>
              <p><strong>Estado:</strong> 
                <span className={votanteEncontrado.ya_voto ? 'ya-voto' : 'pendiente'}>
                  {votanteEncontrado.ya_voto ? 'Ya votó' : 'Pendiente'}
                  {votanteEncontrado.observado && ' (Observado)'}
                </span>
              </p>
            </div>
            <div className="votante-acciones">
              {!votanteEncontrado.ya_voto ? (
                <button 
                  onClick={() => marcarComoVotado(votanteEncontrado)}
                  className="btn marcar-votado"
                >
                  Marcar como Votado
                </button>
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
          <button 
            className={filtro === 'normales' ? 'active' : ''}
            onClick={() => setFiltro('normales')}
          >
            Votos Normales
          </button>
          <button 
            className={filtro === 'observados' ? 'active' : ''}
            onClick={() => setFiltro('observados')}
          >
            Votos Observados
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
            <div key={index} className={`votante-card ${votante.ya_voto ? 'votado' : 'pendiente'} ${votante.id_circuito_asignado !== mesaData.idCircuito ? 'observado' : 'normal'}`}>
              <div className="votante-header">
                <h4>{votante.nombre} {votante.apellido}</h4>
                <div className="estado-container">
                  <span className={`estado ${votante.ya_voto ? 'votado' : 'pendiente'}`}>
                    {votante.ya_voto ? '✓ Votó' : '○ Pendiente'}
                    {votante.observado && ' (Obs.)'}
                  </span>
                  <span className={`tipo-voto ${votante.id_circuito_asignado === mesaData.idCircuito ? 'normal' : 'observado'}`}>
                    {votante.id_circuito_asignado === mesaData.idCircuito ? 'NORMAL' : 'OBSERVADO'}
                  </span>
                </div>
              </div>
              <div className="votante-details">
                <p><strong>CI:</strong> {votante.ci_ciudadano}</p>
                <p><strong>Credencial:</strong> {votante.serie_credencial}-{votante.numero_credencial}</p>
                <p><strong>Fecha Nac:</strong> {new Date(votante.fecha_nac).toLocaleDateString()}</p>
                <p><strong>Circuito Asignado:</strong> {votante.id_circuito_asignado}</p>
                <p><strong>Mesa Actual:</strong> {mesaData.idCircuito}</p>
              </div>
              <div className="votante-acciones">
                {!votante.ya_voto ? (
                  <button 
                    onClick={() => marcarComoVotado(votante)}
                    className={`btn-small marcar ${votante.id_circuito_asignado === mesaData.idCircuito ? 'normal' : 'observado'}`}
                  >
                    Marcar como Votado
                    <small>({votante.id_circuito_asignado === mesaData.idCircuito ? 'Normal' : 'Observado'})</small>
                  </button>
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

