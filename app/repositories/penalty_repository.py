from app.utils.database import Database
from app.models.penalty import Penalty

class PenaltyRepository:

    @staticmethod
    def create_penalty(oduncID):
        """Gecikmiş ödünç için ceza oluşturur"""
        try:
            query = "SELECT sp_CezaOlustur(%s)"
            Database.execute_query(query, (oduncID,))
            return True
        except Exception as e:
            print(f"Ceza oluşturma hatası: {e}")
            return False

    @staticmethod
    def pay_penalty(cezaID):
        """Cezayı ödenmiş olarak işaretler"""
        try:
            query = "SELECT sp_CezaOde(%s)"
            Database.execute_query(query, (cezaID,))
            return True
        except Exception as e:
            print(f"Ceza ödeme hatası: {e}")
            return False

    @staticmethod
    def check_overdue_loans():
        """Tüm gecikmiş ödünçleri kontrol eder ve ceza oluşturur"""
        try:
            query = "SELECT sp_GecikmisOduncKontrol()"
            Database.execute_query(query)
            return True
        except Exception as e:
            print(f"Gecikmiş ödünç kontrol hatası: {e}")
            return False

    @staticmethod
    def find_by_id(cezaID):
        """ID'ye göre ceza kaydı getirir"""
        query = "SELECT * FROM CEZALAR WHERE cezaID = %s"
        row = Database.execute_query(query, (cezaID,), fetch_one=True)
        return Penalty.from_db_row(row) if row else None

    @staticmethod
    def find_by_user(kullaniciID):
        """Kullanıcının cezalarını getirir"""
        query = """
            SELECT 
                c.cezaID,
                c.oduncID,
                c.kullaniciID,
                c.ceza_tutari,
                c.gecikme_gun,
                c.odenme_durumu,
                c.ceza_tarihi,
                c.odeme_tarihi,
                k.baslik,
                y.yazar_ad || ' ' || y.yazar_soyad AS yazar,
                o.odunc_tarihi,
                o.iade_tarihi
            FROM CEZALAR c
            INNER JOIN ODUNC o ON c.oduncID = o.oduncID
            INNER JOIN KITAPLAR k ON o.kitapID = k.kitapID
            INNER JOIN YAZARLAR y ON k.yazarID = y.yazarID
            WHERE c.kullaniciID = %s
            ORDER BY c.ceza_tarihi DESC
        """
        rows = Database.execute_query(query, (kullaniciID,), fetch=True)
        return rows if rows else []

    @staticmethod
    def find_unpaid_by_user(kullaniciID):
        """Kullanıcının ödenmemiş cezalarını getirir"""
        query = """
            SELECT 
                c.*,
                k.baslik,
                y.yazar_ad || ' ' || y.yazar_soyad AS yazar
            FROM CEZALAR c
            INNER JOIN ODUNC o ON c.oduncID = o.oduncID
            INNER JOIN KITAPLAR k ON o.kitapID = k.kitapID
            INNER JOIN YAZARLAR y ON k.yazarID = y.yazarID
            WHERE c.kullaniciID = %s 
            AND c.odenme_durumu = 'odenmedi'
            ORDER BY c.ceza_tarihi DESC
        """
        rows = Database.execute_query(query, (kullaniciID,), fetch=True)
        return rows if rows else []

    @staticmethod
    def get_total_unpaid(kullaniciID):
        """Kullanıcının toplam ödenmemiş ceza tutarını getirir"""
        query = """
            SELECT COALESCE(SUM(ceza_tutari), 0) as toplam
            FROM CEZALAR
            WHERE kullaniciID = %s AND odenme_durumu = 'odenmedi'
        """
        row = Database.execute_query(query, (kullaniciID,), fetch_one=True)
        return float(row['toplam']) if row else 0.00

    @staticmethod
    def find_all():
        """Tüm cezaları getirir (Admin için)"""
        query = """
            SELECT 
                c.*,
                ku.kullanici_adsoyad,
                ku.kullanici_eposta,
                k.baslik,
                y.yazar_ad || ' ' || y.yazar_soyad AS yazar
            FROM CEZALAR c
            INNER JOIN KULLANICILAR ku ON c.kullaniciID = ku.kullaniciID
            INNER JOIN ODUNC o ON c.oduncID = o.oduncID
            INNER JOIN KITAPLAR k ON o.kitapID = k.kitapID
            INNER JOIN YAZARLAR y ON k.yazarID = y.yazarID
            ORDER BY c.ceza_tarihi DESC
        """
        rows = Database.execute_query(query, fetch=True)
        return rows if rows else []

    @staticmethod
    def find_all_unpaid():
        """Tüm ödenmemiş cezaları getirir (Admin için)"""
        query = """
            SELECT 
                c.*,
                ku.kullanici_adsoyad,
                ku.kullanici_eposta,
                k.baslik,
                y.yazar_ad || ' ' || y.yazar_soyad AS yazar
            FROM CEZALAR c
            INNER JOIN KULLANICILAR ku ON c.kullaniciID = ku.kullaniciID
            INNER JOIN ODUNC o ON c.oduncID = o.oduncID
            INNER JOIN KITAPLAR k ON o.kitapID = k.kitapID
            INNER JOIN YAZARLAR y ON k.yazarID = y.yazarID
            WHERE c.odenme_durumu = 'odenmedi'
            ORDER BY c.ceza_tutari DESC, c.ceza_tarihi DESC
        """
        rows = Database.execute_query(query, fetch=True)
        return rows if rows else []