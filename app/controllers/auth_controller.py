from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.auth_service import AuthService
from app.repositories.user_repository import UserRepository
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

def is_valid_email(email):
    """Email formatı kontrolü"""
    if not email or not isinstance(email, str):
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_password(password):
    """Şifre güvenlik kontrolü (minimum 6 karakter)"""
    if not password or not isinstance(password, str):
        return False
    return len(password) >= 6

def sanitize_input(text):
    """Kullanıcı girdilerini temizle"""
    if not text or not isinstance(text, str):
        return ""
    return text.strip()[:200]

@auth_bp.route('/register', methods=['POST'])
def register():
    """Kullanıcı kaydı - Saatte 3 kayıt"""
    # Rate limiter decorator yerine manuel kontrol
    limiter = current_app.limiter
    limiter.limit("3 per hour")(lambda: None)()
    
    try:
        data = request.get_json()
        
        kullanici_adsoyad = sanitize_input(data.get('kullanici_adsoyad'))
        email = sanitize_input(data.get('email'))
        password = data.get('password')
        rol = data.get('rol', 'ogrenci')
        
        if not all([kullanici_adsoyad, email, password]):
            return jsonify({'success': False, 'message': 'Tüm alanları doldurun!'}), 400
        
        if not is_valid_email(email):
            return jsonify({'success': False, 'message': 'Geçersiz email formatı!'}), 400
        
        if not is_valid_password(password):
            return jsonify({'success': False, 'message': 'Şifre en az 6 karakter olmalıdır!'}), 400
        
        if rol != 'ogrenci':
            rol = 'ogrenci'
        
        result = AuthService.register(kullanici_adsoyad, email, password, rol)
        
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400
    
    except Exception as e:
        print(f" Register error: {str(e)}")
        return jsonify({'success': False, 'message': 'Kayıt sırasında bir hata oluştu!'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Kullanıcı girişi - Dakikada 5 deneme"""
    limiter = current_app.limiter
    limiter.limit("5 per minute")(lambda: None)()
    
    try:
        data = request.get_json()
        
        email = sanitize_input(data.get('email'))
        password = data.get('password')
        
        if not all([email, password]):
            return jsonify({'success': False, 'message': 'Email ve şifre gerekli!'}), 400
        
        if not is_valid_email(email):
            return jsonify({'success': False, 'message': 'Geçersiz email formatı!'}), 400
        
        result = AuthService.login(email, password)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 401
    
    except Exception as e:
        print(f" Login error: {str(e)}")
        return jsonify({'success': False, 'message': 'Giriş sırasında bir hata oluştu!'}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Giriş yapmış kullanıcı bilgilerini getirir"""
    try:
        current_user_id = get_jwt_identity()
        user = UserRepository.find_by_id(current_user_id)
        
        if user:
            return jsonify({'success': True, 'user': user.to_dict()}), 200
        else:
            return jsonify({'success': False, 'message': 'Kullanıcı bulunamadı!'}), 404
    
    except Exception as e:
        print(f" Get user error: {str(e)}")
        return jsonify({'success': False, 'message': 'Kullanıcı bilgileri alınamadı!'}), 500

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Şifre değiştirme - Saatte 3 değişiklik"""
    limiter = current_app.limiter
    limiter.limit("3 per hour")(lambda: None)()
    
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        
        if not all([old_password, new_password]):
            return jsonify({'success': False, 'message': 'Eski ve yeni şifre gerekli!'}), 400
        
        if not is_valid_password(new_password):
            return jsonify({'success': False, 'message': 'Yeni şifre en az 6 karakter olmalıdır!'}), 400
        
        if old_password == new_password:
            return jsonify({'success': False, 'message': 'Yeni şifre eski şifre ile aynı olamaz!'}), 400
        
        result = AuthService.change_password(current_user_id, old_password, new_password)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    
    except Exception as e:
        print(f" Change password error: {str(e)}")
        return jsonify({'success': False, 'message': 'Şifre değiştirme sırasında bir hata oluştu!'}), 500