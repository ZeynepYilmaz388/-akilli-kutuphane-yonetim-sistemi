from app.utils.database import Database
from app.models.author import Author

class AuthorRepository:
    
    @staticmethod
    def create(author):
        """Yeni yazar ekler"""
        query = """
            INSERT INTO YAZARLAR (yazar_ad, yazar_soyad, yazar_ulke)
            VALUES (?, ?, ?)
        """
        params = (author.yazar_ad, author.yazar_soyad, author.yazar_ulke)
        Database.execute_query(query, params)
        return True
    
    @staticmethod
    def find_by_id(yazarID):
        """ID'ye göre yazar getirir"""
        query = "SELECT * FROM YAZARLAR WHERE yazarID = ?"
        row = Database.execute_query(query, (yazarID,), fetch_one=True)
        return Author.from_db_row(row) if row else None
    
    @staticmethod
    def find_all():
        """Tüm yazarları getirir"""
        query = "SELECT * FROM YAZARLAR ORDER BY yazar_soyad, yazar_ad"
        rows = Database.execute_query(query, fetch=True)
        return [Author.from_db_row(row) for row in rows] if rows else []
    
    @staticmethod
    def search_by_name(name):
        """İsme göre yazar arar"""
        query = """
            SELECT * FROM YAZARLAR 
            WHERE yazar_ad LIKE ? OR yazar_soyad LIKE ?
            ORDER BY yazar_soyad, yazar_ad
        """
        rows = Database.execute_query(query, (f'%{name}%', f'%{name}%'), fetch=True)
        return [Author.from_db_row(row) for row in rows] if rows else []
    
    @staticmethod
    def update(yazarID, author):
        """Yazar bilgilerini günceller"""
        query = """
            UPDATE YAZARLAR 
            SET yazar_ad = ?, yazar_soyad = ?, yazar_ulke = ?
            WHERE yazarID = ?
        """
        params = (author.yazar_ad, author.yazar_soyad, author.yazar_ulke, yazarID)
        Database.execute_query(query, params)
        return True
    
    @staticmethod
    def delete(yazarID):
        """Yazar siler"""
        query = "DELETE FROM YAZARLAR WHERE yazarID = ?"
        Database.execute_query(query, (yazarID,))
        return True