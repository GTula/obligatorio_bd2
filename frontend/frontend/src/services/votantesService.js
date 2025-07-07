const API_BASE = 'http://127.0.0.1:5000/api';

export class VotantesService {
    // Método existente modificado para obtener votantes de un circuito específico
    static async getVotantesHabilitados(idCircuito, idEleccion) {
        console.log('🔍 VotantesService.getVotantesHabilitados llamado con:', {
            idCircuito,
            idEleccion,
            tipos: {
                idCircuito: typeof idCircuito,
                idEleccion: typeof idEleccion
            }
        });
        
        if (!idCircuito || !idEleccion || isNaN(idCircuito) || isNaN(idEleccion)) {
            throw new Error(`Parámetros inválidos: idCircuito=${idCircuito}, idEleccion=${idEleccion}`);
        }
        
        try {
            const url = `${API_BASE}/votantes/circuito/${idCircuito}/eleccion/${idEleccion}`;
            console.log('🔍 Haciendo request a:', url);
            
            const response = await fetch(url);

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error("Error obteniendo votantes:", error);
            throw error;
        }
    }

    // NUEVO: Obtener TODOS los votantes de una elección
    static async getTodosLosVotantes(idEleccion) {
        console.log('🔍 VotantesService.getTodosLosVotantes llamado con:', {
            idEleccion,
            tipo: typeof idEleccion
        });
        
        if (!idEleccion || isNaN(idEleccion)) {
            throw new Error(`Parámetro inválido: idEleccion=${idEleccion}`);
        }
        
        try {
            const url = `${API_BASE}/votantes/eleccion/${idEleccion}`;
            console.log('🔍 Haciendo request a:', url);
            
            const response = await fetch(url);

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error("Error obteniendo todos los votantes:", error);
            throw error;
        }
    }
    
    // Método existente para buscar votante específico por circuito
    static async buscarVotante(serie, numero, idCircuito, idEleccion) {
        try {
            const params = new URLSearchParams({
                serie,
                numero,
                id_circuito: idCircuito,
                id_eleccion: idEleccion
            });

            const response = await fetch(`${API_BASE}/votantes/buscar?${params}`);

            if (!response.ok) {
                if (response.status === 404) {
                    return null;
                }
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error("Error buscando votante:", error);
            throw error;
        }
    }

    // NUEVO: Buscar votante globalmente (en toda la elección)
    static async buscarVotanteGlobal(serie, numero, idEleccion) {
        try {
            const params = new URLSearchParams({
                serie,
                numero,
                id_eleccion: idEleccion
            });

            const response = await fetch(`${API_BASE}/votantes/buscar-global?${params}`);

            if (!response.ok) {
                if (response.status === 404) {
                    return null;
                }
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error("Error buscando votante globalmente:", error);
            throw error;
        }
    }

    static async marcarComoVotado(serie, numero, idCircuito, idEleccion, observado = false) {
        try {
            const response = await fetch(`${API_BASE}/votantes/marcar-votado`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    serie_credencial: serie,
                    numero_credencial: numero,
                    id_circuito: idCircuito,
                    id_eleccion: idEleccion,
                    observado: observado
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! Status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error("Error marcando como votado:", error);
            throw error;
        }
    }

    static async desmarcarVotado(serie, numero, idCircuito, idEleccion) {
        try {
            const response = await fetch(`${API_BASE}/votantes/desmarcar-votado`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    serie_credencial: serie,
                    numero_credencial: numero,
                    id_circuito: idCircuito,
                    id_eleccion: idEleccion
                })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! Status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error("Error desmarcando votado:", error);
            throw error;
        }
    }
}
