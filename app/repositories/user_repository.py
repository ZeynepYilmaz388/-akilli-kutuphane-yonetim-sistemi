from app.utils.database import Database
from app.models.user import User

class UserRepository:
    
    @staticmethod
    def create(user):
        """Yeni kullanıcı oluşturur"""
        query = """
            INSERT INTO KULLANICILAR (kullanici_adsoyad, kullanici_sifre, kullanici_rol, kullanici_eposta)
            VALUES (%s, %s, %s, %s)
            RETURNING kullaniciID
        """
        params = (user.kullanici_adsoyad, user.kullanici_sifre, user.kullanici_rol, user.kullanici_eposta)
        try:
            result = Database.execute_query(query, params, fetch_one=True)
            return result['kullaniciid'] if result else None
        except Exception as e:
            print(f"Kullanıcı oluşturma hatası: {e}")
            return None
    
    @staticmethod
    def find_by_id(kullaniciID):
        """ID'ye göre kullanıcı getirir"""
        query = "SELECT * FROM KULLANICILAR WHERE kullaniciID = %s"
        row = Database.execute_query(query, (kullaniciID,), fetch_one=True)
        return User.from_db_row(row) if row else None
    
    @staticmethod
    def find_by_email(email):
        """Email'e göre kullanıcı getirir"""
        query = "SELECT * FROM KULLANICILAR WHERE kullanici_eposta = %s"
        row = Database.execute_query(query, (email,), fetch_one=True)
        return User.from_db_row(row) if row else None
    
    @staticmethod
    def find_all():
        """Tüm kullanıcıları getirir"""
        query = "SELECT * FROM KULLANICILAR"
        rows = Database.execute_query(query, fetch=True)
        return [User.from_db_row(row) for row in rows] if rows else []
    
    @staticmethod
    def update(kullaniciID, user):
        """Kullanıcı bilgilerini günceller"""
        query = """
            UPDATE KULLANICILAR 
            SET kullanici_adsoyad = %s, kullanici_rol = %s, kullanici_eposta = %s
            WHERE kullaniciID = %s
        """
        params = (user.kullanici_adsoyad, user.kullanici_rol, user.kullanici_eposta, kullaniciID)
        Database.execute_query(query, params)
        return True
    
    @staticmethod
    def delete(kullaniciID):
        """Kullanıcı siler"""
        query = "DELETE FROM KULLANICILAR WHERE kullaniciID = %s"
        Database.execute_query(query, (kullaniciID,))
        return True
    
    @staticmethod
    def update_password(kullaniciID, new_password_hash):
        """Kullanıcı şifresini günceller"""
        query = "UPDATE KULLANICILAR SET kullanici_sifre = %s WHERE kullaniciID = %s"
        Database.execute_query(query, (new_password_hash, kullaniciID))
        return True