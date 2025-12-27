from app.utils.database import Database
from app.models.book import Book

class BookRepository:
    
    @staticmethod
    def create(book):
        """Yeni kitap ekler"""
        query = """
            INSERT INTO KITAPLAR (baslik, yazarID, kategoriID, yayin_yili, stok_adedi, musait_adet)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING kitapID
        """
        params = (book.baslik, book.yazarID, book.kategoriID, book.yayin_yili, 
                 book.stok_adedi, book.musait_adet)
        #neden try-catch bloğu eklendi: hata durumunda None döndürülsün
        try:
            result = Database.execute_query(query, params, fetch_one=True)
            return result['kitapid'] if result else None
        #except bloğunda hata mesajı yazdırılıyor ve None döndürülüyor
        except Exception as e:
            print(f"Kitap oluşturma hatası: {e}")
            return None
    
    @staticmethod
    def find_by_id(kitapID):
        """ID'ye göre kitap getirir"""
        query = "SELECT * FROM KITAPLAR WHERE kitapID = %s"
        row = Database.execute_query(query, (kitapID,), fetch_one=True)
        return Book.from_db_row(row) if row else None
    
    @staticmethod
    def find_all():
        """Tüm kitapları getirir - Basitleştirilmiş"""
        query = """
            SELECT 
                k.kitapID,
                k.baslik,
                k.yazarID,
                k.kategoriID,
                k.yayin_yili,
                k.stok_adedi,
                k.musait_adet,
                COALESCE(y.yazar_ad, '') as yazar_ad,
                COALESCE(y.yazar_soyad, '') as yazar_soyad,
                COALESCE(kat.katagori_adi, '') as katagori_adi
            FROM KITAPLAR k
            LEFT JOIN YAZARLAR y ON k.yazarID = y.yazarID
            LEFT JOIN KATEGORILER kat ON k.kategoriID = kat.kategoriID
            ORDER BY k.baslik
        """
        #coalesce ile null değerler boş stringe çevriliyor
        #join ile yazar ve kategori bilgileri alınıyor.left joın eksik veri olsa da getirir
        try:
            rows = Database.execute_query(query, fetch=True)
            # Dictionary'leri direk döndür (RealDictCursor kullanıyoruz)
            return [dict(row) for row in rows] if rows else []
        except Exception as e:
            print(f"Kitapları getirme hatası: {e}")
            return []
    
    @staticmethod
    def search_by_title(title):
        """Başlığa göre kitap arar"""
        query = """
            SELECT 
                k.kitapID,
                k.baslik,
                k.yazarID,
                k.kategoriID,
                k.yayin_yili,
                k.stok_adedi,
                k.musait_adet,
                COALESCE(y.yazar_ad, '') as yazar_ad,
                COALESCE(y.yazar_soyad, '') as yazar_soyad,
                COALESCE(kat.katagori_adi, '') as katagori_adi
            FROM KITAPLAR k
            LEFT JOIN YAZARLAR y ON k.yazarID = y.yazarID
            LEFT JOIN KATEGORILER kat ON k.kategoriID = kat.kategoriID
            WHERE k.baslik ILIKE %s
            ORDER BY k.baslik
        """
        try:
            rows = Database.execute_query(query, (f'%{title}%',), fetch=True)
            #liste  halinde kitaplar
            return [dict(row) for row in rows] if rows else []
        except Exception as e:
            print(f"Kitap arama hatası: {e}")
            return []
    
    @staticmethod
    def update(kitapID, book):
        """Kitap bilgilerini günceller"""
        query = """
            UPDATE KITAPLAR 
            SET baslik = %s, yazarID = %s, kategoriID = %s, yayin_yili = %s, 
                stok_adedi = %s, musait_adet = %s
            WHERE kitapID = %s
        """
        #ID’ye göre kitap güncelleniyor
        params = (book.baslik, book.yazarID, book.kategoriID, book.yayin_yili,
                 book.stok_adedi, book.musait_adet, kitapID)
        try:
            Database.execute_query(query, params)
            return True
        except Exception as e:
            print(f"Kitap güncelleme hatası: {e}")
            return False
    
    @staticmethod
    def delete(kitapID):
        """Kitap siler"""
        query = "DELETE FROM KITAPLAR WHERE kitapID = %s"
        try:
            Database.execute_query(query, (kitapID,))
            return True
        except Exception as e:
            print(f"Kitap silme hatası: {e}")
            return False
    
    @staticmethod
    def get_available_books():
        """Müsait kitapları getirir"""
        #stokta en az bir tne olan kitaplar
        query = """
            SELECT 
                k.kitapID,
                k.baslik,
                k.yazarID,
                k.kategoriID,
                k.yayin_yili,
                k.stok_adedi,
                k.musait_adet,
                COALESCE(y.yazar_ad, '') as yazar_ad,
                COALESCE(y.yazar_soyad, '') as yazar_soyad,
                COALESCE(kat.katagori_adi, '') as katagori_adi
            FROM KITAPLAR k
            LEFT JOIN YAZARLAR y ON k.yazarID = y.yazarID
            LEFT JOIN KATEGORILER kat ON k.kategoriID = kat.kategoriID
            WHERE k.musait_adet > 0
            ORDER BY k.baslik
        """
        try:
            rows = Database.execute_query(query, fetch=True)
            return [dict(row) for row in rows] if rows else []
        except Exception as e:
            print(f"Müsait kitapları getirme hatası: {e}")
            return []