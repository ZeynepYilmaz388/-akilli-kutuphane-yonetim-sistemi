from app.utils.database import Database
from app.models.loan import Loan

class LoanRepository:
    
    @staticmethod
    def create_loan(kitapID, kullaniciID, dakika_sayisi=1):
        """Function kullanarak kitap ödünç verir"""
        try:
            query = "SELECT sp_OduncVer(%s, %s, %s)"
            Database.execute_query(query, (kitapID, kullaniciID, dakika_sayisi))
            return True
        except Exception as e:
            print(f" Ödünç verme hatası: {e}")
            return False
    
    @staticmethod
    def return_book(oduncID):
        """Function kullanarak kitap iade eder"""
        try:
            query = "SELECT sp_KitapIade(%s)"
            Database.execute_query(query, (oduncID,))
            return True
        except Exception as e:
            print(f" İade hatası: {e}")
            return False
    
    @staticmethod
    def find_by_id(oduncID):
        """ID'ye göre ödünç kaydı getirir"""
        query = "SELECT * FROM ODUNC WHERE oduncID = %s"
        row = Database.execute_query(query, (oduncID,), fetch_one=True)
        return Loan.from_db_row(row) if row else None
    
    @staticmethod
    def find_by_user(kullaniciID):
        """Kullanıcının ödünç aldığı kitapları getirir"""
        query = """
            SELECT 
                o.oduncID,
                k.baslik,
                y.yazar_ad || ' ' || y.yazar_soyad AS yazar,
                o.odunc_tarihi,
                o.iade_tarihi,
                o.gercek_iade_tarihi,
                o.durum,
                CASE 
                    WHEN o.durum = 'odunc' AND CURRENT_TIMESTAMP > o.iade_tarihi 
                    THEN EXTRACT(DAY FROM (CURRENT_TIMESTAMP - o.iade_tarihi))
                    ELSE 0 
                END AS gecikme_gun
            FROM ODUNC o
            INNER JOIN KITAPLAR k ON o.kitapID = k.kitapID
            INNER JOIN YAZARLAR y ON k.yazarID = y.yazarID
            WHERE o.kullaniciID = %s
            ORDER BY o.odunc_tarihi DESC
        """
        rows = Database.execute_query(query, (kullaniciID,), fetch=True)
        return rows if rows else []
    
    @staticmethod
    def get_active_loans(kullaniciID):
        """Kullanıcının aktif ödünç kitaplarını getirir"""
        query = """
            SELECT 
                o.oduncID,
                o.kullaniciID,
                o.kitapID,
                o.odunc_tarihi,
                o.iade_tarihi,
                o.gercek_iade_tarihi,
                o.durum,
                k.baslik,
                y.yazar_ad,
                y.yazar_soyad
            FROM ODUNC o
            INNER JOIN KITAPLAR k ON o.kitapID = k.kitapID
            INNER JOIN YAZARLAR y ON k.yazarID = y.yazarID
            WHERE o.kullaniciID = %s AND o.durum = 'odunc'
            ORDER BY o.iade_tarihi ASC
        """
        rows = Database.execute_query(query, (kullaniciID,), fetch=True)
        return rows if rows else []
    
    @staticmethod
    def get_returned_loans(kullaniciID):
        """Kullanıcının iade ettiği kitapları getirir"""
        query = """
            SELECT 
                o.oduncID,
                o.kullaniciID,
                o.kitapID,
                o.odunc_tarihi,
                o.iade_tarihi,
                o.gercek_iade_tarihi,
                o.durum,
                k.baslik,
                y.yazar_ad,
                y.yazar_soyad
            FROM ODUNC o
            INNER JOIN KITAPLAR k ON o.kitapID = k.kitapID
            INNER JOIN YAZARLAR y ON k.yazarID = y.yazarID
            WHERE o.kullaniciID = %s AND o.durum = 'iade'
            ORDER BY o.gercek_iade_tarihi DESC
        """
        rows = Database.execute_query(query, (kullaniciID,), fetch=True)
        return rows if rows else []
    
    @staticmethod
    def get_overdue_loans():
        """Geciken kitapları getirir"""
        query = """
            SELECT 
                o.oduncID,
                ku.kullanici_adsoyad,
                ku.kullanici_eposta,
                k.baslik,
                o.odunc_tarihi,
                o.iade_tarihi,
                EXTRACT(DAY FROM (CURRENT_TIMESTAMP - o.iade_tarihi)) AS gecikme_gun
            FROM ODUNC o
            INNER JOIN KULLANICILAR ku ON o.kullaniciID = ku.kullaniciID
            INNER JOIN KITAPLAR k ON o.kitapID = k.kitapID
            WHERE o.durum = 'odunc' 
              AND CURRENT_TIMESTAMP > o.iade_tarihi
            ORDER BY gecikme_gun DESC
        """
        rows = Database.execute_query(query, fetch=True)
        return rows if rows else []
    
    @staticmethod
    def find_all():
        """Tüm ödünç kayıtlarını getirir"""
        query = """
            SELECT o.*, k.baslik, u.kullanici_adsoyad
            FROM ODUNC o
            INNER JOIN KITAPLAR k ON o.kitapID = k.kitapID
            INNER JOIN KULLANICILAR u ON o.kullaniciID = u.kullaniciID
            ORDER BY o.odunc_tarihi DESC
        """
        rows = Database.execute_query(query, fetch=True)
        return rows if rows else []
    
    @staticmethod
    def get_loan_history(kullaniciID):
        """Kullanıcının tüm ödünç geçmişini getirir"""
        query = """
            SELECT o.*, k.baslik, y.yazar_ad, y.yazar_soyad
            FROM ODUNC o
            INNER JOIN KITAPLAR k ON o.kitapID = k.kitapID
            INNER JOIN YAZARLAR y ON k.yazarID = y.yazarID
            WHERE o.kullaniciID = %s
            ORDER BY o.odunc_tarihi DESC
        """
        rows = Database.execute_query(query, (kullaniciID,), fetch=True)
        return rows if rows else []