from flask import Flask
from flask_cors import CORS
from routes.ciudadanos import ciudadanos_bp
from routes.circuito import circuito_bp
from routes.mesa import mesa_bp
from routes.empleados import login_presidente_bp
from routes.eleccion import eleccion_bp
from routes.admin.loginAdmin import login_admin_bp
from routes.admin.admin import admin_bp
from routes.votantes import votantes_bp
from routes.votos_circuito import votos_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(ciudadanos_bp, url_prefix="/api/ciudadanos")
app.register_blueprint(circuito_bp, url_prefix="/api/circuito")
app.register_blueprint(mesa_bp, url_prefix="/api/mesa")
app.register_blueprint(votos_bp, url_prefix="/api/votos")
app.register_blueprint(login_presidente_bp, url_prefix="/api/login_presidente")
app.register_blueprint(eleccion_bp, url_prefix="/api/eleccion")
app.register_blueprint(login_admin_bp, url_prefix="/api/login_admin")
app.register_blueprint(admin_bp, url_prefix="/api/admin")
app.register_blueprint(votantes_bp, url_prefix="/api/votantes")

@app.route('/debug/routes')
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.parse.unquote(f"{rule.endpoint}: {rule.rule} [{methods}]")
        output.append(line)
    return '<br>'.join(sorted(output))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)