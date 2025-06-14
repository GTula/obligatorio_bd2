from flask import Flask
from routes.ciudadanos import ciudadanos_bp
from routes.circuito import circuito_bp
from routes.mesa import mesa_bp

app = Flask(__name__)
app.register_blueprint(ciudadanos_bp, url_prefix="/api/ciudadanos")
app.register_blueprint(circuito_bp, url_prefix="/api/circuito")
app.register_blueprint(mesa_bp, url_prefix="/api/mesa")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)