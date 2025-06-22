import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Mesa.css';
import { useMesa } from '../context/MesaContext';

function VotantesMesa() {
  const navigate = useNavigate();
  const { mesaAbierta } = useMesa();
  const [votantes, setVotantes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchVotantes = async () => {
      try {
        const mesaId = localStorage.getItem('mesa_id');
        const fecha = localStorage.getItem('fecha_eleccion');
        const idEleccion = localStorage.getItem('id_eleccion');
        
        if (!mesaId || !fecha || !idEleccion) {
          setError('Falta información necesaria');
          setLoading(false);
          return;
        }

        // Primero obtenemos el circuito
        const circuitoRes = await fetch(`http://127.0.0.1:5000/api/circuito/por-mesa?num_mesa=${mesaId}&fecha=${fecha}`);
        const circuitoData = await circuitoRes.json();
        
        if (!circuitoRes.ok) {
          setError(circuitoData.error || 'Error al obtener el circuito');
          setLoading(false);
          return;
        }

        // Ahora pedimos los votantes del circuito
        const votantesRes = await fetch(
          `http://127.0.0.1:5000/api/circuito/votantes-circuito?id_circuito=${circuitoData.ID_Circuito}&id_eleccion=${idEleccion}`
        );
        const votantesData = await votantesRes.json();

        if (!votantesRes.ok) {
          setError(votantesData.error || 'Error al obtener los votantes');
          setLoading(false);
          return;
        }

        setVotantes(Array.isArray(votantesData) ? votantesData : []);
        setLoading(false);
      } catch (error) {
        console.error('Error:', error);
        setError('Error al cargar los votantes');
        setLoading(false);
      }
    };

    fetchVotantes();
  }, []);

  if (loading) return <div>Cargando...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="votantes-container">
      <h2>Lista de Votantes</h2>
      {votantes.length === 0 ? (
        <p>No hay votantes asignados a este circuito</p>
      ) : (
        <ul className="votante-lista">
          {votantes.map((v, i) => (
            <li key={i} className="votante">
              <span>
                {v.Nombre} {v.Apellido} - Credencial: {v.serie} {v.numero} - CI: {v.CI}
              </span>
              {mesaAbierta && (
                <button className="btn-voto">🗳️ Marcar como votó</button>
              )}
            </li>
          ))}
        </ul>
      )}
      <button className="btn volver" onClick={() => navigate('/mesa')}>Volver</button>
    </div>
  );
}

export default VotantesMesa;