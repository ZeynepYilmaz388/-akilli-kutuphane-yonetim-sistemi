from app.repositories.penalty_repository import PenaltyRepository

class PenaltyService:

    @staticmethod
    def get_user_penalties(kullaniciID):
        """Kullanıcının tüm cezalarını getirir"""
        try:
            penalties = PenaltyRepository.find_by_user(kullaniciID)
            return {
                'success': True,
                'penalties': penalties
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Cezalar getirilemedi: {str(e)}'
            }

    @staticmethod
    def get_unpaid_penalties(kullaniciID):
        """Kullanıcının ödenmemiş cezalarını getirir"""
        try:
            penalties = PenaltyRepository.find_unpaid_by_user(kullaniciID)
            total = PenaltyRepository.get_total_unpaid(kullaniciID)
            
            return {
                'success': True,
                'penalties': penalties,
                'total_unpaid': total
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Ödenmemiş cezalar getirilemedi: {str(e)}'
            }

    @staticmethod
    def pay_penalty(cezaID):
        """Cezayı öder"""
        try:
            penalty = PenaltyRepository.find_by_id(cezaID)
            
            if not penalty:
                return {
                    'success': False,
                    'message': 'Ceza bulunamadı!'
                }
            
            if penalty.odenme_durumu == 'odendi':
                return {
                    'success': False,
                    'message': 'Bu ceza zaten ödenmiş!'
                }
            
            result = PenaltyRepository.pay_penalty(cezaID)
            
            if result:
                return {
                    'success': True,
                    'message': 'Ceza başarıyla ödendi!'
                }
            else:
                return {
                    'success': False,
                    'message': 'Ceza ödenirken bir hata oluştu!'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Ceza ödeme hatası: {str(e)}'
            }

    @staticmethod
    def check_overdue_and_create_penalties():
        """Gecikmiş ödünçleri kontrol eder ve ceza oluşturur"""
        try:
            result = PenaltyRepository.check_overdue_loans()
            
            if result:
                return {
                    'success': True,
                    'message': 'Gecikmiş ödünçler kontrol edildi ve cezalar oluşturuldu!'
                }
            else:
                return {
                    'success': False,
                    'message': 'Kontrol sırasında bir hata oluştu!'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Kontrol hatası: {str(e)}'
            }

    @staticmethod
    def get_all_penalties():
        """Tüm cezaları getirir (Admin)"""
        try:
            penalties = PenaltyRepository.find_all()
            return {
                'success': True,
                'penalties': penalties
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Cezalar getirilemedi: {str(e)}'
            }

    @staticmethod
    def get_all_unpaid_penalties():
        """Tüm ödenmemiş cezaları getirir (Admin)"""
        try:
            penalties = PenaltyRepository.find_all_unpaid()
            return {
                'success': True,
                'penalties': penalties
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Ödenmemiş cezalar getirilemedi: {str(e)}'
            }