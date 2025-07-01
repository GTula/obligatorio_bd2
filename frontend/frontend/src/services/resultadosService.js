const API_BASE = 'http://127.0.0.1:5000/api';

export class ResultadosService {
    static async getVotosNormales(numMesa, idEleccion, fecha) {
        try {
            const response = await fetch(
                `${API_BASE}/mesa/${numMesa}/votos_normales/${idEleccion}?fecha=${fecha}`
            );

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error("Error obteniendo votos normales:", error);
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
