from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.repositories.category_repository import CategoryRepository
from app.models.category import Category

category_bp = Blueprint('category', __name__, url_prefix='/api/categories')

@category_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_categories():
    """Tüm kategorileri getirir"""
    try:
        categories = CategoryRepository.find_all()
        categories_dict = [category.to_dict() for category in categories]
        return jsonify({'success': True, 'categories': categories_dict}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@category_bp.route('/<int:kategoriID>', methods=['GET'])
@jwt_required()
def get_category(kategoriID):
    """ID'ye göre kategori getirir"""
    try:
        category = CategoryRepository.find_by_id(kategoriID)
        if category:
            return jsonify({'success': True, 'category': category.to_dict()}), 200
        else:
            return jsonify({'success': False, 'message': 'Kategori bulunamadı!'}), 404
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@category_bp.route('/', methods=['POST'])
@jwt_required()
def create_category():
    """Yeni kategori ekler (Sadece admin)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'admin':
            return jsonify({'success': False, 'message': 'Yetkiniz yok!'}), 403
        
        data = request.get_json()
        
        category = Category(
            katagori_adi=data.get('katagori_adi'),
            aciklama=data.get('aciklama')
        )
        
        CategoryRepository.create(category)
        return jsonify({'success': True, 'message': 'Kategori başarıyla eklendi!'}), 201
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@category_bp.route('/<int:kategoriID>', methods=['PUT'])
@jwt_required()
def update_category(kategoriID):
    """Kategori günceller (Sadece admin)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'admin':
            return jsonify({'success': False, 'message': 'Yetkiniz yok!'}), 403
        
        data = request.get_json()
        
        category = Category(
            kategoriID=kategoriID,
            katagori_adi=data.get('katagori_adi'),
            aciklama=data.get('aciklama')
        )
        
        CategoryRepository.update(kategoriID, category)
        return jsonify({'success': True, 'message': 'Kategori başarıyla güncellendi!'}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@category_bp.route('/<int:kategoriID>', methods=['DELETE'])
@jwt_required()
def delete_category(kategoriID):
    """Kategori siler (Sadece admin)"""
    try:
        claims = get_jwt()
        if claims.get('rol') != 'admin':
            return jsonify({'success': False, 'message': 'Yetkiniz yok!'}), 403
        
        CategoryRepository.delete(kategoriID)
        return jsonify({'success': True, 'message': 'Kategori başarıyla silindi!'}), 200
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500