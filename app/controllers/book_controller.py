from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.services.book_service import BookService
from flask_jwt_extended import get_jwt_identity, get_jwt
book_bp = Blueprint('book', __name__, url_prefix='/api/books')

@book_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_books():
    """Tüm kitapları getirir"""
    try:
        result = BookService.get_all_books()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@book_bp.route('/<int:kitapID>', methods=['GET'])
@jwt_required()
def get_book(kitapID):
    """ID'ye göre kitap getirir"""
    try:
        result = BookService.get_book_by_id(kitapID)
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@book_bp.route('/search', methods=['GET'])
@jwt_required()
def search_books():
    """Kitap arama"""
    try:
        title = request.args.get('title', '')
        result = BookService.search_books(title)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@book_bp.route('/available', methods=['GET'])
@jwt_required()
def get_available_books():
    """Müsait kitapları getirir"""
    try:
        result = BookService.get_available_books()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
@book_bp.route('/', methods=['POST'])
@jwt_required()
def create_book():
    """Yeni kitap ekler (Sadece admin)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'admin':
            return jsonify({'success': False, 'message': 'Yetkiniz yok!'}), 403

        data = request.get_json()
        
        #  DEBUG: Gelen veriyi yazdır
        print("=" * 60)
        print("📥 FRONTEND'DEN GELEN VERİ:")
        print(data)
        print("=" * 60)

        baslik = data.get('baslik')
        yazarID = data.get('yazarID')
        kategoriID = data.get('kategoriID')
        yayin_yili = data.get('yayin_yili')
        stok_adedi = data.get('stok_adedi')
        
        #  DEBUG: Her alanı kontrol et
        print(f"baslik: {baslik} (type: {type(baslik)})")
        print(f"yazarID: {yazarID} (type: {type(yazarID)})")
        print(f"kategoriID: {kategoriID} (type: {type(kategoriID)})")
        print(f"yayin_yili: {yayin_yili} (type: {type(yayin_yili)})")
        print(f"stok_adedi: {stok_adedi} (type: {type(stok_adedi)})")
        print("=" * 60)

        if not all([baslik, yazarID, kategoriID, yayin_yili, stok_adedi]):
            print(" HATA: Bazı alanlar boş!")
            print(f"baslik boş mu? {not baslik}")
            print(f"yazarID boş mu? {not yazarID}")
            print(f"kategoriID boş mu? {not kategoriID}")
            print(f"yayin_yili boş mu? {not yayin_yili}")
            print(f"stok_adedi boş mu? {not stok_adedi}")
            return jsonify({'success': False, 'message': 'Tüm alanları doldurun!'}), 400

        result = BookService.create_book(baslik, yazarID, kategoriID, yayin_yili, stok_adedi)

        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400

    except Exception as e:
        print(f" EXCEPTION: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

    
@book_bp.route('/<int:kitapID>', methods=['PUT'])
@jwt_required()
def update_book(kitapID):
    """Kitap günceller (Sadece admin)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'admin':
            return jsonify({'success': False, 'message': 'Yetkiniz yok!'}), 403

        data = request.get_json()
        
        # DEBUG
        print("=" * 60)
        print(f" Kitap güncelleniyor: ID={kitapID}")
        print(f"Gelen veri: {data}")
        print("=" * 60)

        baslik = data.get('baslik')
        yazarID = data.get('yazarID')
        kategoriID = data.get('kategoriID')
        yayin_yili = data.get('yayin_yili')
        stok_adedi = data.get('stok_adedi')

        if not all([baslik, yazarID, kategoriID, yayin_yili, stok_adedi]):
            return jsonify({'success': False, 'message': 'Tüm alanları doldurun!'}), 400

        result = BookService.update_book(kitapID, baslik, yazarID, kategoriID, yayin_yili, stok_adedi, stok_adedi)

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        print(f" Güncelleme hatası: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500                            
@book_bp.route('/<int:kitapID>', methods=['DELETE'])
@jwt_required()
def delete_book(kitapID):
    """Kitap siler (Sadece admin)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'admin':
            return jsonify({'success': False, 'message': 'Yetkiniz yok!'}), 403
        
        result = BookService.delete_book(kitapID)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500                             

@book_bp.route('/', methods=['GET'])
@jwt_required()
def get_books():
    """Tüm kitapları listeler"""
    try:
        # Debug için
        current_user_id = get_jwt_identity()
        jwt_data = get_jwt()
        print(f"User ID: {current_user_id}")  # ← Ekleyin
        print(f"JWT Data: {jwt_data}")  # ← Ekleyin
        
        books = BookService.get_all_books()
        return jsonify({'success': True, 'books': books}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500