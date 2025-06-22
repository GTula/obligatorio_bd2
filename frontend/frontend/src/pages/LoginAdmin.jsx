import { useContext, useState } from "react";
import { adminAuthContext } from "../App";
import { useNavigate } from "react-router-dom";
import "./Login.css";

function LoginAdmin() {
    const [usuario, setUsuario] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isAuthenticated, setIsAuthenticated] = useContext(adminAuthContext);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const res = await fetch('http://localhost:5000/api/login_admin/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ usuario, password })
            });

            const data = await res.json();
            console.log('Login response:', data);
            
            if (res.ok) {
                setIsAuthenticated(true);
                navigate('/admin');
            } else {
                setError(data.error || 'datos inválidos');
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
                <h2 className="login-title">Ingresa tu usuario y contraseña</h2>
                <form onSubmit={handleLogin}>
                    <label htmlFor="usuario" className="login-label">
                        Usuario
                    </label>
                    <input
                        id="usuario"
                        type="text"
                        placeholder="usuario"
                        value={usuario}
                        onChange={(e) => setUsuario(e.target.value)}
                        className="login-input"
                    />
                    <label htmlFor="contraseña" className="login-label">
                        Contraseña
                    </label>
                    <input
                        id="password"
                        type="text"
                        placeholder="contraseña"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
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

export default LoginAdmin;
