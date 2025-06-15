// MesaContext.jsx
import React, { createContext, useContext, useState } from 'react';

const MesaContext = createContext();

export function MesaProvider({ children }) {
  const [mesaAbierta, setMesaAbierta] = useState(false);
  const [mesaCerrada, setMesaCerrada] = useState(false);

  const abrirMesa = () => {
    setMesaAbierta(true);
    setMesaCerrada(false);
  };

  const cerrarMesa = () => {
    setMesaAbierta(false);
    setMesaCerrada(true);
  };

  const puedeVerVotantes = mesaAbierta;
  const puedeVerResultados = mesaCerrada;

  return (
    <MesaContext.Provider
      value={{
        mesaAbierta,
        mesaCerrada,
        abrirMesa,
        cerrarMesa,
        puedeVerVotantes,
        puedeVerResultados,
      }}
    >
      {children}
    </MesaContext.Provider>
  );
}

export function useMesa() {
  return useContext(MesaContext);
}
