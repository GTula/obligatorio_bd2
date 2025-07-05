import React, { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import '../styles/PantallaVotacion.css';

function PantallaVotacion() {
  const [searchParams] = useSearchParams();
  const [mesaInfo, setMesaInfo] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Estados para la votación
  const [credencial, setCredencial] = useState({
    serie: '',
    numero: ''
  });
  const [votanteInfo, setVotanteInfo] = useState(null);
  const [buscandoVotante, setBuscandoVotante] = useState(false);

  useEffect(() => {
    // Leer parámetros de la URL
    const numMesa = searchParams.get('numMesa');
    const idCircuito = searchParams.get('idCircuito');
    const idEleccion = searchParams.get('idEleccion');
    const fecha = searchParams.get('fecha');

    console.log('Parámetros recibidos en tótem:', { numMesa, idCircuito, idEleccion, fecha });

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
    setLoading(false);

    console.log('✅ Tótem configurado para mesa:', info);
  }, [searchParams]);

  const buscarVotante = async () => {
    if (!credencial.serie || !credencial.numero) {
      alert('Por favor ingrese serie y número de credencial');
      return;
    }

    setBuscandoVotante(true);
    setVotanteInfo(null);

    try {
      const response = await fetch(`http://127.0.0.1:5000/api/votantes/buscar?serie=${credencial.serie}&numero=${credencial.numero}&id_circuito=${mesaInfo.idCircuito}&id_eleccion=${mesaInfo.idEleccion}`);
      
      if (response.ok) {
        const votante = await response.json();
        setVotanteInfo(votante);
        
        if (votante.ya_voto) {
          alert('Esta credencial ya fue utilizada para votar');
        }
      } else if (response.status === 404) {
        alert('Credencial no encontrada o no habilitada para este circuito');
      } else {
        const error = await response.json();
        alert(`Error: ${error.error}`);
      }
    } catch (error) {
      console.error('Error buscando votante:', error);
      alert('Error al conectar con el servidor');
    } finally {
      setBuscandoVotante(false);
    }
  };

  const limpiarFormulario = () => {
    setCredencial({ serie: '', numero: '' });
    setVotanteInfo(null);
  };

  const cerrarTotem = () => {
    if (window.confirm('¿Está seguro que desea cerrar el tótem?')) {
      window.close();
    }
  };

  if (loading) {
    return (
      <div style={{ 
        display: 'flex', 
        flexDirection: 'column', 
        alignItems: 'center', 
        justifyContent: 'center', 
        height: '100vh',
        backgroundColor: '#f0f8ff'
      }}>
        <h2>🗳️ Iniciando Tótem de Votación...</h2>
        <div style={{ 
          border: '4px solid #f3f3f3',
          borderTop: '4px solid #3498db',
          borderRadius: '50%',
          width: '40px',
          height: '40px',
          animation: 'spin 2s linear infinite'
        }}></div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ 
        display: 'flex', 
        flexDirection: 'column', 
        alignItems: 'center', 
        justifyContent: 'center', 
        height: '100vh',
        backgroundColor: '#ffe6e6',
        padding: '20px'
      }}>
        <h2>❌ Error en el Tótem</h2>
        <p>{error}</p>
        <p>La URL debe contener los parámetros: numMesa, idCircuito, idEleccion</p>
        <button 
          onClick={cerrarTotem}
          style={{
            padding: '10px 20px',
            backgroundColor: '#dc3545',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            marginTop: '20px'
          }}
        >
          Cerrar Tótem
        </button>
      </div>
    );
  }

  return (
    <div style={{ 
      minHeight: '100vh', 
      backgroundColor: '#f8f9fa',
      fontFamily: 'Arial, sans-serif'
    }}>
      {/* Header del tótem */}
      <div style={{
        backgroundColor: '#007bff',
        color: 'white',
        padding: '20px',
        textAlign: 'center',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
      }}>
        <h1 style={{ margin: '0 0 10px 0' }}>🗳️ TÓTEM DE VOTACIÓN ELECTRÓNICA</h1>
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          maxWidth: '800px',
          margin: '0 auto'
        }}>
          <div style={{ fontSize: '14px' }}>
            <strong>Mesa:</strong> {mesaInfo.numMesa} | 
            <strong> Circuito:</strong> {mesaInfo.idCircuito} | 
            <strong> Elección:</strong> {mesaInfo.idEleccion}
            {mesaInfo.fecha && <span> | <strong>Fecha:</strong> {mesaInfo.fecha}</span>}
          </div>
          <button 
            onClick={cerrarTotem}
            style={{
              padding: '8px 16px',
              backgroundColor: '#dc3545',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer',
              fontSize: '12px'
            }}
          >
            ❌ Cerrar Tótem
          </button>
        </div>
      </div>

      {/* Contenido principal */}
      <div style={{ 
        maxWidth: '600px', 
        margin: '40px auto', 
        padding: '0 20px' 
      }}>    
        {/* Bienvenida */}
        <div style={{
          backgroundColor: 'white',
          padding: '30px',
          borderRadius: '10px',
          boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
          marginBottom: '30px',
          textAlign: 'center'
        }}>
          <h2 style={{ color: '#007bff', marginBottom: '15px' }}>
            Bienvenido al Sistema de Votación Electrónica
          </h2>
          <p style={{ fontSize: '16px', color: '#666', margin: '0' }}>
            Para votar, ingrese los datos de su credencial cívica
          </p>
        </div>

        {/* Formulario de credencial */}
        <div style={{
          backgroundColor: 'white',
          padding: '30px',
          borderRadius: '10px',
          boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
          marginBottom: '30px'
        }}>
          <h3 style={{ marginBottom: '20px', color: '#333' }}>
            Ingrese su Credencial Cívica
          </h3>
          
          <div style={{ marginBottom: '20px' }}>
            <label style={{ 
              display: 'block', 
              marginBottom: '8px', 
              fontWeight: 'bold',
              color: '#555'
            }}>
              Serie:
            </label>
            <input 
              type="text" 
              placeholder="Ej: A" 
              maxLength="5"
              value={credencial.serie}
              onChange={(e) => setCredencial({
                ...credencial, 
                serie: e.target.value.toUpperCase()
              })}
              style={{
                width: '100%',
                padding: '12px',
                fontSize: '16px',
                border: '2px solid #ddd',
                borderRadius: '5px',
                boxSizing: 'border-box'
              }}
            />
          </div>
          
          <div style={{ marginBottom: '20px' }}>
            <label style={{ 
              display: 'block', 
              marginBottom: '8px', 
              fontWeight: 'bold',
              color: '#555'
            }}>
              Número:
            </label>
            <input 
              type="text" 
              placeholder="Ej: 1001"
              maxLength="10"
              value={credencial.numero}
              onChange={(e) => setCredencial({
                ...credencial, 
                numero: e.target.value
              })}
              style={{
                width: '100%',
                padding: '12px',
                fontSize: '16px',
                border: '2px solid #ddd',
                borderRadius: '5px',
                boxSizing: 'border-box'
              }}
            />
          </div>

          <div style={{ 
            display: 'flex', 
            gap: '10px',
            justifyContent: 'center'
          }}>
            <button 
              onClick={buscarVotante}
              disabled={buscandoVotante || !credencial.serie || !credencial.numero}
              style={{
                padding: '12px 24px',
                backgroundColor: buscandoVotante ? '#6c757d' : '#28a745',
                color: 'white',
                border: 'none',
                borderRadius: '5px',
                cursor: buscandoVotante ? 'not-allowed' : 'pointer',
                fontSize: '16px',
                fontWeight: 'bold'
              }}
            >
              {buscandoVotante ? '🔍 Buscando...' : '🔍 Buscar Votante'}
            </button>
            
            <button 
              onClick={limpiarFormulario}
              style={{
                padding: '12px 24px',
                backgroundColor: '#6c757d',
                color: 'white',
                border: 'none',
                borderRadius: '5px',
                cursor: 'pointer',
                fontSize: '16px'
              }}
            >
              🗑️ Limpiar
            </button>
          </div>
        </div>

        {/* Información del votante */}
        {votanteInfo && (
          <div style={{
            backgroundColor: votanteInfo.ya_voto ? '#f8d7da' : '#d4edda',
            border: `1px solid ${votanteInfo.ya_voto ? '#f5c6cb' : '#c3e6cb'}`,
            padding: '20px',
            borderRadius: '10px',
            marginBottom: '30px'
          }}>
            <h3 style={{ 
              color: votanteInfo.ya_voto ? '#721c24' : '#155724',
              marginBottom: '15px'
            }}>
              {votanteInfo.ya_voto ? '❌ Votante Ya Votó' : '✅ Votante Encontrado'}
            </h3>
            
            <div style={{ fontSize: '16px', lineHeight: '1.6' }}>
              <p><strong>Nombre:</strong> {votanteInfo.nombre} {votanteInfo.apellido}</p>
              <p><strong>CI:</strong> {votanteInfo.ci_ciudadano}</p>
              <p><strong>Credencial:</strong> {votanteInfo.serie_credencial}-{votanteInfo.numero_credencial}</p>
              <p><strong>Estado:</strong> 
                <span style={{ 
                  fontWeight: 'bold',
                  color: votanteInfo.ya_voto ? '#721c24' : '#155724'
                }}>
                  {votanteInfo.ya_voto ? ' Ya votó' : ' Habilitado para votar'}
                  {votanteInfo.observado && ' (Observado)'}
                </span>
              </p>
            </div>

            {!votanteInfo.ya_voto && (
              <div style={{ marginTop: '20px', textAlign: 'center' }}>
                <button
                  style={{
                    padding: '15px 30px',
                    backgroundColor: '#007bff',
                    color: 'white',
                    border: 'none',
                    borderRadius: '8px',
                    cursor: 'pointer',
                    fontSize: '18px',
                    fontWeight: 'bold'
                  }}
                  onClick={() => alert('Aquí iría la pantalla de votación')}
                >
                  ➡️ CONTINUAR A VOTAR
                </button>
              </div>
            )}
          </div>
        )}

        {/* Instrucciones */}
        <div style={{
          backgroundColor: '#e9ecef',
          padding: '20px',
          borderRadius: '10px',
          fontSize: '14px',
          color: '#495057'
        }}>
          <h4 style={{ marginBottom: '10px' }}>📋 Instrucciones:</h4>
          <ul style={{ margin: '0', paddingLeft: '20px' }}>
            <li>Ingrese la serie y número de su credencial cívica</li>
            <li>Presione "Buscar Votante" para verificar sus datos</li>
            <li>Si está habilitado, podrá continuar con el proceso de votación</li>
            <li>Si ya votó, no podrá votar nuevamente</li>
          </ul>
        </div>
      </div>

      {/* Estilos CSS para la animación del spinner */}
      <style jsx>{`
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}

export default PantallaVotacion;

