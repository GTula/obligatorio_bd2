const API_BASE = 'http://127.0.0.1:5000/api';

export class ResultadosService {
    // Método existente para votos CON observados
    static async getVotosConObservados(numMesa, idEleccion, fecha) {
        try {
            const response = await fetch(
                `${API_BASE}/votos/${numMesa}/votos_normales/${idEleccion}?fecha=${fecha}`
            );

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error("Error obteniendo votos con observados:", error);
            throw error;
        }
    }

    // NUEVO método para votos SOLO normales (sin observados)
    static async getVotosSoloNormales(numMesa, idEleccion, fecha) {
        try {
            const response = await fetch(
                `${API_BASE}/votos-normales/${numMesa}/votos_normales/${idEleccion}?fecha=${fecha}`
            );

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error("Error obteniendo votos solo normales:", error);
            throw error;
        }
    }

    static async getTipoEleccion(idEleccion) {
        try {
            const response = await fetch(`${API_BASE}/admin/elecciones`);
            
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const elecciones = await response.json();
            const eleccion = elecciones.find(e => e.id === idEleccion);
            
            return eleccion ? eleccion.id_tipo_eleccion : null;
        } catch (error) {
            console.error("Error obteniendo tipo de elección:", error);
            throw error;
        }
    }
}
