from flask import Blueprint
from Personas.Ciudadano import Ciudadano
from Personas.AgentePolicia import AgentePolicia
from Personas.Administrador import Administrador
from Personas.Persona import Persona


# Crear y configurar el blueprint principal
admin_bp = Blueprint('admin', __name__)

# Auto-registrar todos los sub-blueprints
admin_bp.register_blueprint(ciudadanos_bp)
admin_bp.register_blueprint(establecimientos_bp)
admin_bp.register_blueprint(auth_bp)


