from flask import Blueprint, render_template

page_bp = Blueprint('page', __name__)

@page_bp.route('/profile')
def profile():
    """Kullanıcı profil sayfası"""
    return render_template('profile.html')

@page_bp.route('/register')
def register():
    """Kayıt sayfası"""
    return render_template('register.html')