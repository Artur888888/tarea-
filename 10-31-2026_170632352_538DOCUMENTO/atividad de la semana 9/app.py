# ==========================================
# SERVIDOR PRINCIPAL (Arquitectura Cliente-Servidor)
# ==========================================

import os

from flask import Flask, render_template

from models import db, Videojuego
from controllers import api_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL', 'sqlite:///gamezone.db'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024

SECRET_KEY = os.getenv('SECRET_KEY')
if SECRET_KEY:
    app.config['SECRET_KEY'] = SECRET_KEY

db.init_app(app)
app.register_blueprint(api_bp)


@app.route('/')
def index():
    """Servidor entrega la Vista principal al Cliente"""
    return render_template('index.html')


def inicializar_bd():
    with app.app_context():
        db.create_all()
        if not db.session.query(Videojuego.id).first():
            juegos_demo = [
                Videojuego(titulo="Elden Ring", categoria="RPG", precio=59.99, stock=15, ventas_totales=120),
                Videojuego(titulo="FIFA 2026", categoria="Deportes", precio=69.99, stock=30, ventas_totales=350),
                Videojuego(titulo="Cyberpunk 2077", categoria="RPG", precio=49.99, stock=10, ventas_totales=200),
                Videojuego(titulo="God of War", categoria="Accion", precio=39.99, stock=8, ventas_totales=180),
            ]
            db.session.add_all(juegos_demo)
            db.session.commit()


if __name__ == '__main__':
    inicializar_bd()
    debug = os.getenv('FLASK_DEBUG', '0') == '1'
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', '5000'))
    app.run(host=host, port=port, debug=debug)
