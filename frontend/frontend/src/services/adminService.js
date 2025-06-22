const API_BASE = 'http://127.0.0.1:5000/api/admin';

export const adminService = {
  async fetchData(endpoint) {
    try {
      const response = await fetch(`${API_BASE}/${endpoint}`);
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Error fetching data');
      }
      return response.json();
    } catch (error) {
      console.error('Error fetching data:', error);
      throw error;
    }
  },

  async createItem(entity, data) {
    try {
      const response = await fetch(`${API_BASE}/${entity.singularEndpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Error creating item');
      }
      return response.json();
    } catch (error) {
      console.error('Error creating item:', error);
      throw error;
    }
  },

  async updateItem(entity, item, data) {
    try {
      const idFields = entity.idFields || [entity.idField];
      const ids = idFields.map(field => item[field]);
      
      console.log('Update request details:', {
        entity: entity.name,
        idFields,
        item,
        ids,
        data,
        url: `${API_BASE}/${entity.singularEndpoint}/${ids.join('/')}`
      });
      
      const response = await fetch(`${API_BASE}/${entity.singularEndpoint}/${ids.join('/')}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Error updating item');
      }
      return response.json();
    } catch (error) {
      console.error('Error updating item:', error);
      throw error;
    }
  },

  async deleteItem(entity, item) {
    try {
      const idFields = entity.idFields || [entity.idField];
      const ids = idFields.map(field => item[field]);
      
      console.log('Delete request details:', {
        entity: entity.name,
        idFields,
        item,
        ids,
        url: `${API_BASE}/${entity.singularEndpoint}/${ids.join('/')}`
      });
      
      const response = await fetch(`${API_BASE}/${entity.singularEndpoint}/${ids.join('/')}`, {
        method: 'DELETE'
      });
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || 'Error deleting item');
      }
      return response.json();
    } catch (error) {
      console.error('Error deleting item:', error);
      throw error;
    }
  }
};
