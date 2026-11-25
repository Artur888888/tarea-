# ==========================================
# 1. CAPA DE MODELO (Model)
# Responsabilidad: Entidades, Persistencia (BD) y Reglas de Negocio
# ==========================================

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import update

db = SQLAlchemy()


class Videojuego(db.Model):
    __tablename__ = 'videojuegos'

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.String(50), nullable=False, index=True)
    precio = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    ventas_totales = db.Column(db.Integer, default=0, nullable=False)

    def to_dict(self):
        """Convierte el objeto del modelo a diccionario JSON serializable."""
        return {
            "id": self.id,
            "titulo": self.titulo,
            "categoria": self.categoria,
            "precio": round(float(self.precio), 2),
            "stock": self.stock,
            "ventas_totales": self.ventas_totales,
        }


class JuegoService:
    """Reglas de negocio y acceso a datos."""

    @staticmethod
    def obtener_juegos(categoria=None, limit=100, offset=0):
        consulta = Videojuego.query
        if categoria:
            consulta = consulta.filter_by(categoria=categoria)
        return consulta.order_by(Videojuego.id).limit(limit).offset(offset).all()

    @staticmethod
    def registrar_venta(juego_id, cantidad):
        juego = db.session.get(Videojuego, juego_id)
        if juego is None:
            return None, "Juego no encontrado", 404

        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad <= 0:
            return None, "La cantidad debe ser un entero positivo", 400

        try:
            # Una sola instrucción WHERE evita vender más unidades que las disponibles
            # aunque lleguen varias solicitudes al mismo tiempo.
            statement = (
                update(Videojuego)
                .where(Videojuego.id == juego_id)
                .where(Videojuego.stock >= cantidad)
                .values(
                    stock=Videojuego.stock - cantidad,
                    ventas_totales=Videojuego.ventas_totales + cantidad,
                )
                .execution_options(synchronize_session=False)
            )
            resultado = db.session.execute(statement)

            if resultado.rowcount != 1:
                db.session.rollback()
                return None, "Stock insuficiente", 409

            db.session.commit()
            juego = db.session.get(Videojuego, juego_id)
            return juego, "Venta registrada con éxito", 200
        except Exception:
            db.session.rollback()
            raise
