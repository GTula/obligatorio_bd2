import { createContext, useState } from 'react';
import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import MenuVotante from './pages/MenuVotante';
import Mesa from './pages/Mesa';

export const UsuarioContext = createContext();

function App() {
  const [usuario, setUsuario] = useState(null);

  return (
    <UsuarioContext.Provider value={[usuario, setUsuario]}>
      <BrowserRouter>
        <Routes>
          <Route
            path="/votante"
            element={usuario?.rol === "votante"
              ? <MenuVotante usuario={usuario} />
              : <Navigate to="/login" />}
          />

          <Route
            path="/mesa"
            element={usuario?.rol === "presidente"
              ? <Mesa usuario={usuario} />
              : <Navigate to="/login" />}
          />

          <Route
            path="/login"
            element={<Login setUsuario={setUsuario} />}
          />

          <Route
            path="/"
            element={<Navigate to="/login" />}
          />
        </Routes>
      </BrowserRouter>
    </UsuarioContext.Provider>
  );
}

export default App;
