from app.utils.database import Database
from app.models.book import Book

class BookRepository:
    
    @staticmethod
    def create(book):
        """Yeni kitap ekler"""
        query = """
            INSERT INTO KITAPLAR (baslik, yazarID, kategoriID, yayin_yili, stok_adedi, musait_adet)
            VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (book.baslik, book.yazarID, book.kategoriID, book.yayin_yili, 
                 book.stok_adedi, book.musait_adet)
        Database.execute_query(query, params)
        return True
    
    @staticmethod
    def find_by_id(kitapID):
        """ID'ye göre kitap getirir"""
        query = "SELECT * FROM KITAPLAR WHERE kitapID = ?"
        row = Database.execute_query(query, (kitapID,), fetch_one=True)
        return Book.from_db_row(row) if row else None
    
    @staticmethod
    def find_all():
        """Tüm kitapları getirir"""
        query = """
            SELECT k.*, y.yazar_ad, y.yazar_soyad, kat.katagori_adi
            FROM KITAPLAR k
            LEFT JOIN YAZARLAR y ON k.yazarID = y.yazarID
            LEFT JOIN KATEGORILER kat ON k.kategoriID = kat.kategoriID
            ORDER BY k.baslik
        """
        rows = Database.execute_query(query, fetch=True)
        return rows if rows else []
    
    @staticmethod
    def search_by_title(title):
        """Başlığa göre kitap arar"""
        query = """
            SELECT k.*, y.yazar_ad, y.yazar_soyad, kat.katagori_adi
            FROM KITAPLAR k
            LEFT JOIN YAZARLAR y ON k.yazarID = y.yazarID
            LEFT JOIN KATEGORILER kat ON k.kategoriID = kat.kategoriID
            WHERE k.baslik LIKE ?
            ORDER BY k.baslik
        """
        rows = Database.execute_query(query, (f'%{title}%',), fetch=True)
        return rows if rows else []
    
    @staticmethod
    def find_by_author(yazarID):
        """Yazara göre kitapları getirir"""
        query = """
            SELECT k.*, y.yazar_ad, y.yazar_soyad, kat.katagori_adi
            FROM KITAPLAR k
            LEFT JOIN YAZARLAR y ON k.yazarID = y.yazarID
            LEFT JOIN KATEGORILER kat ON k.kategoriID = kat.kategoriID
            WHERE k.yazarID = ?
            ORDER BY k.baslik
        """
        rows = Database.execute_query(query, (yazarID,), fetch=True)
        return rows if rows else []
    
    @staticmethod
    def find_by_category(kategoriID):
        """Kategoriye göre kitapları getirir"""
        query = """
            SELECT k.*, y.yazar_ad, y.yazar_soyad, kat.katagori_adi
            FROM KITAPLAR k
            LEFT JOIN YAZARLAR y ON k.yazarID = y.yazarID
            LEFT JOIN KATEGORILER kat ON k.kategoriID = kat.kategoriID
            WHERE k.kategoriID = ?
            ORDER BY k.baslik
        """
        rows = Database.execute_query(query, (kategoriID,), fetch=True)
        return rows if rows else []
    
    @staticmethod
    def update(kitapID, book):
        """Kitap bilgilerini günceller"""
        query = """
            UPDATE KITAPLAR 
            SET baslik = ?, yazarID = ?, kategoriID = ?, yayin_yili = ?, 
                stok_adedi = ?, musait_adet = ?
            WHERE kitapID = ?
        """
        params = (book.baslik, book.yazarID, book.kategoriID, book.yayin_yili,
                 book.stok_adedi, book.musait_adet, kitapID)
        Database.execute_query(query, params)
        return True
    
    @staticmethod
    def delete(kitapID):
        """Kitap siler"""
        query = "DELETE FROM KITAPLAR WHERE kitapID = ?"
        Database.execute_query(query, (kitapID,))
        return True
    
    @staticmethod
    def get_available_books():
        """Müsait kitapları getirir"""
        query = """
            SELECT k.*, y.yazar_ad, y.yazar_soyad, kat.katagori_adi
            FROM KITAPLAR k
            LEFT JOIN YAZARLAR y ON k.yazarID = y.yazarID
            LEFT JOIN KATEGORILER kat ON k.kategoriID = kat.kategoriID
            WHERE k.musait_adet > 0
            ORDER BY k.baslik
        """
        rows = Database.execute_query(query, fetch=True)
        return rows if rows else []