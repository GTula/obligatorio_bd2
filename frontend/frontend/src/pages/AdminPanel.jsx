import React, { useState } from 'react';
import EntityManager from '../components/EntityManager';
import { entities } from '../config/entities';
import '../styles/AdminPanel.css';

const AdminPanel = () => {
  const [selectedEntity, setSelectedEntity] = useState(null);

  const handleEntitySelect = (entity) => {
    setSelectedEntity(entity);
  };

  const handleBack = () => {
    setSelectedEntity(null);
  };

  return (
    <div className="admin-panel">
      {!selectedEntity ? (
        <div className="entities-grid">
          <h1>Panel de Administración</h1>
          <div className="entities-container">
            {entities.map((entity, index) => (
              <div 
                key={index} 
                className="entity-card"
                onClick={() => handleEntitySelect(entity)}
              >
                <h3>{entity.name}</h3>
                <p>Gestionar {entity.name.toLowerCase()}</p>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <EntityManager 
          entity={selectedEntity} 
          onBack={handleBack}
        />
      )}
    </div>
  );
};

export default AdminPanel;
