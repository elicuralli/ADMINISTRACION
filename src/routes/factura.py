from flask import Blueprint, jsonify
from models.facturamodel import FacturaModel

factura_bp = Blueprint('factura_bp', __name__)

@factura_bp.route('/factura', methods=['GET'])
def get_invoice_number():
    try:
        current_number = FacturaModel.get_current_number()
        incremented_number = FacturaModel.get_incremented_number()
        return jsonify({
            'ok': True,
            'status': 200,
            'data': {'factura_number': incremented_number}
        }), 200
    except Exception as e:
        return jsonify({
            'ok': False,
            'status': 500,
            'message': str(e)
        }), 500
