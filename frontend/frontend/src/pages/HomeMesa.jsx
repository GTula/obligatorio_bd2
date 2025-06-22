// HomeMesa.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Mesa.css';
import { useMesa } from '../context/MesaContext';

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

  useEffect(() => {
    const fetchCircuitoInfo = async () => {
      const mesaId = localStorage.getItem('mesa_id');
      const fecha = localStorage.getItem('fecha_eleccion');
      
      if (!mesaId || !fecha) {
        console.error('No mesa information found');
        return;
      }

      console.log('Fetching circuito info for:', { mesaId, fecha });

      try {
        const response = await fetch(`http://127.0.0.1:5000/api/circuito/por-mesa?num_mesa=${mesaId}&fecha=${fecha}`);
        const data = await response.json();
        console.log('Circuito info response:', data);
        
        if (response.ok) {
          setCircuitoInfo(data);
        } else {
          console.error('Error fetching circuito info:', data.error);
        }
      } catch (error) {
        console.error('Error fetching circuito info:', error);
      }
    };

    fetchCircuitoInfo();
  }, []);

  const abrirModal = (tipo) => {
    setAccion(tipo);
    setModalOpen(true);
  };

  const cerrarModal = () => {
    setModalOpen(false);
  };

  const confirmarAccion = () => {
    if (accion === 'abrir') abrirMesa();
    else if (accion === 'cerrar') cerrarMesa();
    cerrarModal();
  };

  return (
    <div className="container">
      <div className="sidebar">
        <div className="logo">
          <img src="..\pictures\Coat_of_arms_of_Uruguay.svg.png" alt="Logo" />
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
              onClick={() => puedeVerResultados && navigate('/resultados')}
            >
              <span className="circle"></span> Ver Resultados
            </li>
          </ul>
        </nav>
        <div className="mesa-status">
          <p><strong>Estado de la mesa</strong><br />
            {mesaAbierta ? 'Abierta' : mesaCerrada ? 'Cerrada' : 'Sin iniciar'}
          </p>
          <button className="btn blue" disabled={mesaAbierta || mesaCerrada} onClick={() => abrirModal('abrir')}>Abrir Mesa</button>
          <button className="btn red" disabled={!mesaAbierta || mesaCerrada} onClick={() => abrirModal('cerrar')}>Cerrar Mesa</button>
        </div>
        <footer>
          <p>Desarrollado por Soft<br /><small>Contacto: +598 91234567</small></p>
        </footer>
      </div>

      <div className="main">
        <h2>Bienvenido al administrador de la comisión receptora de votos</h2>
        <h3>Mesa Nº {localStorage.getItem('mesa_id') || 'Cargando...'}</h3>
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
      </div>

      {modalOpen && (
        <div className="modal">
          <div className="modal-content">
            <span className="icon">ℹ️</span>
            <p>¿Estás seguro que deseas {accion === 'abrir' ? 'abrir' : 'cerrar'} la mesa?</p>
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