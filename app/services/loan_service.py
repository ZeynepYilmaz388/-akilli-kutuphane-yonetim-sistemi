from app.repositories.loan_repository import LoanRepository
from app.repositories.book_repository import BookRepository

class LoanService:
    @staticmethod
    def borrow_book(kitapID, kullaniciID, dakika_sayisi=1):
        """Kitap ödünç verir"""
        try:
            # Kitap kontrolü
            book = BookRepository.find_by_id(kitapID)
            if not book:
                return {'success': False, 'message': 'Kitap bulunamadı!'}

            if book.musait_adet <= 0:
                return {'success': False, 'message': 'Kitap stokta mevcut değil!'}

            # Ödünç ver
            result = LoanRepository.create_loan(kitapID, kullaniciID, dakika_sayisi)

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
            rows = LoanRepository.find_by_user(kullaniciID)
            
            loans_list = []
            for row in rows:
                loan_dict = {
                    'oduncid': row.get('oduncid'),
                    'baslik': row.get('baslik'),
                    'yazar': row.get('yazar'),
                    'odunc_tarihi': row['odunc_tarihi'].strftime('%d.%m.%Y %H:%M') if row.get('odunc_tarihi') else None,
                    'iade_tarihi': row['iade_tarihi'].strftime('%d.%m.%Y %H:%M') if row.get('iade_tarihi') else None,
                    'gercek_iade_tarihi': row['gercek_iade_tarihi'].strftime('%d.%m.%Y %H:%M') if row.get('gercek_iade_tarihi') else None,
                    'durum': row.get('durum'),
                    'gecikme_gun': int(row.get('gecikme_gun', 0))
                }
                loans_list.append(loan_dict)
            
            return {'success': True, 'loans': loans_list}
        except Exception as e:
            print(f" User loans error: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'success': False, 'message': f'Ödünç listesi getirilemedi: {str(e)}'}

    @staticmethod
    def get_active_loans(kullaniciID):
        """Kullanıcının aktif ödünç kitaplarını getirir"""
        try:
            rows = LoanRepository.get_active_loans(kullaniciID)
            
            loans_list = []
            for row in rows:
                # PostgreSQL küçük harf döndürüyor: oduncid, kitapid, kullaniciid
                loan_dict = {
                    'oduncid': row.get('oduncid'),
                    'kullaniciid': row.get('kullaniciid'),
                    'kitapid': row.get('kitapid'),
                    'odunc_tarihi': row['odunc_tarihi'].strftime('%d.%m.%Y %H:%M') if row.get('odunc_tarihi') else None,
                    'iade_tarihi': row['iade_tarihi'].strftime('%d.%m.%Y %H:%M') if row.get('iade_tarihi') else None,
                    'gercek_iade_tarihi': row['gercek_iade_tarihi'].strftime('%d.%m.%Y %H:%M') if row.get('gercek_iade_tarihi') else None,
                    'durum': row.get('durum'),
                    'baslik': row.get('baslik'),
                    'yazar_ad': row.get('yazar_ad'),
                    'yazar_soyad': row.get('yazar_soyad')
                }
                loans_list.append(loan_dict)
            
            return {'success': True, 'loans': loans_list}
        except Exception as e:
            print(f" Active loans error: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'success': False, 'message': f'Aktif ödünçler getirilemedi: {str(e)}'}

    @staticmethod
    def get_returned_loans(kullaniciID):
        """Kullanıcının iade ettiği kitapları getirir"""
        try:
            rows = LoanRepository.get_returned_loans(kullaniciID)
            
            loans_list = []
            for row in rows:
                loan_dict = {
                    'oduncid': row.get('oduncid'),
                    'kullaniciid': row.get('kullaniciid'),
                    'kitapid': row.get('kitapid'),
                    'odunc_tarihi': row['odunc_tarihi'].strftime('%d.%m.%Y %H:%M') if row.get('odunc_tarihi') else None,
                    'iade_tarihi': row['iade_tarihi'].strftime('%d.%m.%Y %H:%M') if row.get('iade_tarihi') else None,
                    'gercek_iade_tarihi': row['gercek_iade_tarihi'].strftime('%d.%m.%Y %H:%M') if row.get('gercek_iade_tarihi') else None,
                    'durum': row.get('durum'),
                    'baslik': row.get('baslik'),
                    'yazar_ad': row.get('yazar_ad'),
                    'yazar_soyad': row.get('yazar_soyad')
                }
                loans_list.append(loan_dict)
            
            return {'success': True, 'loans': loans_list}
        except Exception as e:
            print(f" Returned loans error: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'success': False, 'message': f'İade edilenler getirilemedi: {str(e)}'}

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