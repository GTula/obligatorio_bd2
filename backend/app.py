from flask import Flask
from routes.ciudadanos import ciudadanos_bp
from routes.circuito import circuito_bp
from routes.mesa import mesa_bp
from routes.empleados import login_presidente_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.register_blueprint(ciudadanos_bp, url_prefix="/api/ciudadanos")
app.register_blueprint(circuito_bp, url_prefix="/api/circuito")
app.register_blueprint(mesa_bp, url_prefix="/api/mesa")
app.register_blueprint(login_presidente_bp, url_prefix="/api/login_presidente")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)