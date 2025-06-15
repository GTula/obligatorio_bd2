import { createContext, useContext, useState } from 'react';

const MesaContext = createContext();

export const useMesa = () => useContext(MesaContext);

export function MesaProvider({ children }) {
  const [estadoMesa, setEstadoMesa] = useState('cerrada'); // 'abierta' o 'cerrada'

  return (
    <MesaContext.Provider value={{ estadoMesa, setEstadoMesa }}>
      {children}
    </MesaContext.Provider>
  );
}
