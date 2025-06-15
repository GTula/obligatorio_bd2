import React, { useState } from 'react';
import './Mesa.css';

function HomeMesa() {
  const [modalOpen, setModalOpen] = useState(false);
  const [accion, setAccion] = useState('');
  const [estadoMesa, setEstadoMesa] = useState('cerrada');
  const [mesaCerradaConfirmada, setMesaCerradaConfirmada] = useState(false);

  const abrirModal = (tipo) => {
    setAccion(tipo);
    setModalOpen(true);
  };

  const cerrarModal = () => {
    setModalOpen(false);
  };

  const confirmarAccion = () => {
    if (accion === 'abrir') {
      setEstadoMesa('abierta');
      setMesaCerradaConfirmada(false);
    } else if (accion === 'cerrar') {
      setEstadoMesa('cerrada');
      setMesaCerradaConfirmada(true);
    }
    cerrarModal();
  };

  return (
    <div className="container">
      <div className="sidebar">
        <div className="logo">
          <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/64/Coat_of_arms_of_Uruguay_%281829-1908%29.svg/330px-Coat_of_arms_of_Uruguay_%281829-1908%29.svg.png" alt="Logo" />
          <h3>
            CORTE ELECTORAL<br />
            <small>República Oriental del Uruguay</small>
          </h3>
        </div>

        <div className="sidebar-content">
          <nav>
            <p className="nav-title">Navegación</p>
            <ul>
              <li className={estadoMesa === 'abierta' ? 'enabled' : 'disabled'}>
                <span className="circle"></span> Lista Votantes
              </li>
              <li className={mesaCerradaConfirmada ? 'enabled' : 'disabled'}>
                <span className="circle"></span> Ver Resultados
              </li>
            </ul>
          </nav>

          <div className="mesa-status">
            <p>
              <strong>Estado de la mesa</strong><br />
              {estadoMesa.charAt(0).toUpperCase() + estadoMesa.slice(1)}
            </p>
            <button
              className="btn blue"
              onClick={() => abrirModal('abrir')}
              disabled={estadoMesa === 'abierta'}
            >
              Abrir Mesa
            </button>
            <button
              className="btn red"
              onClick={() => abrirModal('cerrar')}
              disabled={estadoMesa === 'cerrada'}
            >
              Cerrar Mesa
            </button>
          </div>
        </div>

        <footer>
          <p>Desarrollado por Soft<br /><small>Contacto: +598 91234567</small></p>
        </footer>
      </div>

      <div className="main">
        <h2>Bienvenido al administrador de la comisión receptora de votos</h2>
        <h3>Mesa Nº 3515</h3>

        <section className="stats-section">
          <div className="card">
            <h3>Estado</h3>
            <p className={`status ${estadoMesa}`}>
              {estadoMesa.charAt(0).toUpperCase() + estadoMesa.slice(1)}
            </p>
          </div>
          <div className="card">
            <h3>Habilitados</h3>
            <p>327</p>
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
