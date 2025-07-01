// HomeMesa.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Mesa.css';
import { useMesa } from '../context/MesaContext';
import escudo from '../assets/escudo_uruguay.png';

function HomeMesa() {
  const [modalOpen, setModalOpen] = useState(false);
  const [accion, setAccion] = useState('');
  const [circuitoInfo, setCircuitoInfo] = useState(null);
  const navigate = useNavigate();
  const {
    mesaAbierta,
    mesaCerrada,
    abrirMesa,
    cerrarMesa,
    puedeVerVotantes,
    puedeVerResultados,
  } = useMesa();

  // Estados para los datos de la mesa
  const [mesaData, setMesaData] = useState({
    numMesa: null,
    idEleccion: null,
    fecha: null
  });

  useEffect(() => {
    const fetchCircuitoInfo = async () => {
      const mesaId = localStorage.getItem('mesa_id');
      const fecha = localStorage.getItem('fecha_eleccion');
      
      if (!mesaId || !fecha) {
        console.error('No mesa information found');
        return;
      }

      // Actualizar mesaData con la información disponible
      setMesaData(prev => ({
        ...prev,
        numMesa: parseInt(mesaId),
        fecha: fecha
      }));

      console.log('Fetching circuito info for:', { mesaId, fecha });

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/circuito/por-mesa?num_mesa=${mesaId}&fecha=${fecha}`);
        const data = await response.json();
        console.log('Circuito info response:', data);
        
        if (response.ok) {
          setCircuitoInfo(data);
          // Actualizar mesaData con el ID del circuito
          setMesaData(prev => ({
            ...prev,
            idCircuito: data.ID_Circuito
          }));
        } else {
          console.error('Error fetching circuito info:', data.error);
        }
      } catch (error) {
        console.error('Error fetching circuito info:', error);
      }
    };

    fetchCircuitoInfo();
  }, []);

  // Obtener ID de elección (puedes ajustar esto según tu lógica)
  useEffect(() => {
    // Aquí deberías obtener el ID de elección según tu lógica de negocio
    // Por ejemplo, desde localStorage, una API, o props
    const idEleccion = localStorage.getItem('id_eleccion') || 1; // Valor por defecto
    setMesaData(prev => ({
      ...prev,
      idEleccion: parseInt(idEleccion)
    }));
  }, []);

  const abrirModal = (tipo) => {
    setAccion(tipo);
    setModalOpen(true);
  };

  const cerrarModal = () => {
    setModalOpen(false);
  };

  const confirmarAccion = () => {
    if (accion === 'abrir') {
      abrirMesa();
    } else if (accion === 'cerrar') {
      // Pasar los datos de la mesa al contexto antes de cerrar
      cerrarMesa(mesaData);
    }
    cerrarModal();
  };

  // Función para navegar a resultados (solo si la mesa está cerrada)
  const navegarAResultados = () => {
    if (puedeVerResultados && mesaCerrada) {
      navigate('/resultados');
    }
  };

  return (
    <div className="container">
      <div className="sidebar">
        <div className="logo">
          <img src={escudo} alt="Escudo de Uruguay" />
          <h3>
            CORTE ELECTORAL<br />
            <small>República Oriental del Uruguay</small>
          </h3>
        </div>
        <nav>
          <p className="nav-title">Navegación</p>
          <ul>
            <li
              className={puedeVerVotantes ? 'activo' : 'inactivo'}
              onClick={() => puedeVerVotantes && navigate('/votantes')}
            >
              <span className="circle"></span> Lista Votantes
            </li>
            <li
              className={puedeVerResultados ? 'activo' : 'inactivo'}
              onClick={navegarAResultados}
            >
              <span className="circle"></span> Ver Resultados
            </li>
          </ul>
        </nav>
        <div className="mesa-status">
          <p><strong>Estado de la mesa</strong><br />
            {mesaAbierta ? 'Abierta' : mesaCerrada ? 'Cerrada' : 'Sin iniciar'}
          </p>
          <button 
            className="btn blue" 
            disabled={mesaAbierta || mesaCerrada} 
            onClick={() => abrirModal('abrir')}
          >
            Abrir Mesa
          </button>
          <button 
            className="btn red" 
            disabled={!mesaAbierta || mesaCerrada} 
            onClick={() => abrirModal('cerrar')}
          >
            Cerrar Mesa
          </button>
        </div>
      </div>

      <div className="main">
        <h2>Bienvenido al administrador de la comisión receptora de votos</h2>
        <h3>Mesa Nº {mesaData.numMesa || 'Cargando...'}</h3>
        <h4>Circuito Nº {circuitoInfo?.ID_Circuito || 'Cargando...'}</h4>

        <section className="stats-section">
          <div className="card">
            <h3>Estado</h3>
            <p className={`status ${mesaAbierta ? 'abierto' : 'cerrado'}`}>
              {mesaAbierta ? 'Abierta' : mesaCerrada ? 'Cerrada' : 'Sin iniciar'}
            </p>
          </div>
          <div className="card">
            <h3>Habilitados</h3>
            <p>0</p>
          </div>
          <div className="card">
            <h3>Votaron</h3>
            <p>0</p>
          </div>
          <div className="card">
            <h3>Tiempo restante</h3>
            <p>8h 30min</p>
          </div>
        </section>

        {/* Información de debug (puedes remover en producción) */}
        <section className="debug-info" style={{ marginTop: '20px', padding: '10px', backgroundColor: '#f0f0f0', fontSize: '12px' }}>
          <h4>Información de Mesa (Debug)</h4>
          <p>Mesa: {mesaData.numMesa}</p>
          <p>Circuito: {mesaData.idCircuito}</p>
          <p>Elección: {mesaData.idEleccion}</p>
          <p>Fecha: {mesaData.fecha}</p>
        </section>
      </div>

      {modalOpen && (
        <div className="modal">
          <div className="modal-content">
            <span className="icon">ℹ️</span>
            <p>¿Estás seguro que deseas {accion === 'abrir' ? 'abrir' : 'cerrar'} la mesa?</p>
            {accion === 'cerrar' && (
              <div className="mesa-info">
                <p><small>Se guardarán los datos de la mesa para consultar resultados</small></p>
              </div>
            )}
            <div className="modal-buttons">
              <button className="btn red" onClick={cerrarModal}>Cancelar</button>
              <button className="btn green" onClick={confirmarAccion}>Aceptar</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default HomeMesa;
