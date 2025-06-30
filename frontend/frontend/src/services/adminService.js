const API_BASE = 'http://127.0.0.1:5000/api/admin';

export const adminService = {
  async fetchData(endpoint) {
    try {
      console.log(`Fetching data from: ${API_BASE}/${endpoint}`);
      const response = await fetch(`${API_BASE}/${endpoint}`);
      
      // Verificar si la respuesta es HTML (error del servidor)
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        const text = await response.text();
        console.error('Response is not JSON:', text);
        throw new Error(`El servidor devolvió un error. Endpoint: ${endpoint}`);
      }
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || `Error ${response.status}: ${response.statusText}`);
      }
      
      return response.json();
    } catch (error) {
      console.error('Error fetching data:', error);
      if (error.message.includes('Failed to fetch')) {
        throw new Error('No se puede conectar con el servidor. Verifique que esté ejecutándose.');
      }
      throw error;
    }
  },

  async createItem(entity, data) {
    try {
      console.log(`Creating item at: ${API_BASE}/${entity.singularEndpoint}`, data);
      const response = await fetch(`${API_BASE}/${entity.singularEndpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      
      // Verificar si la respuesta es HTML (error del servidor)
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        const text = await response.text();
        console.error('Response is not JSON:', text);
        throw new Error(`Error del servidor al crear ${entity.name}`);
      }
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || `Error ${response.status}: ${response.statusText}`);
      }
      return response.json();
    } catch (error) {
      console.error('Error creating item:', error);
      if (error.message.includes('Failed to fetch')) {
        throw new Error('No se puede conectar con el servidor. Verifique que esté ejecutándose.');
      }
      throw error;
    }
  },

  async updateItem(entity, item, data) {
    try {
      const idFields = entity.idFields || [entity.idField];
      const ids = idFields.map(field => {
        // Manejar casos especiales donde el campo puede tener un nombre diferente en el item
        if (field === 'ci_ciudadano' && item.ci_ciudadano) {
          return item.ci_ciudadano;
        }
        if (field === 'ci' && item.ci) {
          return item.ci;
        }
        return item[field];
      });
      
      const url = `${API_BASE}/${entity.singularEndpoint}/${ids.join('/')}`;
      console.log('Update request details:', {
        entity: entity.name,
        idFields,
        item,
        ids,
        data,
        url
      });
      
      const response = await fetch(url, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      
      // Verificar si la respuesta es HTML (error del servidor)
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        const text = await response.text();
        console.error('Response is not JSON:', text);
        throw new Error(`Error del servidor al actualizar ${entity.name}. URL: ${url}`);
      }
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || `Error ${response.status}: ${response.statusText}`);
      }
      return response.json();
    } catch (error) {
      console.error('Error updating item:', error);
      if (error.message.includes('Failed to fetch')) {
        throw new Error('No se puede conectar con el servidor. Verifique que esté ejecutándose.');
      }
      throw error;
    }
  },

  async deleteItem(entity, item) {
    try {
      const idFields = entity.idFields || [entity.idField];
      const ids = idFields.map(field => {
        // Manejar casos especiales donde el campo puede tener un nombre diferente en el item
        if (field === 'ci_ciudadano' && item.ci_ciudadano) {
          return item.ci_ciudadano;
        }
        if (field === 'ci' && item.ci) {
          return item.ci;
        }
        return item[field];
      });
      
      const url = `${API_BASE}/${entity.singularEndpoint}/${ids.join('/')}`;
      console.log('Delete request details:', {
        entity: entity.name,
        idFields,
        item,
        ids,
        url
      });
      
      const response = await fetch(url, {
        method: 'DELETE'
      });
      
      // Verificar si la respuesta es HTML (error del servidor)
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        const text = await response.text();
        console.error('Response is not JSON:', text);
        throw new Error(`Error del servidor al eliminar ${entity.name}. URL: ${url}`);
      }
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || `Error ${response.status}: ${response.statusText}`);
      }
      return response.json();
    } catch (error) {
      console.error('Error deleting item:', error);
      if (error.message.includes('Failed to fetch')) {
        throw new Error('No se puede conectar con el servidor. Verifique que esté ejecutándose.');
      }
      throw error;
    }
  }
};
