from flask import Blueprint

# Importa aquí todos los blueprints de la carpeta admin y subcarpetas
from routes.admin.Personas.Ciudadano import ciudadano_bp
from routes.admin.Personas.EmpleadoPublico import empleado_publico_bp
from routes.admin.Personas.Candidato import candidato_bp
from routes.admin.Personas.Autoridad import autoridad_bp
from routes.admin.Personas.Credencial import credencial_bp
from routes.admin.Personas.AgentePolicia import agente_policia_bp
from routes.admin.Personas.TipoEmpleado import tipo_empleado_bp

from routes.admin.Lugares.Departamento import departamento_bp
from routes.admin.Lugares.Zona import zona_bp
from routes.admin.Lugares.Establecimiento import establecimiento_bp
from routes.admin.Lugares.Comisaria import comisaria_bp
from routes.admin.Lugares.Circuito import circuito_bp

from routes.admin.Grupos.Mesa import mesa_bp
from routes.admin.Grupos.Partido import partido_bp

from routes.admin.Eleccion.Eleccion import eleccion_bp
from routes.admin.Eleccion.TipoEleccion import tipo_eleccion_bp
from routes.admin.Eleccion.Papeleta import papeleta_bp
from routes.admin.Eleccion.PapeletaPlebiscito import papeleta_plebiscito_bp
from routes.admin.Eleccion.Lista import lista_bp

from routes.admin.Relaciones.Asignado import asignado_bp
from routes.admin.Relaciones.VotaEn import vota_en_bp
from routes.admin.Relaciones.CandidatoXLista import candidato_por_lista_bp
from routes.admin.Relaciones.AgenteEstablecimiento import agente_establecimiento_bp


# Crear y configurar el blueprint principal
admin_bp = Blueprint('admin', __name__)

# Registrar todos los sub-blueprints
admin_bp.register_blueprint(ciudadano_bp)
admin_bp.register_blueprint(empleado_publico_bp)
admin_bp.register_blueprint(candidato_bp)
admin_bp.register_blueprint(autoridad_bp)
admin_bp.register_blueprint(credencial_bp)
admin_bp.register_blueprint(agente_policia_bp)
admin_bp.register_blueprint(tipo_empleado_bp)

admin_bp.register_blueprint(departamento_bp)
admin_bp.register_blueprint(zona_bp)
admin_bp.register_blueprint(establecimiento_bp)
admin_bp.register_blueprint(comisaria_bp)
admin_bp.register_blueprint(circuito_bp)

admin_bp.register_blueprint(mesa_bp)
admin_bp.register_blueprint(partido_bp)

admin_bp.register_blueprint(eleccion_bp)
admin_bp.register_blueprint(tipo_eleccion_bp)
admin_bp.register_blueprint(papeleta_bp)
admin_bp.register_blueprint(papeleta_plebiscito_bp)
admin_bp.register_blueprint(lista_bp)

admin_bp.register_blueprint(asignado_bp)
admin_bp.register_blueprint(vota_en_bp)
admin_bp.register_blueprint(candidato_por_lista_bp)
admin_bp.register_blueprint(agente_establecimiento_bp)


