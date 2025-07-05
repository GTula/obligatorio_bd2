const API_BASE = 'http://127.0.0.1:5000/api';

export class VotantesService {
    static async getVotantesHabilitados(idCircuito, idEleccion) {
        // Debug temporal
        console.log('🔍 VotantesService.getVotantesHabilitados llamado con:', {
            idCircuito,
            idEleccion,
            tipos: {
                idCircuito: typeof idCircuito,
                idEleccion: typeof idEleccion
            }
        });
        
        // Validar parámetros
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
                    return null; // Votante no encontrado
                }
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error("Error buscando votante:", error);
            throw error;
        }
    }

    static async marcarComoVotado(serieCredencial, numeroCredencial, idCircuito, idEleccion, observado = false) {
        try {
            const response = await fetch(`${API_BASE}/votantes/marcar-voto`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    serie_credencial: serieCredencial,
                    numero_credencial: numeroCredencial,
                    id_circuito: idCircuito,
                    id_eleccion: idEleccion,
                    observado: observado
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || `HTTP error! Status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error("Error marcando voto:", error);
            throw error;
        }
    }

    static async desmarcarVotado(serieCredencial, numeroCredencial, idCircuito, idEleccion) {
        try {
            const response = await fetch(`${API_BASE}/votantes/desmarcar-voto`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    serie_credencial: serieCredencial,
                    numero_credencial: numeroCredencial,
                    id_circuito: idCircuito,
                    id_eleccion: idEleccion
                })
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || `HTTP error! Status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error("Error desmarcando voto:", error);
            throw error;
        }
    }
}
