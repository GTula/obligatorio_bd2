import { useContext, useState } from "react";
import { mesaAuthContext } from "../App";
import { useNavigate } from "react-router-dom";
import "./Login.css";

function LoginMesa() {
    const [numero, setNumero] = useState('');
    const [serie, setSerie] = useState('');
    const [error, setError] = useState('');
    const [isAuthenticated, setIsAuthenticated] = useContext(mesaAuthContext);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const fecha = '2025-10-20'; // Esto debería ser dinámico en una app real
            const res = await fetch('http://127.0.0.1:5000/api/login_presidente/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ serie, numero, fecha })
            });

            const data = await res.json();
            console.log('Login response:', data);
            
            if (res.ok) {
                // Guardar información de la mesa
                localStorage.setItem('mesa_id', data.mesa_id);
                localStorage.setItem('fecha_eleccion', fecha);
                localStorage.setItem('id_eleccion', data.id_eleccion);
                console.log('Stored in localStorage:', {
                    mesa_id: data.mesa_id,
                    fecha_eleccion: fecha,
                    id_eleccion: data.id_eleccion
                });
                setIsAuthenticated(true);
                navigate('/mesa');
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
                Elecciones uruguayas <strong>tipo de eleccion</strong> del fecha <a href="#">¿Qué es esto?</a>
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

export default LoginMesa;
