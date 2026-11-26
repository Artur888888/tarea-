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
                Videojuego(titulo="Elden Ring", categoria="RPG", precio=59.99, stock=15, ventas_totales=120, imagen="/static/img/portadas/elden-ring.jpg"),
                Videojuego(titulo="EA Sports FC 25", categoria="Deportes", precio=69.99, stock=30, ventas_totales=350, imagen="/static/img/portadas/fc-25.jpg"),
                Videojuego(titulo="God of War Ragnarök", categoria="Accion", precio=39.99, stock=8, ventas_totales=180, imagen="/static/img/portadas/god-of-war.jpg"),
                Videojuego(titulo="Grand Theft Auto V", categoria="Accion", precio=29.99, stock=20, ventas_totales=410, imagen="/static/img/portadas/gta-v.jpg"),
                Videojuego(titulo="Plants vs. Zombies: Garden Warfare 2", categoria="Shooter", precio=19.99, stock=25, ventas_totales=240, imagen="/static/img/portadas/pvz-gw2.jpg"),
            ]
            db.session.add_all(juegos_demo)
            db.session.commit()


if __name__ == '__main__':
    inicializar_bd()
    debug = os.getenv('FLASK_DEBUG', '0') == '1'
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', '5000'))
    app.run(host=host, port=port, debug=debug)