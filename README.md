# Sistema de Votación Electrónica - Obligatorio BD2

## Descripción del Proyecto

Sistema integral de votación electrónica desarrollado para el curso de Bases de Datos 2. El sistema simula el proceso electoral uruguayo con funcionalidades completas para administración de mesas, votación y gestión de resultados.

## Características Principales

- **Sistema de Mesa Electoral**: Gestión completa del proceso de votación
- **Tótem de Votación**: Interfaz para votantes con modo normal y observado
- **Panel de Administración**: CRUD completo para todas las entidades del sistema
- **Gestión de Votantes**: Control de habilitados, votantes y estadísticas en tiempo real
- **Sistema de Resultados**: Visualización de escrutinio por mesa
- **Autenticación Multi-rol**: Presidente de mesa, votantes y administradores

## Tecnologías Utilizadas

### Backend
- **Python** con Flask
- **MySQL** como base de datos
- **Flask-CORS** para comunicación con frontend
- **bcrypt** para encriptación de contraseñas
- **mysql-connector-python** para conexión a BD

### Frontend
- **React** con Create React App
- **React Router** para navegación
- **Context API** para manejo de estado
- **CSS3** con diseño responsive
- **Fetch API** para comunicación con backend

### Infraestructura
- **Docker & Docker Compose** para containerización
- **Nginx** como servidor web de producción

## Estructura del Proyecto

```
obligatorio_bd2/
├── backend/                          # Aplicación Flask (API)
│   ├── routes/                       # Endpoints de la API
│   │   ├── admin/                    # Rutas de administración
│   │   │   ├── Personas/             # Gestión de personas
│   │   │   │   ├── Ciudadano.py
│   │   │   │   ├── Candidato.py
│   │   │   │   ├── Autoridad.py
│   │   │   │   ├── EmpleadoPublico.py
│   │   │   │   ├── Credencial.py
│   │   │   │   ├── AgentePolicia.py
│   │   │   │   └── TipoEmpleado.py
│   │   │   ├── Lugares/              # Gestión de ubicaciones
│   │   │   │   ├── Departamento.py
│   │   │   │   ├── Zona.py
│   │   │   │   ├── Establecimiento.py
│   │   │   │   ├── Comisaria.py
│   │   │   │   └── Circuito.py
│   │   │   ├── Grupos/               # Gestión de agrupaciones
│   │   │   │   ├── Mesa.py
│   │   │   │   └── Partido.py
│   │   │   ├── Eleccion/             # Gestión electoral
│   │   │   │   ├── Eleccion.py
│   │   │   │   ├── TipoEleccion.py
│   │   │   │   ├── Papeleta.py
│   │   │   │   ├── PapeletaPlebiscito.py
│   │   │   │   └── Lista.py
│   │   │   ├── Relaciones/           # Relaciones entre entidades
│   │   │   │   ├── Asignado.py
│   │   │   │   ├── VotaEn.py
│   │   │   │   ├── CandidatoXLista.py
│   │   │   │   └── AgenteEstablecimiento.py
│   │   │   ├── loginAdmin.py         # Autenticación admin
│   │   │   └── admin.py              # Blueprint principal admin
│   │   ├── ciudadanos.py             # Gestión de ciudadanos
│   │   ├── circuito.py               # Gestión de circuitos
│   │   ├── mesa.py                   # Gestión de mesas
│   │   ├── empleados.py              # Login presidente de mesa
│   │   ├── eleccion.py               # Gestión de elecciones
│   │   ├── papeletas.py              # Gestión de papeletas
│   │   ├── votantes.py               # Gestión de votantes
│   │   └── votos.py                  # Gestión de votos
│   ├── db.py                         # Configuración de base de datos
│   ├── app.py                        # Aplicación principal Flask
│   ├── crearAdmin.py                 # Script para crear administradores
│   └── requirements.txt              # Dependencias Python
├── frontend/                         # Aplicación React
│   ├── public/                       # Archivos públicos
│   │   ├── index.html
│   │   └── favicon.ico
│   ├── src/                          # Código fuente React
│   │   ├── components/               # Componentes reutilizables
│   │   │   ├── EntityManager.jsx     # Gestor de entidades CRUD
│   │   │   └── Modal.jsx             # Componente modal
│   │   ├── pages/                    # Páginas principales
│   │   │   ├── LoginMesa.jsx         # Login presidente de mesa
│   │   │   ├── HomeMesa.jsx          # Dashboard de mesa
│   │   │   ├── VotantesMesa.jsx      # Gestión de votantes
│   │   │   ├── Resultados.jsx        # Visualización de resultados
│   │   │   ├── LoginVotante.jsx      # Login de votantes
│   │   │   ├── PantallaVotacion.jsx  # Tótem de votación
│   │   │   ├── PantallaObservado.jsx # Tótem modo observado
│   │   │   ├── LoginAdmin.jsx        # Login administrador
│   │   │   └── AdminPanel.jsx        # Panel de administración
│   │   ├── context/                  # Context API
│   │   │   └── MesaContext.jsx       # Estado global de mesa
│   │   ├── services/                 # Servicios de API
│   │   │   ├── adminService.js       # Servicios admin
│   │   │   ├── resultadosService.js  # Servicios resultados
│   │   │   ├── votantesService.js    # Servicios votantes
│   │   │   └── validations.js        # Validaciones
│   │   ├── config/                   # Configuraciones
│   │   │   └── entities.js           # Configuración entidades
│   │   ├── styles/                   # Estilos CSS
│   │   │   ├── AdminPanel.css
│   │   │   ├── EntityManager.css
│   │   │   └── PantallaVotacion.css
│   │   ├── utils/                    # Utilidades
│   │   │   └── dateUtils.js          # Utilidades de fecha
│   │   ├── assets/                   # Recursos estáticos
│   │   │   └── escudo_uruguay.png
│   │   ├── App.jsx                   # Componente principal
│   │   └── index.js                  # Punto de entrada
│   ├── package.json                  # Dependencias Node.js
│   └── README.md                     # Documentación React
├── bd/                               # Base de datos
│   ├── Tables.sql                    # Definición de tablas
│   └── Inserts.sql                   # Datos de prueba
├── docker-compose.yml                # Configuración Docker
├── Dockerfile.frontend               # Imagen Docker frontend
├── Dockerfile.backend                # Imagen Docker backend
└── README.md                         # Este archivo
```

## Instalación y Configuración

### Prerrequisitos

- **Git** para clonar el repositorio
- **Docker** y **Docker Compose** instalados
- **MySQL 8.0+** (si se ejecuta sin Docker)
- **Node.js 16+** y **npm** (si se ejecuta sin Docker)
- **Python 3.8+** y **pip** (si se ejecuta sin Docker)

### Instalación con Docker 

1. **Clonar el repositorio**
git clone https://github.com/GTula/obligatorio_bd2.git
cd obligatorio_bd2

2. **Levantar los servicios con Docker Compose**
docker-compose up --build

3. **Acceder a las aplicaciones**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- MySQL: localhost:3306


## Configuración de Base de Datos

### Estructura Principal

El sistema utiliza las siguientes tablas principales:

- **ciudadano**: Información básica de ciudadanos
- **credencial**: Credenciales cívicas para votación
- **eleccion**: Información de elecciones
- **circuito**: Circuitos electorales
- **mesa**: Mesas de votación
- **voto**: Registros de votos emitidos
- **papeleta**: Papeletas de votación
- **lista**: Listas de candidatos
- etc...

### Datos de Prueba

El archivo `bd/Inserts.sql` incluye datos de prueba para:

- Ciudadanos con cédulas válidas
- Credenciales de prueba (Serie A, Número 1001)
- Elecciones configuradas para fecha actual
- Mesas y circuitos de prueba
- Empleados públicos (presidentes de mesa)
- etc...

## Uso del Sistema

### 1. Acceso como Presidente de Mesa

1. Ir a http://localhost:3000/login-mesa
2. Usar credencial de prueba:
   - Serie: B
   - Número: 1002
3. Acceder al dashboard de mesa
4. Abrir mesa para habilitar votación
5. Gestionar votantes y consultar resultados

### 2. Acceso como Administrador

1. Ir a http://localhost:3000/login-admin
2. Usar credenciales creadas con `crearAdmin.py`
3. Acceder al panel de administración
4. Gestionar todas las entidades del sistema

### 3. Proceso de Votación

1. Desde la mesa, abrir tótem de votación
2. El votante ingresa su credencial
3. Sistema valida habilitación
4. Votante selecciona opciones
5. Voto se registra en la base de datos

## API Endpoints

### Autenticación
- `POST /api/login_presidente/` - Login presidente de mesa
- `POST /api/login_admin/` - Login administrador

### Gestión de Mesa
- `GET /api/circuito/por-mesa` - Información de circuito
- `GET /api/votantes/circuito/{id}/eleccion/{id}` - Votantes habilitados
- `POST /api/votantes/marcar-voto` - Marcar votante como votado
- `GET /api/mesa/{num}/votos_normales/{id_eleccion}` - Resultados de votación

### Administración
- `GET /api/admin/{entidad}` - Listar entidades
- `POST /api/admin/{entidad}` - Crear entidad
- `PUT /api/admin/{entidad}/{id}` - Actualizar entidad
- `DELETE /api/admin/{entidad}/{id}` - Eliminar entidad

## Funcionalidades Principales

### Sistema de Mesa Electoral
- Dashboard con estadísticas en tiempo real
- Control de apertura/cierre de mesa
- Gestión de votantes habilitados
- Visualización de resultados

### Tótem de Votación
- Validación de credenciales
- Interfaz intuitiva para votación
- Modo normal y observado
- Registro seguro de votos

### Panel de Administración
- CRUD completo para todas las entidades
- Validación de datos
- Gestión de relaciones entre entidades
- Interfaz responsive

### Gestión de Votantes
- Lista de habilitados por circuito
- Búsqueda por credencial
- Marcado de votantes
- Estadísticas en tiempo real

## Seguridad

- Validación de cédulas uruguayas
- Encriptación de contraseñas con bcrypt
- Validación de datos en frontend y backend
- Control de acceso por roles
- Prevención de doble votación

## Testing y Datos de Prueba

### Credenciales de Prueba

**Presidente de Mesa:**
- Serie: B, Número: 1002

**Administrador:**
- Crear con `python crearAdmin.py`

### Escenarios de Prueba

1. **Flujo completo de votación**
2. **Gestión de mesa electoral**
3. **Administración de entidades**
4. **Consulta de resultados**

## Troubleshooting

### Problemas Comunes

1. **Error de conexión a BD**
   - Verificar que MySQL esté ejecutándose
   - Revisar credenciales en `db.py`

2. **Frontend no carga**
   - Verificar que el backend esté en puerto 5000
   - Revisar CORS en Flask

3. **Docker no inicia**
   - Verificar que los puertos 3000, 5000 y 3306 estén libres
   - Ejecutar `docker-compose down` y volver a intentar

### Logs y Debugging

# Ver logs de Docker
docker-compose logs -f

# Logs específicos
docker-compose logs backend
docker-compose logs frontend
docker-compose logs mysql

## Contribución y Desarrollo

### Estructura de Desarrollo

- **Backend**: Arquitectura modular con blueprints de Flask
- **Frontend**: Componentes React con hooks y context
- **Base de Datos**: Diseño normalizado con integridad referencial

## Arquitectura del Sistema

### Patrón de Diseño

El sistema implementa una arquitectura de **3 capas**:

1. **Capa de Presentación** (Frontend React)
   - Componentes reutilizables
   - Gestión de estado con Context API
   - Routing con React Router
   - Validaciones del lado cliente

2. **Capa de Lógica de Negocio** (Backend Flask)
   - API RESTful
   - Validaciones de negocio
   - Autenticación y autorización
   - Manejo de errores

3. **Capa de Datos** (MySQL)
   - Modelo relacional normalizado

### Flujo de Datos

Frontend (React) ←→ API REST (Flask) ←→ Base de Datos (MySQL)


## Conclusión

Este sistema de votación electrónica implementa las mejores prácticas de desarrollo web, con una arquitectura escalable y mantenible. El código está documentado y estructurado para facilitar su comprensión y extensión.

La implementación cumple con los requerimientos académicos del curso de Bases de Datos 2, demostrando:

- Diseño de base de datos normalizada
- Implementación de API RESTful
- Interfaz de usuario moderna y responsive
- Validaciones de integridad de datos
- Seguridad básica implementada

