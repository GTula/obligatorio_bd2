import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom';
import { createContext, useState } from 'react';

import LoginMesa from './pages/LoginMesa';
import HomeMesa from './pages/HomeMesa';
import LoginVotante from './pages/LoginVotante';
import PantallaVotacion from './pages/PantallaVotacion';
import Login from './pages/Login';
import VotantesMesa from './pages/VotantesMesa';
import Resultados from './pages/Resultados';

import { MesaProvider } from './context/MesaContext'; // <- este es tu nuevo contexto

export const mesaAuthContext = createContext();
export const votanteAuthContext = createContext();

function App() {
  const [isMesaAuthenticated, setMesaAuthenticated] = useState(false);
  const [isVotanteAuthenticated, setVotanteAuthenticated] = useState(false);

  return (
    <mesaAuthContext.Provider value={[isMesaAuthenticated, setMesaAuthenticated]}>
      <votanteAuthContext.Provider value={[isVotanteAuthenticated, setVotanteAuthenticated]}>
        <MesaProvider>
          <BrowserRouter>
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/login-mesa" element={<LoginMesa />} />
              <Route path="/mesa" element={
                isMesaAuthenticated ? <HomeMesa /> : <Navigate to="/login-mesa" />
              } />
              <Route path="/login-votante" element={<LoginVotante />} />
              <Route path="/votar" element={
                isVotanteAuthenticated ? <PantallaVotacion /> : <Navigate to="/login-votante" />
              } />
              <Route path="/votantes" element={
                isMesaAuthenticated ? <VotantesMesa /> : <Navigate to="/login-mesa" />
              } />
              <Route path="/resultados" element={
                isMesaAuthenticated ? <Resultados /> : <Navigate to="/login-mesa" />
              } />
            </Routes>
          </BrowserRouter>
        </MesaProvider>
      </votanteAuthContext.Provider>
    </mesaAuthContext.Provider>
  );
}

export default App;
