import { useContext, useState } from "react";
import { mesaAuthContext } from "../App";
import { useNavigate } from "react-router-dom";
import escudo from "../assets/escudo_uruguay.png";
import "./Login.css";

function LoginMesa() {
    const [numero, setNumero] = useState('');
    const [serie, setSerie] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [isAuthenticated, setIsAuthenticated] = useContext(mesaAuthContext);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        
        try {
            // Obtener fecha actual en formato YYYY-MM-DD
            const fechaActual = new Date().toISOString().split('T')[0];
            
            const res = await fetch('http://127.0.0.1:5000/api/login_presidente/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ serie, numero, fecha: fechaActual })
            });

            const data = await res.json();
            console.log('Login response:', data);
            
            if (res.ok) {
                // Guardar información de la mesa
                localStorage.setItem('mesa_id', data.mesa_id);
                localStorage.setItem('fecha_eleccion', fechaActual);
                localStorage.setItem('id_eleccion', data.id_eleccion);
                console.log('Stored in localStorage:', {
                    mesa_id: data.mesa_id,
                    fecha_eleccion: fechaActual,
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
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-page">
            {/* Header con información de la elección */}
            <div className="login-header">
                <div className="election-info">
                    <div className="election-badge">
                        <span className="election-type">ELECCIÓN GENERAL</span>
                        <span className="election-date">
                            {new Date().toLocaleDateString('es-UY', {
                                weekday: 'long',
                                year: 'numeric',
                                month: 'long',
                                day: 'numeric'
                            })}
                        </span>
                    </div>
                </div>
            </div>

            {/* Contenedor principal */}
            <div className="login-main">
                <div className="login-container mesa-login">
                    {/* Logo y título */}
                    <div className="login-logo">
                        <img src={escudo} alt="Escudo de Uruguay" className="escudo-image" />
                        <div className="login-title-section">
                            <h1 className="login-main-title">CORTE ELECTORAL</h1>
                            <p className="login-subtitle">República Oriental del Uruguay</p>
                            <div className="login-divider"></div>
                            <h2 className="login-form-title">Acceso Mesa Electoral</h2>
                            <p className="login-description">
                                Ingrese su credencial de presidente de mesa
                            </p>
                        </div>
                    </div>

                    {/* Formulario */}
                    <form onSubmit={handleLogin} className="login-form">
                        <div className="form-group">
                            <label htmlFor="serie" className="form-label">
                                <span className="label-icon">📋</span>
                                Serie de Credencial
                            </label>
                            <input
                                id="serie"
                                type="text"
                                placeholder="Ej: A"
                                value={serie}
                                onChange={(e) => setSerie(e.target.value.toUpperCase())}
                                className="form-input"
                                maxLength="5"
                                required
                                disabled={loading}
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="numero" className="form-label">
                                <span className="label-icon">🔢</span>
                                Número de Credencial
                            </label>
                            <input
                                id="numero"
                                type="text"
                                placeholder="Ej: 1001"
                                value={numero}
                                onChange={(e) => setNumero(e.target.value)}
                                className="form-input"
                                maxLength="10"
                                required
                                disabled={loading}
                            />
                        </div>

                        {error && (
                            <div className="error-message">
                                <span className="error-icon">⚠️</span>
                                {error}
                            </div>
                        )}

                        <button 
                            type="submit" 
                            className={`login-button mesa-button ${loading ? 'loading' : ''}`}
                            disabled={loading || !serie || !numero}
                        >
                            {loading ? (
                                <>
                                    <span className="loading-spinner"></span>
                                    Verificando...
                                </>
                            ) : (
                                <>
                                    <span className="button-icon">🗳️</span>
                                    Acceder a Mesa
                                </>
                            )}
                        </button>
                    </form>

                    {/* Footer del formulario */}
                    <div className="login-footer">
                        <div className="access-links">
                            <a href="/login-admin" className="access-link admin-link">
                                <span className="link-icon">⚙️</span>
                                Acceso Administrador
                            </a>
                        </div>
                    </div>
                </div>
            </div>

            {/* Footer con información adicional */}
            <div className="login-bottom">
                <div className="security-info">
                    <span className="security-icon">🔒</span>
                    <span>Conexión segura - Todos los datos están protegidos</span>
                </div>
            </div>
        </div>
    );
}

export default LoginMesa;
