from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.penalty_service import PenaltyService

penalty_bp = Blueprint('penalty', __name__, url_prefix='/api/penalties')

@penalty_bp.route('/my', methods=['GET'])
@jwt_required()
def get_my_penalties():
    """Kullanıcının tüm cezalarını getirir"""
    try:
        kullaniciID = get_jwt_identity()
        result = PenaltyService.get_user_penalties(kullaniciID)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@penalty_bp.route('/my/unpaid', methods=['GET'])
@jwt_required()
def get_my_unpaid_penalties():
    """Kullanıcının ödenmemiş cezalarını getirir"""
    try:
        kullaniciID = get_jwt_identity()
        result = PenaltyService.get_unpaid_penalties(kullaniciID)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@penalty_bp.route('/<int:cezaID>/pay', methods=['POST'])
@jwt_required()
def pay_penalty(cezaID):
    """Ceza öder"""
    try:
        result = PenaltyService.pay_penalty(cezaID)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@penalty_bp.route('/check-overdue', methods=['POST'])
@jwt_required()
def check_overdue():
    """Gecikmiş ödünçleri kontrol eder ve ceza oluşturur (Admin)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'admin':
            return jsonify({'success': False, 'message': 'Yetkiniz yok!'}), 403
        
        result = PenaltyService.check_overdue_and_create_penalties()
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@penalty_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_penalties():
    """Tüm cezaları getirir (Admin)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'admin':
            return jsonify({'success': False, 'message': 'Yetkiniz yok!'}), 403
        
        result = PenaltyService.get_all_penalties()
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@penalty_bp.route('/unpaid', methods=['GET'])
@jwt_required()
def get_all_unpaid():
    """Tüm ödenmemiş cezaları getirir (Admin)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'admin':
            return jsonify({'success': False, 'message': 'Yetkiniz yok!'}), 403
        
        result = PenaltyService.get_all_unpaid_penalties()
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
            
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500