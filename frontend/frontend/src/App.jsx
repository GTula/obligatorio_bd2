import { BrowserRouter, Route, Routes, Navigate } from 'react-router-dom';
import { createContext, useState } from 'react';

import LoginMesa from './pages/LoginMesa';
import HomeMesa from './pages/HomeMesa';
import LoginVotante from './pages/LoginVotante';
import PantallaVotacion from './pages/PantallaVotacion';
import Votantes from './pages/VotantesMesa';
import Resultados from './pages/Resultados';
import LoginAdmin from './pages/LoginAdmin';
import AdminPanel from './pages/AdminPanel';


import { MesaProvider } from './context/MesaContext'; // <- este es tu nuevo contexto

export const mesaAuthContext = createContext();
export const votanteAuthContext = createContext();
export const adminAuthContext = createContext();

function App() {
  const [isMesaAuthenticated, setMesaAuthenticated] = useState(false);
  const [isVotanteAuthenticated, setVotanteAuthenticated] = useState(false);
  const [isAdminAuthenticated, setAdminAuthenticated] = useState(false);

  return (
    <adminAuthContext.Provider value={[isAdminAuthenticated, setAdminAuthenticated]}>
      <mesaAuthContext.Provider value={[isMesaAuthenticated, setMesaAuthenticated]}>
        <votanteAuthContext.Provider value={[isVotanteAuthenticated, setVotanteAuthenticated]}>
          <MesaProvider>
            <BrowserRouter>
              <Routes>
                <Route path="/login-mesa" element={<LoginMesa />} />
                <Route path="/mesa" element={
                  isMesaAuthenticated ? <HomeMesa /> : <Navigate to="/login-mesa" />
                } />
                <Route path="/login-votante" element={<LoginVotante />} />
                <Route path="/votar" element={
                  isVotanteAuthenticated ? <PantallaVotacion /> : <Navigate to="/login-votante" />
                } />
                <Route path="/votantes" element={
                  isMesaAuthenticated ? <Votantes /> : <Navigate to="/login-mesa" />
                } />
                <Route path="/resultados" element={
                  isMesaAuthenticated ? <Resultados /> : <Navigate to="/login-mesa" />
                } />
                <Route path="/login-admin" element={<LoginAdmin />} />
                <Route path="/admin" element={
                  isAdminAuthenticated ? <AdminPanel /> : <Navigate to="/login-admin" />
                } />
              </Routes>
            </BrowserRouter>
          </MesaProvider>
        </votanteAuthContext.Provider>
      </mesaAuthContext.Provider>
    </adminAuthContext.Provider>
  );
}

export default App;
