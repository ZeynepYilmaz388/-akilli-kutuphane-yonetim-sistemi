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
            existing_user = UserRepository.find_by_email(email)
            if existing_user:
                return {'success': False, 'message': 'Bu email adresi zaten kayıtlı!'}
            
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            
            user = User(
                kullanici_adsoyad=kullanici_adsoyad,
                kullanici_sifre=hashed_password,
                kullanici_rol=rol,
                kullanici_eposta=email
            )
            
            result = UserRepository.create(user)
            
            if result:
                return {'success': True, 'message': 'Kayıt başarılı!'}
            else:
                return {'success': False, 'message': 'Kayıt sırasında bir hata oluştu!'}
        
        except Exception as e:
            print(f"Register service hatası: {e}")
            return {'success': False, 'message': f'Kayıt hatası: {str(e)}'}
    
    @staticmethod
    def login(email, password):
        """Kullanıcı girişi yapar"""
        try:
            user = UserRepository.find_by_email(email)
            
            if not user:
                return {'success': False, 'message': 'Email veya şifre hatalı!'}
            
            if not bcrypt.check_password_hash(user.kullanici_sifre, password):
                return {'success': False, 'message': 'Email veya şifre hatalı!'}
            
            # ÖNEMLİ: kullaniciID integer olmalı!
            user_id = int(user.kullaniciID) if user.kullaniciID else None
            
            if not user_id:
                print("HATA: kullaniciID bulunamadı!")
                return {'success': False, 'message': 'Kullanıcı ID hatası!'}
            
            print(f"Token oluşturuluyor - User ID: {user_id} (type: {type(user_id)})")  # Debug
            
            access_token = create_access_token(
                identity=str(user_id),  # ← integer olmalı!
                additional_claims={
                    'rol': str(user.kullanici_rol),
                    'email': str(user.kullanici_eposta)
                }
            )
            
            print(f"Token başarıyla oluşturuldu!")  # Debug
            
            return {
                'success': True,
                'message': 'Giriş başarılı!',
                'access_token': access_token,
                'user': user.to_dict()
            }
        
        except Exception as e:
            print(f"Login service hatası: {e}")
            import traceback
            traceback.print_exc()  # Tam hata detayı
            return {'success': False, 'message': f'Giriş hatası: {str(e)}'}
    
    @staticmethod
    def change_password(kullaniciID, old_password, new_password):
        """Kullanıcı şifresini değiştirir"""
        try:
            user = UserRepository.find_by_id(kullaniciID)
            
            if not user:
                return {'success': False, 'message': 'Kullanıcı bulunamadı!'}
            
            if not bcrypt.check_password_hash(user.kullanici_sifre, old_password):
                return {'success': False, 'message': 'Eski şifre hatalı!'}
            
            new_hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            
            UserRepository.update_password(kullaniciID, new_hashed_password)
            
            return {'success': True, 'message': 'Şifre başarıyla değiştirildi!'}
        
        except Exception as e:
            return {'success': False, 'message': f'Şifre değiştirme hatası: {str(e)}'}