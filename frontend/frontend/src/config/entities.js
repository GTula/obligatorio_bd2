export const entities = [
  // Entidades principales
   {
    name: 'Ciudadanos',
    endpoint: 'ciudadanos',
    singularEndpoint: 'ciudadano',
    idField: 'ci', 
    fields: ['ci', 'nombre', 'apellido', 'fecha_nac'],
    displayFields: ['ci', 'nombre', 'apellido', 'fecha_nac'],
    validations: {
      ci: { type: 'text', required: true },
      nombre: { type: 'text', required: true },
      apellido: { type: 'text', required: true },
      fecha_nac: { type: 'date', required: true }
    }
  },
  { 
    name: 'Departamentos', 
    endpoint: 'departamentos', 
    singularEndpoint: 'departamento',
    fields: ['nombre'],
    idFields: ['id'],
    displayFields: ['id', 'nombre'],
    validations: {
      nombre: { required: true, type: 'text' }
    }
  },
  { 
    name: 'Comisarías', 
    endpoint: 'comisarias', 
    singularEndpoint: 'comisaria',
    fields: ['nombre'],
    idFields: ['id'],
    displayFields: ['id', 'nombre'],
    validations: {
      nombre: { required: true, type: 'text' }
    }
  },
  { 
    name: 'Partidos', 
    endpoint: 'partidos', 
    singularEndpoint: 'partido',
    fields: ['nombre', 'direccion'],
    idFields: ['id'],
    displayFields: ['id', 'nombre', 'direccion'],
    validations: {
      nombre: { required: true, type: 'text' },
      direccion: { required: true, type: 'text' }
    }
  },
  { 
    name: 'Establecimientos', 
    endpoint: 'establecimientos', 
    singularEndpoint: 'establecimiento',
    fields: ['direccion', 'id_zona', 'id_departamento'],
    idFields: ['id'],
    displayFields: ['id', 'direccion', 'id_zona', 'id_departamento'],
    validations: {
      direccion: { required: true, type: 'text' },
      id_zona: { required: true, type: 'number' },
      id_departamento: { required: true, type: 'number' }
    }
  },
  { 
    name: 'Zonas', 
    endpoint: 'zonas', 
    singularEndpoint: 'zona',
    fields: ['nombre', 'id_departamento'],
    idFields: ['id'],
    displayFields: ['id', 'nombre', 'id_departamento'],
    validations: {
      nombre: { required: true, type: 'text' },
      id_departamento: { required: true, type: 'number' }
    }
  },
  { 
    name: 'Candidatos', 
    endpoint: 'candidatos', 
    singularEndpoint: 'candidato',
    fields: ['ci_ciudadano', 'id_partido'],
    idFields: ['ci_ciudadano'],
    displayFields: ['ci_ciudadano', 'id_partido'],
    validations: {
      ci_ciudadano: { required: true, type: 'text' },
      id_partido: { required: true, type: 'number' }
    }
  },
  { 
    name: 'Autoridades', 
    endpoint: 'autoridades', 
    singularEndpoint: 'autoridad',
    fields: ['ci_ciudadano', 'id_partido'],
    idFields: ['ci_ciudadano'],
    displayFields: ['ci_ciudadano', 'id_partido'],
    validations: {
      ci_ciudadano: { required: true, type: 'text' },
      id_partido: { required: true, type: 'number' }
    }
  },
  { 
    name: 'Credenciales', 
    endpoint: 'credenciales', 
    singularEndpoint: 'credencial',
    fields: ['serie', 'numero', 'ci_ciudadano'],
    idFields: ['serie', 'numero'],
    displayFields: ['serie', 'numero', 'ci_ciudadano'],
    validations: {
      serie: { required: true, type: 'text' },
      numero: { required: true, type: 'text' },
      ci_ciudadano: { required: true, type: 'text' }
    }
  },
  { 
    name: 'Elecciones', 
    endpoint: 'elecciones', 
    singularEndpoint: 'eleccion',
    fields: ['fecha', 'id_tipo_eleccion'],
    idFields: ['id'],
    displayFields: ['id', 'fecha', 'id_tipo_eleccion'],
    validations: {
      fecha: { required: true, type: 'date' },
      id_tipo_eleccion: { required: true, type: 'number' }
    }
  },
  { 
    name: 'Agentes Policía', 
    endpoint: 'agentes-policia', 
    singularEndpoint: 'agente-policia',
    fields: ['ci_ciudadano', 'id_comisaria'],
    idFields: ['ci_ciudadano'],
    displayFields: ['ci_ciudadano', 'id_comisaria'],
    validations: {
      ci_ciudadano: { required: true, type: 'text' },
      id_comisaria: { required: true, type: 'number' }
    }
  },
  { 
    name: 'Circuitos', 
    endpoint: 'circuitos', 
    singularEndpoint: 'circuito',
    fields: ['id_eleccion', 'accesible', 'id_establecimiento'],
    idFields: ['id'],
    displayFields: ['id', 'id_eleccion', 'accesible'],
    validations: {
      id_eleccion: { required: true, type: 'number' },
      accesible: { required: false, type: 'checkbox' },
      id_establecimiento: { required: true, type: 'number' }
    }
  },
  { 
    name: 'Mesas', 
    endpoint: 'mesas', 
    singularEndpoint: 'mesa',
    fields: ['num', 'id_circuito', 'id_eleccion'],
    idFields: ['num'],
    displayFields: ['num', 'id_circuito', 'id_eleccion'],
    validations: {
      num: { required: true, type: 'number' },
      id_circuito: { required: true, type: 'number' },
      id_eleccion: { required: true, type: 'number' }
    }
  },
  { 
    name: 'Empleados Públicos', 
    endpoint: 'empleados-publicos', 
    singularEndpoint: 'empleado-publico',
    fields: ['ci_ciudadano', 'num_mesa', 'id_tipo'],
    idFields: ['ci_ciudadano'],
    displayFields: ['ci_ciudadano', 'num_mesa', 'id_tipo'],
    validations: {
      ci_ciudadano: { required: true, type: 'text' },
      num_mesa: { required: true, type: 'number' },
      id_tipo: { required: true, type: 'number' }
    }
  },
  { 
    name: 'Tipos Elección', 
    endpoint: 'tipos-eleccion', 
    singularEndpoint: 'tipo-eleccion',
    fields: ['nombre'],
    idFields: ['id'],
    displayFields: ['id', 'nombre'],
    validations: {
      nombre: { required: true, type: 'text' }
    }
  },
  { 
    name: 'Tipos Empleado', 
    endpoint: 'tipos-empleado', 
    singularEndpoint: 'tipo-empleado',
    fields: ['nombre'],
    idFields: ['id'],
    displayFields: ['id', 'nombre'],
    validations: {
      nombre: { required: true, type: 'text' }
    }
  }
];