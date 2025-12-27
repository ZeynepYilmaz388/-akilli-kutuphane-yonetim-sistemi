from app.repositories.book_repository import BookRepository
from app.models.book import Book

class BookService:
    
    @staticmethod
    def get_all_books():
        """Tüm kitapları getirir"""
        try:
            books = BookRepository.find_all()
            return {'success': True, 'books': books}
        except Exception as e:
            print(f"Get all books service hatası: {e}")
            return {'success': False, 'message': f'Kitaplar getirilemedi: {str(e)}', 'books': []}
    
    @staticmethod
    def get_book_by_id(kitapID):
        """ID'ye göre kitap getirir"""
        try:
            book = BookRepository.find_by_id(kitapID)
            if book:
                return {'success': True, 'book': book.to_dict()}
            return {'success': False, 'message': 'Kitap bulunamadı!'}
        except Exception as e:
            print(f"Get book by id service hatası: {e}")
            return {'success': False, 'message': f'Kitap getirilemedi: {str(e)}'}
    
    @staticmethod
    def search_books(title):
        """Başlığa göre kitap arar"""
        try:
            books = BookRepository.search_by_title(title)
            return {'success': True, 'books': books}
        except Exception as e:
            print(f"Search books service hatası: {e}")
            return {'success': False, 'message': f'Arama hatası: {str(e)}', 'books': []}
    
    @staticmethod
    def get_available_books():
        """Müsait kitapları getirir"""
        try:
            books = BookRepository.get_available_books()
            return {'success': True, 'books': books}
        except Exception as e:
            print(f"Get available books service hatası: {e}")
            return {'success': False, 'message': f'Kitaplar getirilemedi: {str(e)}', 'books': []}
    
    @staticmethod
    def create_book(baslik, yazarID, kategoriID, yayin_yili, stok_adedi):
        """Yeni kitap ekler"""
        try:
            book = Book(
                baslik=baslik,
                yazarID=yazarID,
                kategoriID=kategoriID,
                yayin_yili=yayin_yili,
                stok_adedi=stok_adedi,
                musait_adet=stok_adedi
            )
            result = BookRepository.create(book)
            if result:
                return {'success': True, 'message': 'Kitap başarıyla eklendi!'}
            else:
                return {'success': False, 'message': 'Kitap eklenemedi!'}
        except Exception as e:
            print(f"Create book service hatası: {e}")
            return {'success': False, 'message': f'Kitap eklenemedi: {str(e)}'}
    
    @staticmethod
    def update_book(kitapID, baslik, yazarID, kategoriID, yayin_yili, stok_adedi, musait_adet):
        """Kitap bilgilerini günceller"""
        try:
            book = Book(
                kitapID=kitapID,
                baslik=baslik,
                yazarID=yazarID,
                kategoriID=kategoriID,
                yayin_yili=yayin_yili,
                stok_adedi=stok_adedi,
                musait_adet=musait_adet
            )
            result = BookRepository.update(kitapID, book)
            if result:
                return {'success': True, 'message': 'Kitap başarıyla güncellendi!'}
            else:
                return {'success': False, 'message': 'Kitap güncellenemedi!'}
        except Exception as e:
            print(f"Update book service hatası: {e}")
            return {'success': False, 'message': f'Kitap güncellenemedi: {str(e)}'}
    
    @staticmethod
    def delete_book(kitapID):
        """Kitap siler"""
        try:
            result = BookRepository.delete(kitapID)
            if result:
                return {'success': True, 'message': 'Kitap başarıyla silindi!'}
            else:
                return {'success': False, 'message': 'Kitap silinemedi!'}
        except Exception as e:
            print(f"Delete book service hatası: {e}")
            return {'success': False, 'message': f'Kitap silinemedi: {str(e)}'}