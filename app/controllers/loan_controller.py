from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.loan_service import LoanService

loan_bp = Blueprint('loan', __name__, url_prefix='/api/loans')

@loan_bp.route('/borrow', methods=['POST'])
@jwt_required()
def borrow_book():
    """Kitap ödünç alma"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        kitapID = data.get('kitapID')
        gun_sayisi = data.get('gun_sayisi', 14)
        
        if not kitapID:
            return jsonify({'success': False, 'message': 'Kitap ID gerekli!'}), 400
        
        result = LoanService.borrow_book(kitapID, current_user_id, gun_sayisi)
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@loan_bp.route('/return/<int:oduncID>', methods=['POST'])
@jwt_required()
def return_book(oduncID):
    """Kitap iade etme"""
    try:
        result = LoanService.return_book(oduncID)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@loan_bp.route('/my-loans', methods=['GET'])
@jwt_required()
def get_my_loans():
    """Kullanıcının ödünç aldığı kitapları getirir"""
    try:
        current_user_id = get_jwt_identity()
        result = LoanService.get_user_loans(current_user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@loan_bp.route('/my-active-loans', methods=['GET'])
@jwt_required()
def get_my_active_loans():
    """Kullanıcının aktif ödünçlerini getirir"""
    try:
        current_user_id = get_jwt_identity()
        result = LoanService.get_active_loans(current_user_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@loan_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_loans():
    """Tüm ödünç kayıtlarını getirir (Sadece admin)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'admin':
            return jsonify({'success': False, 'message': 'Yetkiniz yok!'}), 403
        
        result = LoanService.get_all_loans()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@loan_bp.route('/overdue', methods=['GET'])
@jwt_required()
def get_overdue_loans():
    """Geciken kitapları getirir (Sadece admin)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'admin':
            return jsonify({'success': False, 'message': 'Yetkiniz yok!'}), 403
        
        result = LoanService.get_overdue_loans()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500