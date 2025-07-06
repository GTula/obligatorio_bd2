import { useContext, useState } from "react";
import { adminAuthContext } from "../App";
import { useNavigate } from "react-router-dom";
import escudo from "../assets/escudo_uruguay.png";
import "./Login.css";

function LoginAdmin() {
    const [usuario, setUsuario] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [isAuthenticated, setIsAuthenticated] = useContext(adminAuthContext);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        
        try {
            const res = await fetch('http://127.0.0.1:5000/api/login_admin/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ usuario, password })
            });

            const data = await res.json();
            
            if (res.ok) {
                setIsAuthenticated(true);
                navigate('/admin');
            } else {
                setError(data.error || 'Credenciales inválidas');
            }
        } catch (err) {
            console.log(err);
            setError('Error al conectar con el servidor');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="login-page admin-page">
            {/* Header con información de la elección */}
            <div className="login-header admin-header">
                <div className="election-info">
                    <div className="election-badge admin-badge">
                        <span className="election-type">PANEL DE ADMINISTRACIÓN</span>
                        <span className="election-date">Sistema Electoral</span>
                    </div>
                </div>
            </div>

            {/* Contenedor principal */}
            <div className="login-main">
                <div className="login-container admin-login">
                    {/* Logo y título */}
                    <div className="login-logo">
                        <img src={escudo} alt="Escudo de Uruguay" className="escudo-image" />
                        <div className="login-title-section">
                            <h1 className="login-main-title">CORTE ELECTORAL</h1>
                            <p className="login-subtitle">República Oriental del Uruguay</p>
                            <div className="login-divider admin-divider"></div>
                            <h2 className="login-form-title">Panel de Administración</h2>
                            <p className="login-description">
                                Acceso restringido para administradores del sistema
                            </p>
                        </div>
                    </div>

                    {/* Formulario */}
                    <form onSubmit={handleLogin} className="login-form">
                        <div className="form-group">
                            <label htmlFor="usuario" className="form-label">
                                <span className="label-icon">👤</span>
                                Usuario
                            </label>
                            <input
                                id="usuario"
                                type="text"
                                placeholder="Nombre de usuario"
                                value={usuario}
                                onChange={(e) => setUsuario(e.target.value)}
                                className="form-input"
                                required
                                disabled={loading}
                                autoComplete="username"
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="password" className="form-label">
                                <span className="label-icon">🔐</span>
                                Contraseña
                            </label>
                            <div className="password-input-container">
                                <input
                                    id="password"
                                    type={showPassword ? "text" : "password"}
                                    placeholder="Contraseña"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="form-input password-input"
                                    required
                                    disabled={loading}
                                    autoComplete="current-password"
                                />
                                <button
                                    type="button"
                                    className="password-toggle"
                                    onClick={() => setShowPassword(!showPassword)}
                                    disabled={loading}
                                >
                                    {showPassword ? '👁️' : '👁️‍🗨️'}
                                </button>
                            </div>
                        </div>

                        {error && (
                            <div className="error-message admin-error">
                                <span className="error-icon">🚫</span>
                                {error}
                            </div>
                        )}

                        <button 
                            type="submit" 
                            className={`login-button admin-button ${loading ? 'loading' : ''}`}
                            disabled={loading || !usuario || !password}
                        >
                            {loading ? (
                                <>
                                    <span className="loading-spinner"></span>
                                    Verificando...
                                </>
                            ) : (
                                <>
                                    <span className="button-icon">⚙️</span>
                                    Acceder al Panel
                                </>
                            )}
                        </button>
                    </form>

                    {/* Información de seguridad */}
                    <div className="admin-security-notice">
                        <div className="security-warning">
                            <span className="warning-icon">⚠️</span>
                            <div className="warning-text">
                                <strong>Acceso Restringido</strong>
                                <p>Este panel está destinado únicamente para administradores autorizados del sistema electoral.</p>
                            </div>
                        </div>
                    </div>

                    {/* Footer del formulario */}
                    <div className="login-footer">
                        <div className="access-links">
                            <a href="/login-mesa" className="access-link mesa-link">
                                <span className="link-icon">🗳️</span>
                                Acceso Mesa Electoral
                            </a>
                        </div>
                    </div>
                </div>
            </div>

            {/* Footer con información adicional */}
            <div className="login-bottom admin-bottom">
                <div className="security-info">
                    <span className="security-icon">🔒</span>
                    <span>Conexión segura - Todas las acciones son registradas</span>
                </div>
            </div>
        </div>
    );
}

export default LoginAdmin;
