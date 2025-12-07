from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from app.repositories.user_repository import UserRepository
from app.models.user import User

bcrypt = Bcrypt()

class AuthService:
    
    @staticmethod
    def register(kullanici_adsoyad, email, password, rol='ogrenci'):
        """Yeni kullanıcı kaydı oluşturur"""
        try:
            # Email kontrolü
            existing_user = UserRepository.find_by_email(email)
            if existing_user:
                return {'success': False, 'message': 'Bu email adresi zaten kayıtlı!'}
            
            # Şifreyi hashle
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            
            # Yeni kullanıcı oluştur
            user = User(
                kullanici_adsoyad=kullanici_adsoyad,
                kullanici_sifre=hashed_password,
                kullanici_rol=rol,
                kullanici_eposta=email
            )
            
            UserRepository.create(user)
            
            return {'success': True, 'message': 'Kayıt başarılı!'}
        
        except Exception as e:
            return {'success': False, 'message': f'Kayıt hatası: {str(e)}'}
    
    @staticmethod
    def login(email, password):
        """Kullanıcı girişi yapar"""
        try:
            # Kullanıcıyı bul
            user = UserRepository.find_by_email(email)
            
            if not user:
                return {'success': False, 'message': 'Email veya şifre hatalı!'}
            
            # Şifre kontrolü
            if not bcrypt.check_password_hash(user.kullanici_sifre, password):
                return {'success': False, 'message': 'Email veya şifre hatalı!'}
            
            # JWT token oluştur
            access_token = create_access_token(
                identity=user.kullaniciID,
                additional_claims={
                    'rol': user.kullanici_rol,
                    'email': user.kullanici_eposta
                }
            )
            
            return {
                'success': True,
                'message': 'Giriş başarılı!',
                'access_token': access_token,
                'user': user.to_dict()
            }
        
        except Exception as e:
            return {'success': False, 'message': f'Giriş hatası: {str(e)}'}
    
    @staticmethod
    def change_password(kullaniciID, old_password, new_password):
        """Kullanıcı şifresini değiştirir"""
        try:
            user = UserRepository.find_by_id(kullaniciID)
            
            if not user:
                return {'success': False, 'message': 'Kullanıcı bulunamadı!'}
            
            # Eski şifre kontrolü
            if not bcrypt.check_password_hash(user.kullanici_sifre, old_password):
                return {'success': False, 'message': 'Eski şifre hatalı!'}
            
            # Yeni şifreyi hashle
            new_hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            
            UserRepository.update_password(kullaniciID, new_hashed_password)
            
            return {'success': True, 'message': 'Şifre başarıyla değiştirildi!'}
        
        except Exception as e:
            return {'success': False, 'message': f'Şifre değiştirme hatası: {str(e)}'}