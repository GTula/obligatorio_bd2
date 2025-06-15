import { useContext, useState } from "react";
import { votanteAuthContext } from "../App";
import { useNavigate } from "react-router-dom";
import "./Login.css";

function LoginVotante() {
    const [numero, setNumero] = useState('');
    const [serie, setSerie] = useState('');
    const [error, setError] = useState('');
    const [isAuthenticated, setIsAuthenticated] = useContext(votanteAuthContext);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
        const res = await fetch('http://127.0.0.1:5000/api/circuito/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ serie, numero, fecha:'2025-10-20' })
        });

        const data = await res.json();
        if (res.ok) {
            setIsAuthenticated(true);
            navigate('/votar');
        } else {
            setError(data.error || 'Credencial inválida');
        }
        } catch (err) {
            console.log(err);
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
            <label htmlFor="serie" className="login-label">
                Serie de credencial
            </label>
            <input
                id="serie"
                type="text"
                placeholder="serie"
                value={serie}
                onChange={(e) => setSerie(e.target.value)}
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

export default LoginVotante;
