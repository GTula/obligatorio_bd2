export class BackendCallerActividad {
    static #API_URL = 'http://127.0.0.1:5000/api';

    static async getAllActividades() {
        try {
            const response = await fetch(this.#API_URL, { method: "GET" });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error("Error al obtener todas las clases:", error);
        }
    }

    static async deleteActividadById(actividadId) {
        try {
            const response = await fetch(`${this.#API_URL}/${actividadId}`, { method: "DELETE" });
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            return { success: true };
        } catch (error) {
            console.error("Error al eliminar la actividad:", error);
            return { success: false };
        }
    }

    static async getActividadById(actividadId) {
        try {
            const response = await fetch(`${this.#API_URL}/${actividadId}`, { method: "GET" });
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
    
            const data = await response.json();
            return data; 
        } catch (error) {
            console.error("Error al recoger los detalles de la actividad:", error);
            return null;
        }
    }
    

    static async addActividad(obj) {
        try {
            const response = await fetch(this.#API_URL,
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify(obj)
                });

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            return data;
        } catch (error) {
            console.error("Error al ingresar actividad:", error);
        }
    }

    static async putActividadById(actividadId, obj) {
        try {
            const response = await fetch(`${this.#API_URL}/${actividadId}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(obj),
            });
    
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
    
            const data = await response.json();
            return data;
        } catch (error) {
            console.error("Error al actualizar la clase:", error);
            return null; 
        }
    }
}

export default BackendCallerActividad;