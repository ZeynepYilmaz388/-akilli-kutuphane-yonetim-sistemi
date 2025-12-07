from app.utils.database import Database
from app.models.category import Category

class CategoryRepository:
    
    @staticmethod
    def create(category):
        """Yeni kategori ekler"""
        query = """
            INSERT INTO KATEGORILER (katagori_adi, aciklama)
            VALUES (?, ?)
        """
        params = (category.katagori_adi, category.aciklama)
        Database.execute_query(query, params)
        return True
    
    @staticmethod
    def find_by_id(kategoriID):
        """ID'ye göre kategori getirir"""
        query = "SELECT * FROM KATEGORILER WHERE kategoriID = ?"
        row = Database.execute_query(query, (kategoriID,), fetch_one=True)
        return Category.from_db_row(row) if row else None
    
    @staticmethod
    def find_all():
        """Tüm kategorileri getirir"""
        query = "SELECT * FROM KATEGORILER ORDER BY katagori_adi"
        rows = Database.execute_query(query, fetch=True)
        return [Category.from_db_row(row) for row in rows] if rows else []
    
    @staticmethod
    def update(kategoriID, category):
        """Kategori bilgilerini günceller"""
        query = """
            UPDATE KATEGORILER 
            SET katagori_adi = ?, aciklama = ?
            WHERE kategoriID = ?
        """
        params = (category.katagori_adi, category.aciklama, kategoriID)
        Database.execute_query(query, params)
        return True
    
    @staticmethod
    def delete(kategoriID):
        """Kategori siler"""
        query = "DELETE FROM KATEGORILER WHERE kategoriID = ?"
        Database.execute_query(query, (kategoriID,))
        return True