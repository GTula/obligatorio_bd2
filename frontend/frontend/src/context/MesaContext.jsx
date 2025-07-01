import React, { createContext, useContext, useState } from 'react';

const MesaContext = createContext();

export const useMesa = () => {
    const context = useContext(MesaContext);
    if (!context) {
        throw new Error('useMesa debe usarse dentro de MesaProvider');
    }
    return context;
};

export const MesaProvider = ({ children }) => {
    const [mesaAbierta, setMesaAbierta] = useState(false);
    const [mesaCerrada, setMesaCerrada] = useState(false);
    const [mesaData, setMesaData] = useState({
        numMesa: null,
        idEleccion: null,
        idCircuito: null,
        fecha: null
    });

    const abrirMesa = () => {
        setMesaAbierta(true);
        setMesaCerrada(false);
    };

    const cerrarMesa = (data) => {
        console.log('Cerrando mesa con datos:', data);
        setMesaData(data);
        setMesaAbierta(false);
        setMesaCerrada(true);
    };

    const reiniciarMesa = () => {
        setMesaAbierta(false);
        setMesaCerrada(false);
        setMesaData({
            numMesa: null,
            idEleccion: null,
            idCircuito: null,
            fecha: null
        });
    };

    // Lógica para determinar qué puede ver el usuario
    const puedeVerVotantes = mesaAbierta;
    const puedeVerResultados = mesaCerrada;

    return (
        <MesaContext.Provider value={{
            mesaAbierta,
            mesaCerrada,
            mesaData,
            abrirMesa,
            cerrarMesa,
            reiniciarMesa,
            puedeVerVotantes,
            puedeVerResultados
        }}>
            {children}
        </MesaContext.Provider>
    );
};
