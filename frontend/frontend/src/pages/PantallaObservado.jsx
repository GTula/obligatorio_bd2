import React, { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import '../styles/PantallaVotacion.css';

function PantallaObservado() {
  const [searchParams] = useSearchParams();
  const [mesaInfo, setMesaInfo] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Estados para la votación
  const [eleccionInfo, setEleccionInfo] = useState(null);
  const [papeletas, setPapeletas] = useState([]);
  const [tipoVoto, setTipoVoto] = useState(''); // 'normal', 'blanco', 'anulado'
  const [papeletaSeleccionada, setPapeletaSeleccionada] = useState(null);
  const [votando, setVotando] = useState(false);
  const [votoCompletado, setVotoCompletado] = useState(false);

  useEffect(() => {
    // Leer parámetros de la URL
    const numMesa = searchParams.get('numMesa');
    const idCircuito = searchParams.get('idCircuito');
    const idEleccion = searchParams.get('idEleccion');
    const fecha = searchParams.get('fecha');

    console.log('Parámetros recibidos en tótem OBSERVADO:', { numMesa, idCircuito, idEleccion, fecha });

    // Validar que todos los parámetros estén presentes
    if (!numMesa || !idCircuito || !idEleccion) {
      setError('Faltan parámetros requeridos en la URL. Esta ventana debe abrirse desde la mesa.');
      setLoading(false);
      return;
    }

    // Guardar información de la mesa
    const info = {
      numMesa: parseInt(numMesa),
      idCircuito: parseInt(idCircuito),
      idEleccion: parseInt(idEleccion),
      fecha: fecha
    };

    setMesaInfo(info);
    
    // Cargar papeletas
    cargarPapeletas(info.idEleccion);

    console.log('✅ Tótem OBSERVADO configurado para mesa:', info);
  }, [searchParams]);

  const cargarPapeletas = async (idEleccion) => {
    try {
      setLoading(true);
      const response = await fetch(`http://127.0.0.1:5000/api/papeletas/eleccion/${idEleccion}`);
      
      if (response.ok) {
        const data = await response.json();
        setEleccionInfo(data.eleccion);
        setPapeletas(data.papeletas);
      } else {
        const error = await response.json();
        setError(`Error cargando papeletas: ${error.error}`);
      }
    } catch (error) {
      console.error('Error cargando papeletas:', error);
      setError('Error al conectar con el servidor');
    } finally {
      setLoading(false);
    }
  };

  const confirmarVoto = async () => {
    if (!tipoVoto) {
      alert('Debe seleccionar un tipo de voto');
      return;
    }

    if (tipoVoto === 'normal' && !papeletaSeleccionada) {
      alert('Debe seleccionar una papeleta');
      return;
    }

    const confirmacion = window.confirm(
      `¿Confirma su voto ${tipoVoto.toUpperCase()} OBSERVADO?${
        tipoVoto === 'normal' ? `\nPapeleta seleccionada: ${getPapeletaTexto(papeletaSeleccionada)}` : ''
      }\n\n⚠️ ESTE VOTO SERÁ MARCADO COMO OBSERVADO`
    );

    if (!confirmacion) return;

    try {
      setVotando(true);
      
      const votoData = {
        id_circuito: mesaInfo.idCircuito,
        id_eleccion: mesaInfo.idEleccion,
        tipo_voto: tipoVoto,
        observado: true // ← SIEMPRE observado en esta pantalla
      };

      if (tipoVoto === 'normal') {
        votoData.id_papeleta = papeletaSeleccionada.id;
      }

      const response = await fetch('http://127.0.0.1:5000/api/papeletas/votar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(votoData)
      });

      if (response.ok) {
        const result = await response.json();
        console.log('Voto OBSERVADO registrado:', result);
        setVotoCompletado(true);
        
        // Auto-cerrar después de 3 segundos
        setTimeout(() => {
          window.close();
        }, 3000);
      } else {
        const error = await response.json();
        alert(`Error registrando voto: ${error.error}`);
      }
    } catch (error) {
      console.error('Error registrando voto:', error);
      alert('Error al conectar con el servidor');
    } finally {
      setVotando(false);
    }
  };

  const getPapeletaTexto = (papeleta) => {
    if (!papeleta) return '';
    
    if (eleccionInfo?.id_tipo_eleccion === 3) {
      // Plebiscito
      return `${papeleta.nombre}: ${papeleta.valor}`;
    } else {
      // Otras elecciones
      return `${papeleta.partido} - ${papeleta.organo} (${papeleta.departamento})`;
    }
  };

  const reiniciarVoto = () => {
    setTipoVoto('');
    setPapeletaSeleccionada(null);
    setVotoCompletado(false);
  };

  const cerrarTotem = () => {
    if (window.confirm('¿Está seguro que desea cerrar el tótem observado?')) {
      window.close();
    }
  };

  if (loading) {
    return (
      <div className="totem-loading observado">
        <h2>⚠️ Cargando Sistema de Votación OBSERVADO...</h2>
        <div className="spinner"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="totem-error observado">
        <h2>❌ Error en el Tótem Observado</h2>
        <p>{error}</p>
        <button onClick={cerrarTotem} className="btn-error">
          Cerrar Tótem
        </button>
      </div>
    );
  }

  if (votoCompletado) {
    return (
      <div className="totem-success observado">
        <div className="success-content">
          <h1>✅ VOTO OBSERVADO REGISTRADO</h1>
          <div className="success-details">
            <p><strong>Tipo de voto:</strong> {tipoVoto.toUpperCase()}</p>
            {tipoVoto === 'normal' && (
              <p><strong>Selección:</strong> {getPapeletaTexto(papeletaSeleccionada)}</p>
            )}
            <p className="observado-badge">⚠️ VOTO OBSERVADO</p>
          </div>
          <p className="auto-close">Esta ventana se cerrará automáticamente...</p>
          <button onClick={() => window.close()} className="btn-close">
            Cerrar Ahora
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="totem-container observado">
      {/* Header del tótem observado */}
      <div className="totem-header observado">
        <h1>⚠️ SISTEMA DE VOTACIÓN OBSERVADO</h1>
        <div className="observado-badge-large">
          ⚠️ MODO OBSERVADO - TODOS LOS VOTOS SERÁN MARCADOS COMO OBSERVADOS
        </div>
        <div className="mesa-info">
          <span>Mesa: {mesaInfo.numMesa}</span>
          <span>Circuito: {mesaInfo.idCircuito}</span>
          <span>Elección: {eleccionInfo?.tipo_eleccion || 'Cargando...'}</span>
          <button onClick={cerrarTotem} className="btn-close-header">❌</button>
        </div>
      </div>

      {/* Contenido principal */}
      <div className="totem-content">
        <div className="voting-section observado">
          <h2>Seleccione su opción de voto (OBSERVADO)</h2>
          
          {/* Opciones de tipo de voto */}
          <div className="vote-type-section">
            <h3>Tipo de Voto</h3>
            <div className="vote-type-buttons">
              <button 
                className={`vote-type-btn observado ${tipoVoto === 'normal' ? 'selected' : ''}`}
                onClick={() => setTipoVoto('normal')}
              >
                <span className="vote-icon">✓</span>
                <span>VOTO NORMAL (OBSERVADO)</span>
                <small>Seleccionar una opción</small>
              </button>
              
              <button 
                className={`vote-type-btn observado ${tipoVoto === 'blanco' ? 'selected' : ''}`}
                onClick={() => setTipoVoto('blanco')}
              >
                <span className="vote-icon">⬜</span>
                <span>VOTO EN BLANCO (OBSERVADO)</span>
                <small>No seleccionar ninguna opción</small>
              </button>
              
              <button 
                className={`vote-type-btn observado ${tipoVoto === 'anulado' ? 'selected' : ''}`}
                onClick={() => setTipoVoto('anulado')}
              >
                <span className="vote-icon">❌</span>
                <span>VOTO ANULADO (OBSERVADO)</span>
                <small>Anular el voto</small>
              </button>
            </div>
          </div>

          {/* Selección de papeletas (solo si es voto normal) */}
          {tipoVoto === 'normal' && (
            <div className="papeletas-section">
              <h3>Seleccione una opción</h3>
              <div className="papeletas-grid">
                {papeletas.map((papeleta, index) => (
                  <div 
                    key={index}
                    className={`papeleta-card observado ${papeletaSeleccionada?.id === papeleta.id ? 'selected' : ''}`}
                    onClick={() => setPapeletaSeleccionada(papeleta)}
                  >
                    {eleccionInfo?.id_tipo_eleccion === 3 ? (
                      // Plebiscito
                      <div className="papeleta-plebiscito">
                        <h4>{papeleta.nombre}</h4>
                        <div className={`valor-plebiscito ${papeleta.valor.toLowerCase()}`}>
                          {papeleta.valor}
                        </div>
                      </div>
                    ) : (
                      // Otras elecciones
                      <div className="papeleta-partido">
                        <h4>{papeleta.partido}</h4>
                        <p><strong>Órgano:</strong> {papeleta.organo}</p>
                        <p><strong>Departamento:</strong> {papeleta.departamento}</p>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Resumen del voto */}
          {tipoVoto && (
            <div className="vote-summary observado">
              <h3>Resumen de su voto</h3>
              <div className="summary-content">
                <p><strong>Tipo:</strong> {tipoVoto.toUpperCase()}</p>
                {tipoVoto === 'normal' && papeletaSeleccionada && (
                  <p><strong>Selección:</strong> {getPapeletaTexto(papeletaSeleccionada)}</p>
                )}
                <p className="observado-text">⚠️ VOTO OBSERVADO</p>
              </div>
            </div>
          )}

          {/* Botones de acción */}
          <div className="action-buttons">
            <button 
              onClick={reiniciarVoto}
              className="btn-secondary"
              disabled={votando}
            >
              🔄 Reiniciar
            </button>
            
            <button 
              onClick={confirmarVoto}
              className="btn-confirm observado"
              disabled={votando || !tipoVoto || (tipoVoto === 'normal' && !papeletaSeleccionada)}
            >
              {votando ? '⏳ Registrando...' : '⚠️ CONFIRMAR VOTO OBSERVADO'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default PantallaObservado;
