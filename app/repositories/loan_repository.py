from app.utils.database import Database
from app.models.loan import Loan

class LoanRepository:
    
    @staticmethod
    def create_loan(kitapID, kullaniciID, gun_sayisi=14):
        """Stored Procedure kullanarak kitap ödünç verir"""
        try:
            Database.execute_stored_procedure('sp_OduncVer', (kitapID, kullaniciID, gun_sayisi))
            return True
        except Exception as e:
            print(f"Ödünç verme hatası: {e}")
            return False
    
    @staticmethod
    def return_book(oduncID):
        """Stored Procedure kullanarak kitap iade eder"""
        try:
            Database.execute_stored_procedure('sp_KitapIade', (oduncID,))
            return True
        except Exception as e:
            print(f"İade hatası: {e}")
            return False
    
    @staticmethod
    def find_by_id(oduncID):
        """ID'ye göre ödünç kaydı getirir"""
        query = "SELECT * FROM ODUNC WHERE oduncID = ?"
        row = Database.execute_query(query, (oduncID,), fetch_one=True)
        return Loan.from_db_row(row) if row else None
    
    @staticmethod
    def find_by_user(kullaniciID):
        """Kullanıcının ödünç aldığı kitapları getirir"""
        try:
            rows = Database.execute_stored_procedure('sp_KullaniciOduncListesi', (kullaniciID,))
            return rows if rows else []
        except Exception as e:
            print(f"Kullanıcı ödünç listesi hatası: {e}")
            return []
    
    @staticmethod
    def get_active_loans(kullaniciID):
        """Kullanıcının aktif ödünç kitaplarını getirir"""
        query = """
            SELECT o.*, k.baslik, y.yazar_ad, y.yazar_soyad
            FROM ODUNC o
            INNER JOIN KITAPLAR k ON o.kitapID = k.kitapID
            INNER JOIN YAZARLAR y ON k.yazarID = y.yazarID
            WHERE o.kullaniciID = ? AND o.durum = 'odunc'
            ORDER BY o.iade_tarihi
        """
        rows = Database.execute_query(query, (kullaniciID,), fetch=True)
        return rows if rows else []
    
    @staticmethod
    def get_overdue_loans():
        """Geciken kitapları getirir"""
        try:
            rows = Database.execute_stored_procedure('sp_GecikenKitaplar')
            return rows if rows else []
        except Exception as e:
            print(f"Geciken kitaplar hatası: {e}")
            return []
    
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
            WHERE o.kullaniciID = ?
            ORDER BY o.odunc_tarihi DESC
        """
        rows = Database.execute_query(query, (kullaniciID,), fetch=True)
        return rows if rows else []