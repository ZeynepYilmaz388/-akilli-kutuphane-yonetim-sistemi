from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.loan_service import LoanService

loan_bp = Blueprint('loan', __name__, url_prefix='/api/loans')

# ÖDÜNÇ ALMA ENDPOINTİ
@loan_bp.route('/borrow/<int:kitapID>', methods=['POST'])
@jwt_required()
def borrow_book(kitapID):
    """Kitap ödünç alma endpoint'i"""
    try:
        # Kullanıcı kimliğini al
        current_user_id = get_jwt_identity()
        
        # Gün sayısı (isteğe bağlı, default 14 gün)
        try:
            data = request.get_json(silent=True) or {}
        except:
            data = {}
        gun_sayisi = data.get('gun_sayisi', 14)
        
        # Ödünç verme işlemi
        result = LoanService.borrow_book(kitapID, current_user_id, gun_sayisi)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': result['message']
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 400
            
    except Exception as e:
        print(f" Ödünç alma hatası: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Bir hata oluştu: {str(e)}'
        }), 500


#  İADE ETME ENDPOINTİ
@loan_bp.route('/return/<int:oduncID>', methods=['POST'])
@jwt_required()
def return_book(oduncID):
    """Kitap iade etme endpoint'i"""
    try:
        # İade işlemi
        result = LoanService.return_book(oduncID)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': result['message']
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 400
            
    except Exception as e:
        print(f" İade hatası: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Bir hata oluştu: {str(e)}'
        }), 500


#  KULLANICININ ÖDÜNÇ KİTAPLARINI LİSTELE
@loan_bp.route('/my-loans', methods=['GET'])
@jwt_required()
def get_my_loans():
    """Kullanıcının ödünç aldığı kitapları listele"""
    try:
        current_user_id = get_jwt_identity()
        
        # Kullanıcının tüm ödünç kayıtlarını getir
        result = LoanService.get_user_loans(current_user_id)
        
        if result['success']:
            return jsonify({
                'success': True,
                'loans': result['loans']
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': result['message'],
                'loans': []
            }), 400
            
    except Exception as e:
        print(f" Liste hatası: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Bir hata oluştu: {str(e)}',
            'loans': []
        }), 500


# KULLANICININ AKTİF ÖDÜNÇ KİTAPLARINI LİSTELE
@loan_bp.route('/my-active-loans', methods=['GET'])
@jwt_required()
def get_my_active_loans():
    """Kullanıcının aktif ödünç kitaplarını listele"""
    try:
        current_user_id = get_jwt_identity()
        
        # Sadece aktif ödünç kayıtlarını getir
        result = LoanService.get_active_loans(current_user_id)
        
        if result['success']:
            return jsonify({
                'success': True,
                'loans': result['loans']
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': result['message'],
                'loans': []
            }), 400
            
    except Exception as e:
        print(f"Aktif liste hatası: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Bir hata oluştu: {str(e)}',
            'loans': []
        }), 500


#  TÜM ÖDÜNÇ KAYITLARINI LİSTELE (Admin için)
@loan_bp.route('/all', methods=['GET'])
@jwt_required()
def get_all_loans():
    """Tüm ödünç kayıtlarını listele (Admin)"""
    try:
        # Admin kontrolü
        claims = get_jwt()
        if claims.get('rol') != 'admin':
            return jsonify({
                'success': False,
                'message': 'Bu işlem için yetkiniz yok!'
            }), 403
        
        # Tüm ödünç kayıtlarını getir
        result = LoanService.get_all_loans()
        
        if result['success']:
            return jsonify({
                'success': True,
                'loans': result['loans']
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': result['message'],
                'loans': []
            }), 400
            
    except Exception as e:
        print(f" Tüm liste hatası: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Bir hata oluştu: {str(e)}',
            'loans': []
        }), 500


# GECİKEN KİTAPLARI LİSTELE (Admin için)
@loan_bp.route('/overdue', methods=['GET'])
@jwt_required()
def get_overdue_loans():
    """Geciken kitapları listele (Admin)"""
    try:
        # Admin kontrolü
        claims = get_jwt()
        if claims.get('rol') != 'admin':
            return jsonify({
                'success': False,
                'message': 'Bu işlem için yetkiniz yok!'
            }), 403
        
        # Geciken kitapları getir
        result = LoanService.get_overdue_loans()
        
        if result['success']:
            return jsonify({
                'success': True,
                'loans': result['loans']
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': result['message'],
                'loans': []
            }), 400
            
    except Exception as e:
        print(f" Geciken liste hatası: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Bir hata oluştu: {str(e)}',
            'loans': []
        }), 500    
    # İADE EDİLEN KİTAPLARI LİSTELE
@loan_bp.route('/my-returned-loans', methods=['GET'])
@jwt_required()
def get_my_returned_loans():
    """Kullanıcının iade ettiği kitapları listele"""
    try:
        current_user_id = get_jwt_identity()
        
        # İade edilmiş kayıtları getir
        result = LoanService.get_returned_loans(current_user_id)
        
        if result['success']:
            return jsonify({
                'success': True,
                'loans': result['loans']
            }), 200
        else:
            return jsonify({
                'success': False,
                'message': result['message'],
                'loans': []
            }), 400
    
    except Exception as e:
        print(f"İade edilenler liste hatası: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Bir hata oluştu: {str(e)}',
            'loans': []
        }), 500