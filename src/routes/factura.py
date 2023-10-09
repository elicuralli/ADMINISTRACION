from flask import Blueprint, jsonify
from models.facturamodel import FacturaModel
import traceback
factura_bp = Blueprint('factura_bp', __name__)

@factura_bp.route('/', methods=['GET'])
def get_invoice_number():
    try:
        incremented_number = FacturaModel.get_incremented_number()
        return jsonify({
            'ok': True,
            'status': 200,
            'data': {'nroFactura': incremented_number}
        }), 200
    except Exception as e:
        print(e)
        traceback.print_exc()
        return jsonify({
            'ok': False,
            'status': 500,
            'message': str(e)
        }), 500
