import { useContext, useState } from "react";
import { mesaAuthContext } from "../App";
import { useNavigate } from "react-router-dom";
import "./Login.css";

function LoginMesa() {
  const [numero, setNumero] = useState('');
  const [error, setError] = useState('');
  const [isAuthenticated, setIsAuthenticated] = useContext(mesaAuthContext);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch('http://127.0.0.1:5000/api/login_presidente', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ numero })
      });

      const data = await res.json();
      if (res.ok) {
        setIsAuthenticated(true);
        navigate('/mesa');
      } else {
        setError(data.error || 'Credencial inválida');
      }
    } catch (err) {
      setError('Error al conectar con el servidor');
    }
  };

  return (
    <div className="login-page">
      <div className="login-security-banner">
        Elecciones uruguayas <strong>tipo de eleccion</strong> del fecha<a href="#">¿Qué es esto?</a>
      </div>

      <div className="login-container">
        <h2 className="login-title">Ingresa tu credencial</h2>
        <form onSubmit={handleLogin}>
          <label htmlFor="numero" className="login-label">
            Serie de credencial
          </label>
          <input
            id="serie"
            type="text"
            placeholder="serie"
            value={numero}
            onChange={(e) => setNumero(e.target.value)}
            className="login-input"
          />
         <label htmlFor="numero" className="login-label">
            Número de credencial
          </label>
          <input
            id="numero"
            type="text"
            placeholder="numero"
            value={numero}
            onChange={(e) => setNumero(e.target.value)}
            className="login-input"
          />
          <button type="submit" className="login-button">
            Continuar
          </button>
        </form>

        {error && <p className="login-error">{error}</p>}
      </div>
    </div>
  );
}

export default LoginMesa;
