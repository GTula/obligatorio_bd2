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
  const [tiempoRestante, setTiempoRestante] = useState('');

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
    const actualizarTiempo = () => {
      const ahora = new Date();
      const finDelDia = new Date();
      finDelDia.setHours(23, 59, 59, 999);
      
      const diferencia = finDelDia - ahora;
      
      if (diferencia > 0) {
        const horas = Math.floor(diferencia / (1000 * 60 * 60));
        const minutos = Math.floor((diferencia % (1000 * 60 * 60)) / (1000 * 60));
        setTiempoRestante(`${horas}h ${minutos}min`);
      } else {
        setTiempoRestante('Tiempo finalizado');
      }
    };

    // Actualizar inmediatamente
    actualizarTiempo();
    
    // Actualizar cada minuto
    const intervalo = setInterval(actualizarTiempo, 60000);
    
    return () => clearInterval(intervalo);
  }, []);

  useEffect(() => {
  const fetchCircuitoInfo = async () => {
    const mesaId = localStorage.getItem('mesa_id');
    const fecha = localStorage.getItem('fecha_eleccion');
    
    if (!mesaId || !fecha) {
      console.error('❌ No mesa information found');
      return;
    }

    console.log('🔍 Fetching circuito info for:', { mesaId, fecha });

    try {
      const response = await fetch(`http://127.0.0.1:5000/api/circuito/por-mesa?num_mesa=${mesaId}&fecha=${fecha}`);
      const data = await response.json();
      console.log('✅ Circuito info response:', data);
      
      if (response.ok) {
        setCircuitoInfo(data);
        
        const idCircuito = data.ID_Circuito || data.id_circuito || data.idCircuito;
        const idEleccion = data.ID_Eleccion || data.id_eleccion || data.idEleccion || 1;
        
        console.log('🔍 IDs extraídos:', { idCircuito, idEleccion });
        
        if (idCircuito) {
          localStorage.setItem('id_circuito', idCircuito.toString());
          localStorage.setItem('id_eleccion', idEleccion.toString());
          
          console.log('✅ Guardado en localStorage:', {
            id_circuito: localStorage.getItem('id_circuito'),
            id_eleccion: localStorage.getItem('id_eleccion')
          });
        } else {
          console.error('❌ No se pudo obtener ID_Circuito de la respuesta');
        }
        
        // Actualizar mesaData
        setMesaData(prev => ({
          ...prev,
          numMesa: parseInt(mesaId),
          idCircuito: idCircuito,
          idEleccion: idEleccion,
          fecha: fecha
        }));
      } else {
        console.error('❌ Error fetching circuito info:', data.error);
      }
    } catch (error) {
      console.error('❌ Error fetching circuito info:', error);
    }
  };

  fetchCircuitoInfo();
  }, []);

  useEffect(() => {
 
    const idEleccion = localStorage.getItem('id_eleccion') || 1; 
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
            <p className="stat-number tiempo">{tiempoRestante}</p>
          </div>
        </section>

        {/* Información de la mesa - estilo coherente */}
        <section className="debug-info">
          <h4>Información de la Mesa</h4>
          <div className="debug-info-grid">
            <div className="debug-info-item mesa">
              <div className="label">Mesa</div>
              <div className={`value ${!mesaData.numMesa ? 'null' : ''}`}>
                {mesaData.numMesa || 'Cargando...'}
              </div>
            </div>
            <div className="debug-info-item circuito">
              <div className="label">Circuito</div>
              <div className={`value ${!mesaData.idCircuito ? 'null' : ''}`}>
                {mesaData.idCircuito || 'Cargando...'}
              </div>
            </div>
            <div className="debug-info-item eleccion">
              <div className="label">Elección</div>
              <div className={`value ${!mesaData.idEleccion ? 'null' : ''}`}>
                {mesaData.idEleccion || 'Cargando...'}
              </div>
            </div>
            <div className="debug-info-item fecha">
              <div className="label">Fecha</div>
              <div className={`value ${!mesaData.fecha ? 'null' : ''}`}>
                {mesaData.fecha || 'Cargando...'}
              </div>
            </div>
          </div>
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
