from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.repositories.author_repository import AuthorRepository
from app.models.author import Author

author_bp = Blueprint('author', __name__, url_prefix='/api/authors')

@author_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_authors():
    """Tüm yazarları getirir"""
    try:
        authors = AuthorRepository.find_all()
        authors_dict = [author.to_dict() for author in authors]
        return jsonify({'success': True, 'authors': authors_dict}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@author_bp.route('/<int:yazarID>', methods=['GET'])
@jwt_required()
def get_author(yazarID):
    """ID'ye göre yazar getirir"""
    try:
        author = AuthorRepository.find_by_id(yazarID)
        if author:
            return jsonify({'success': True, 'author': author.to_dict()}), 200
        else:
            return jsonify({'success': False, 'message': 'Yazar bulunamadı!'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@author_bp.route('/', methods=['POST'])
@jwt_required()
def create_author():
    """Yeni yazar ekler (Sadece admin)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'admin':
            return jsonify({'success': False, 'message': 'Yetkiniz yok!'}), 403
        
        data = request.get_json()
        
        author = Author(
            yazar_ad=data.get('yazar_ad'),
            yazar_soyad=data.get('yazar_soyad'),
            yazar_ulke=data.get('yazar_ulke')
        )
        
        AuthorRepository.create(author)
        return jsonify({'success': True, 'message': 'Yazar başarıyla eklendi!'}), 201
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@author_bp.route('/<int:yazarID>', methods=['PUT'])
@jwt_required()
def update_author(yazarID):
    """Yazar günceller (Sadece admin)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'admin':
            return jsonify({'success': False, 'message': 'Yetkiniz yok!'}), 403
        
        data = request.get_json()
        
        author = Author(
            yazarID=yazarID,
            yazar_ad=data.get('yazar_ad'),
            yazar_soyad=data.get('yazar_soyad'),
            yazar_ulke=data.get('yazar_ulke')
        )
        
        AuthorRepository.update(yazarID, author)
        return jsonify({'success': True, 'message': 'Yazar başarıyla güncellendi!'}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@author_bp.route('/<int:yazarID>', methods=['DELETE'])
@jwt_required()
def delete_author(yazarID):
    """Yazar siler (Sadece admin)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'admin':
            return jsonify({'success': False, 'message': 'Yetkiniz yok!'}), 403
        
        AuthorRepository.delete(yazarID)
        return jsonify({'success': True, 'message': 'Yazar başarıyla silindi!'}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500