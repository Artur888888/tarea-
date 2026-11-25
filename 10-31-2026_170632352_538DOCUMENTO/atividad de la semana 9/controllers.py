# ==========================================
# 2. CAPA DE CONTROLADOR (Controller)
# Responsabilidad: Recibir peticiones HTTP, orquestar servicios y responder
# ==========================================

from flask import Blueprint, jsonify, request

from models import JuegoService

api_bp = Blueprint('api', __name__)


def _leer_entero(argumento, predeterminado=None, minimo=0, maximo=None):
    valor = request.args.get(argumento, predeterminado)
    try:
        valor = int(valor)
    except (TypeError, ValueError):
        return None
    if valor < minimo:
        return None
    if maximo is not None and valor > maximo:
        return None
    return valor


@api_bp.route('/api/juegos', methods=['GET'])
def get_juegos():
    """Endpoint REST para listar videojuegos con filtro y paginación."""
    categoria = request.args.get('categoria', '').strip()
    if len(categoria) > 50:
        return jsonify({"status": "error", "message": "Categoría inválida"}), 400

    limit = _leer_entero('limit', 100, minimo=1, maximo=100)
    offset = _leer_entero('offset', 0, minimo=0, maximo=1_000_000)
    if limit is None or offset is None:
        return jsonify({"status": "error", "message": "Paginación inválida"}), 400

    juegos = JuegoService.obtener_juegos(categoria or None, limit=limit, offset=offset)
    return jsonify([juego.to_dict() for juego in juegos])


@api_bp.route('/api/ventas', methods=['POST'])
def post_venta():
    """Endpoint REST para registrar una venta."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"status": "error", "message": "Se requiere un objeto JSON"}), 400

    juego_id = data.get('juego_id')
    cantidad = data.get('cantidad', 1)

    if isinstance(juego_id, bool) or not isinstance(juego_id, int) or juego_id <= 0:
        return jsonify({"status": "error", "message": "juego_id inválido"}), 400
    if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
        return jsonify({"status": "error", "message": "La cantidad debe ser un entero positivo"}), 400
    if cantidad > 100:
        return jsonify({"status": "error", "message": "La cantidad máxima por venta es 100"}), 400

    juego, mensaje, codigo = JuegoService.registrar_venta(juego_id, cantidad)
    if not juego:
        return jsonify({"status": "error", "message": mensaje}), codigo

    return jsonify({
        "status": "success",
        "message": mensaje,
        "juego": juego.to_dict(),
    })
