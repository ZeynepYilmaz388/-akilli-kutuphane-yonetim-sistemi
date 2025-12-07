from app.repositories.loan_repository import LoanRepository
from app.repositories.book_repository import BookRepository

class LoanService:
    
    @staticmethod
    def borrow_book(kitapID, kullaniciID, gun_sayisi=14):
        """Kitap ödünç verir"""
        try:
            # Kitap kontrolü
            book = BookRepository.find_by_id(kitapID)
            if not book:
                return {'success': False, 'message': 'Kitap bulunamadı!'}
            
            if book.musait_adet <= 0:
                return {'success': False, 'message': 'Kitap stokta mevcut değil!'}
            
            # Ödünç ver
            result = LoanRepository.create_loan(kitapID, kullaniciID, gun_sayisi)
            
            if result:
                return {'success': True, 'message': 'Kitap başarıyla ödünç verildi!'}
            else:
                return {'success': False, 'message': 'Ödünç verme işlemi başarısız!'}
        
        except Exception as e:
            return {'success': False, 'message': f'Ödünç verme hatası: {str(e)}'}
    
    @staticmethod
    def return_book(oduncID):
        """Kitap iade eder"""
        try:
            # Ödünç kaydı kontrolü
            loan = LoanRepository.find_by_id(oduncID)
            if not loan:
                return {'success': False, 'message': 'Ödünç kaydı bulunamadı!'}
            
            if loan.durum != 'odunc':
                return {'success': False, 'message': 'Bu kitap zaten iade edilmiş!'}
            
            # İade et
            result = LoanRepository.return_book(oduncID)
            
            if result:
                return {'success': True, 'message': 'Kitap başarıyla iade edildi!'}
            else:
                return {'success': False, 'message': 'İade işlemi başarısız!'}
        
        except Exception as e:
            return {'success': False, 'message': f'İade hatası: {str(e)}'}
    
    @staticmethod
    def get_user_loans(kullaniciID):
        """Kullanıcının ödünç aldığı kitapları getirir"""
        try:
            loans = LoanRepository.find_by_user(kullaniciID)
            return {'success': True, 'loans': loans}
        except Exception as e:
            return {'success': False, 'message': f'Ödünç listesi getirilemedi: {str(e)}'}
    
    @staticmethod
    def get_active_loans(kullaniciID):
        """Kullanıcının aktif ödünç kitaplarını getirir"""
        try:
            loans = LoanRepository.get_active_loans(kullaniciID)
            return {'success': True, 'loans': loans}
        except Exception as e:
            return {'success': False, 'message': f'Aktif ödünçler getirilemedi: {str(e)}'}
    
    @staticmethod
    def get_overdue_loans():
        """Geciken kitapları getirir"""
        try:
            loans = LoanRepository.get_overdue_loans()
            return {'success': True, 'loans': loans}
        except Exception as e:
            return {'success': False, 'message': f'Geciken kitaplar getirilemedi: {str(e)}'}
    
    @staticmethod
    def get_all_loans():
        """Tüm ödünç kayıtlarını getirir"""
        try:
            loans = LoanRepository.find_all()
            return {'success': True, 'loans': loans}
        except Exception as e:
            return {'success': False, 'message': f'Ödünç kayıtları getirilemedi: {str(e)}'}