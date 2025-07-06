import React, { useState, useEffect } from 'react';
import Modal from './Modal';
import { adminService } from '../services/adminService';
import { validarCI } from '../services/validations';
import '../styles/EntityManager.css';

const EntityManager = ({ entity, onBack }) => {
  const [action, setAction] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [data, setData] = useState([]);
  const [selectedItem, setSelectedItem] = useState(null);
  const [formData, setFormData] = useState({});
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (action === 'show') {
      fetchData();
    }
  }, [action]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const result = await adminService.fetchData(entity.endpoint);
      setData(result);
    } catch (error) {
      alert(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleActionSelect = (selectedAction) => {
    setAction(selectedAction);
    setShowModal(true);
    
    if (selectedAction === 'create') {
      const initialData = {};
      entity.fields.forEach(field => {
        const validation = entity.validations[field];
        if (validation?.type === 'checkbox') {
          initialData[field] = false;
        } else {
          initialData[field] = '';
        }
      });
      setFormData(initialData);
    }
  };

  const handleInputChange = (field, value) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
  };

  // Función mejorada para detectar campos de cédula
  const isCedulaField = (fieldName) => {
    const lowerField = fieldName.toLowerCase();
    return lowerField === 'ci' || 
           lowerField === 'ci_ciudadano' || 
           lowerField === 'ci_policia' || 
           lowerField === 'id_candidato' ||
           lowerField.startsWith('ci_') ||
           lowerField.endsWith('_ci');
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      // Validar cédulas antes de enviar
      for (const field of entity.fields) {
        if (isCedulaField(field) && formData[field] && !validarCI(formData[field])) {
          throw new Error(`La cédula en el campo ${field} no es válida`);
        }
      }

      // Convert dates in formData before sending to backend
      const processedData = { ...formData };
      entity.fields.forEach(field => {
        const validation = entity.validations[field];
        if (validation?.type === 'date' && processedData[field]) {
          // Ensure date is in yyyy-MM-dd format
          if (typeof processedData[field] === 'string' && processedData[field].includes('GMT')) {
            const date = new Date(processedData[field]);
            if (!isNaN(date.getTime())) {
              processedData[field] = date.toISOString().split('T')[0];
            }
          }
        }
      });

      if (action === 'create') {
        await adminService.createItem(entity, processedData);
        alert('Creado exitosamente');
      } else if (action === 'update') {
        await adminService.updateItem(entity, selectedItem, processedData);
        alert('Actualizado exitosamente');
      } else if (action === 'delete') {
        await adminService.deleteItem(entity, selectedItem);
        alert('Eliminado exitosamente');
      }
      
      setShowModal(false);
      if (action === 'show') {
        fetchData();
      }
    } catch (error) {
      alert(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleForceDelete = async (item) => {
    // Doble confirmación para eliminación forzada
    const confirmacion1 = window.confirm(
      `⚠️ PRIMERA CONFIRMACIÓN\n\n¿Está ABSOLUTAMENTE SEGURO que desea eliminar forzadamente este elemento?\n\nEsta acción eliminará el elemento y TODAS sus dependencias.\n\n¡Esta operación NO se puede deshacer!`
    );
    
    if (!confirmacion1) return;
    
    const confirmacion2 = window.confirm(
      `⚠️ SEGUNDA CONFIRMACIÓN\n\nEsta es su ÚLTIMA oportunidad para cancelar.\n\n¿Confirma la eliminación FORZADA?\n\nSe eliminarán TODOS los datos relacionados.`
    );
    
    if (!confirmacion2) return;

    try {
      setLoading(true);
      const idFields = entity.idFields || [entity.idField];
      const ids = idFields.map(field => {
        if (field === 'ci_ciudadano' && item.ci_ciudadano) {
          return item.ci_ciudadano;
        }
        if (field === 'ci' && item.ci) {
          return item.ci;
        }
        return item[field];
      });
      
      const url = `http://127.0.0.1:5000/api/admin/${entity.singularEndpoint}/forzar/${ids.join('/')}`;
      console.log('Force delete URL:', url);
      
      const response = await fetch(url, {
        method: 'DELETE'
      });
      
      const contentType = response.headers.get('content-type');
      if (!contentType || !contentType.includes('application/json')) {
        const text = await response.text();
        console.error('Response is not JSON:', text);
        throw new Error(`Error del servidor en eliminación forzada`);
      }
      
      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.error || `Error ${response.status}: ${response.statusText}`);
      }
      
      const result = await response.json();
      alert(`✅ ${result.mensaje}`);
      setShowModal(false);
      
      // Recargar datos si estamos en modo mostrar
      if (action === 'show') {
        fetchData();
      }
    } catch (error) {
      console.error('Error en eliminación forzada:', error);
      alert(`❌ Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleItemSelect = (item) => {
    setSelectedItem(item);
    if (action === 'update') {
      // Convert the item data, especially dates, for the form
      const convertedData = { ...item };
      entity.fields.forEach(field => {
        const validation = entity.validations[field];
        if (validation?.type === 'date' && convertedData[field]) {
          // Convert from database format to yyyy-MM-dd
          if (typeof convertedData[field] === 'string' && convertedData[field].includes('GMT')) {
            const date = new Date(convertedData[field]);
            if (!isNaN(date.getTime())) {
              convertedData[field] = date.toISOString().split('T')[0];
            }
          }
        }
      });
      setFormData(convertedData);
    }
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setSelectedItem(null);
    setFormData({});
  };

  const renderInput = (field) => {
    const validation = entity.validations[field];
    let value = formData[field] || '';

    // Handle date formatting for HTML date input
    if (validation?.type === 'date' && value) {
      if (typeof value === 'string' && value.includes('GMT')) {
        // Convert from database format to yyyy-MM-dd
        const date = new Date(value);
        if (!isNaN(date.getTime())) {
          value = date.toISOString().split('T')[0];
        }
      }
    }

    // Usar la función mejorada para detectar campos de cédula
    const isCIField = isCedulaField(field);

    switch (validation?.type) {
      case 'date':
        return (
          <input
            type="date"
            value={value}
            onChange={(e) => handleInputChange(field, e.target.value)}
            required={validation.required}
          />
        );
      case 'number':
        return (
          <input
            type="number"
            value={value}
            onChange={(e) => {
              const newValue = e.target.value;
              handleInputChange(field, newValue);
            }}
            required={validation.required}
            min={isCIField ? 10000000 : undefined}
            max={isCIField ? 99999999 : undefined}
            onBlur={(e) => {
              // Validar cédula cuando el usuario sale del campo
              if (isCIField && e.target.value && !validarCI(e.target.value)) {
                e.target.setCustomValidity('Cédula uruguaya inválida');
                e.target.reportValidity();
              } else {
                e.target.setCustomValidity('');
              }
            }}
          />
        );
      case 'checkbox':
        return (
          <input
            type="checkbox"
            checked={value}
            onChange={(e) => handleInputChange(field, e.target.checked)}
          />
        );
      case 'select':
        return (
          <select
            value={value}
            onChange={(e) => handleInputChange(field, e.target.value)}
            required={validation.required}
          >
            <option value="">Seleccione...</option>
            {validation.options?.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        );
      default:
        return (
          <input
            type="text"
            value={value}
            onChange={(e) => handleInputChange(field, e.target.value)}
            required={validation?.required}
          />
        );
    }
  };

  const renderModalContent = () => {
    switch (action) {
      case 'create':
      case 'update':
        // Verificar si la entidad solo tiene campos de ID de ciudadano y no debería permitir modificación
        const hasOnlyCIFields = entity.fields.every(field => 
          isCedulaField(field) || 
          field.toLowerCase().includes('id')
        );
        
        if (action === 'update' && hasOnlyCIFields && entity.fields.length <= 2) {
          return (
            <div className="info-container">
              <h3>Modificación no disponible</h3>
              <p>Esta entidad solo contiene campos de identificación y no puede ser modificada.</p>
              <div className="modal-buttons">
                <button onClick={closeModal} className="btn-secondary">Cerrar</button>
              </div>
            </div>
          );
        }

        return (
          <div className="form-container">
            <h3>{action === 'create' ? 'Crear' : 'Actualizar'} {entity.name}</h3>
            {entity.fields.map(field => (
              <div key={field} className="form-group">
                <label>{field.replace(/_/g, ' ').toUpperCase()}:</label>
                {renderInput(field)}
              </div>
            ))}
            <div className="modal-buttons">
              <button 
                onClick={handleSubmit} 
                className="btn-primary"
                disabled={loading}
              >
                {loading ? 'Procesando...' : (action === 'create' ? 'Crear' : 'Actualizar')}
              </button>
              <button onClick={closeModal} className="btn-secondary">Cancelar</button>
            </div>
          </div>
        );

      case 'delete':
        return (
          <div className="confirmation-container">
            <h3>Confirmar Eliminación</h3>
            <p>¿Está seguro que desea eliminar este elemento?</p>
            {selectedItem && (
              <div className="item-details">
                {entity.displayFields.map(field => (
                  <p key={field}>
                    <strong>{field.replace(/_/g, ' ').toUpperCase()}:</strong> {selectedItem[field]}
                  </p>
                ))}
              </div>
            )}
            <div className="modal-buttons">
              <button 
                onClick={handleSubmit} 
                className="btn-danger"
                disabled={loading}
              >
                {loading ? 'Eliminando...' : 'Eliminar'}
              </button>
              <button onClick={closeModal} className="btn-secondary">Cancelar</button>
            </div>
          </div>
        );

      case 'force-delete':
        return (
          <div className="confirmation-container">
            <h3 style={{color: '#dc3545'}}>⚠️ ELIMINAR FORZADAMENTE</h3>
            <div style={{
              backgroundColor: '#f8d7da',
              border: '1px solid #f5c6cb',
              padding: '15px',
              borderRadius: '5px',
              marginBottom: '15px'
            }}>
              <p style={{color: '#721c24', fontWeight: 'bold', margin: '0 0 10px 0'}}>
                ⚠️ ADVERTENCIA CRÍTICA
              </p>
              <p style={{color: '#721c24', margin: '0'}}>
                Esta acción eliminará el elemento y TODAS sus dependencias de la base de datos.
                Esta operación NO se puede deshacer y puede afectar múltiples tablas.
              </p>
            </div>
            {selectedItem && (
              <div className="item-details">
                <h4>Elemento a eliminar:</h4>
                {entity.displayFields.map(field => (
                  <p key={field}>
                    <strong>{field.replace(/_/g, ' ').toUpperCase()}:</strong> {selectedItem[field]}
                  </p>
                ))}
              </div>
            )}
            <div className="modal-buttons">
              <button 
                onClick={() => handleForceDelete(selectedItem)} 
                className="btn-force-delete"
                disabled={loading}
              >
                {loading ? 'Eliminando...' : '⚠️ CONFIRMAR ELIMINACIÓN FORZADA'}
              </button>
              <button onClick={closeModal} className="btn-secondary">Cancelar</button>
            </div>
          </div>
        );

      case 'show':
        return (
          <div className="data-container">
            <h3>Datos de {entity.name}</h3>
            {loading ? (
              <p>Cargando...</p>
            ) : (
              <div className="data-table">
                <table>
                  <thead>
                    <tr>
                      {entity.displayFields.map(field => (
                        <th key={field}>{field.replace(/_/g, ' ').toUpperCase()}</th>
                      ))}
                    </tr>
                  </thead>
                                    <tbody>
                    {data.map((item, index) => (
                      <tr key={index}>
                        {entity.displayFields.map(field => (
                          <td key={field}>
                            {typeof item[field] === 'boolean' 
                              ? (item[field] ? 'Sí' : 'No')
                              : item[field]
                            }
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
            <div className="modal-buttons">
              <button onClick={closeModal} className="btn-secondary">Cerrar</button>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  // Verificar si la entidad solo tiene campos de ID de ciudadano para ocultar el botón de modificar
  const hasOnlyCIFields = entity.fields.every(field => 
    isCedulaField(field) || 
    field.toLowerCase().includes('id')
  );
  
  const shouldHideUpdate = hasOnlyCIFields && entity.fields.length <= 2;

  return (
    <div className="entity-manager">
      <div className="header">
        <button onClick={onBack} className="btn-back">← Volver</button>
        <h2>Gestionar {entity.name}</h2>
      </div>

      <div className="actions-grid">
        <div className="action-card create" onClick={() => handleActionSelect('create')}>
          <h3>Crear</h3>
          <p>Agregar nuevo {entity.name.slice(0, -1)}</p>
        </div>

        <div className="action-card show" onClick={() => handleActionSelect('show')}>
          <h3>Mostrar</h3>
          <p>Ver todos los {entity.name.toLowerCase()}</p>
        </div>

        {!shouldHideUpdate && (
          <div className="action-card update" onClick={() => {
            setAction('update');
            fetchData();
          }}>
            <h3>Modificar</h3>
            <p>Actualizar {entity.name.toLowerCase()}</p>
          </div>
        )}

        <div className="action-card delete" onClick={() => {
          setAction('delete');
          fetchData();
        }}>
          <h3>Eliminar</h3>
          <p>Eliminar {entity.name.toLowerCase()}</p>
        </div>

        <div className="action-card force-delete" onClick={() => {
          setAction('force-delete');
          fetchData();
        }}>
          <h3>⚠️ Eliminar Forzado</h3>
          <p>Eliminar con todas las dependencias</p>
        </div>
      </div>

      {(action === 'update' || action === 'delete' || action === 'force-delete') && data.length > 0 && !showModal && (
        <div className="items-list">
          <h3>Seleccione un elemento:</h3>
          {loading ? (
            <p>Cargando...</p>
          ) : (
            <div className="items-grid">
              {data.map((item, index) => (
                <div 
                  key={index} 
                  className="item-card"
                  onClick={() => handleItemSelect(item)}
                >
                  {entity.displayFields.slice(0, 3).map(field => (
                    <p key={field}>
                      <strong>{field.replace(/_/g, ' ').toUpperCase()}:</strong> {
                        typeof item[field] === 'boolean' 
                          ? (item[field] ? 'Sí' : 'No')
                          : item[field]
                      }
                    </p>
                  ))}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {showModal && (
        <Modal onClose={closeModal}>
          {renderModalContent()}
        </Modal>
      )}
    </div>
  );
};

export default EntityManager;

