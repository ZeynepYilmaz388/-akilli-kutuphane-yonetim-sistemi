from app.utils.database import Database
from app.models.author import Author

class AuthorRepository:
    #bu sınıf yazarlar ile ilgili tüm veri tabanı işlemlerini yapar
    @staticmethod
    def create(author):
        """Yeni yazar ekler"""
        #SQL INSERT sorgusu hazırlanıyor.%s → parametre yeri (güvenli, injection yok)
        query = """
            INSERT INTO YAZARLAR (yazar_ad, yazar_soyad, yazar_ulke)
            VALUES (%s, %s, %s)
        """
        params = (author.yazar_ad, author.yazar_soyad, author.yazar_ulke)
        #Author nesnesinin içinden değerler alınıyor .SQL’deki %s’lere sırayla yerleştirilecek
        Database.execute_query(query, params)
        #sorgu database sınıfına gonderiliyor. bağlantı ,commint vs işlemler orada yapılıyor
        return True
    
    @staticmethod
    def find_by_id(yazarID):
        """ID'ye göre yazar getirir"""
        query = "SELECT * FROM YAZARLAR WHERE yazarID = %s"
        #ID’ye göre tek yazar arayan SQL yazılıyor
        row = Database.execute_query(query, (yazarID,), fetch_one=True)
        #sorgu calısısyor ve tek satır döndürüyor
        return Author.from_db_row(row) if row else None
    
    @staticmethod
    def find_all():
        """Tüm yazarları getirir"""
        query = "SELECT * FROM YAZARLAR ORDER BY yazar_soyad, yazar_ad"
        #tum yazalarlar getiriliyor ve soyad ada göre sıralanıyor
        rows = Database.execute_query(query, fetch=True)
        #birden fazla satır döndürüyor
        return [Author.from_db_row(row) for row in rows] if rows else []
    # her satır için from_db_row metodu çağrılıyor ve Author nesnesi oluşturuluyor
    @staticmethod
    def search_by_name(name):
        """İsme göre yazar arar"""
        query = """
            SELECT * FROM YAZARLAR 
            WHERE yazar_ad ILIKE %s OR yazar_soyad ILIKE %s
            ORDER BY yazar_soyad, yazar_ad
        """
        #ılıke ile arama yapılıyor (büyük küçük harf duyarsız)
        rows = Database.execute_query(query, (f'%{name}%', f'%{name}%'), fetch=True)
        return [Author.from_db_row(row) for row in rows] if rows else []
    # her satır için from_db_row metodu çağrılıyor ve Author nesnesi oluşturuluyor
    
    @staticmethod
    def update(yazarID, author):
        """Yazar bilgilerini günceller"""
        query = """
            UPDATE YAZARLAR 
            SET yazar_ad = %s, yazar_soyad = %s, yazar_ulke = %s
            WHERE yazarID = %s
        """
        #Belirli ID’ye sahip yazar güncelleniyor
        params = (author.yazar_ad, author.yazar_soyad, author.yazar_ulke, yazarID)
        #yeni biligler veritabanına yazılıyor
        Database.execute_query(query, params)
        return True
    
    @staticmethod
    def delete(yazarID):
        """Yazar siler"""
        query = "DELETE FROM YAZARLAR WHERE yazarID = %s"
        # yazarID’ye göre yazar siliniyor
        Database.execute_query(query, (yazarID,))
        return True