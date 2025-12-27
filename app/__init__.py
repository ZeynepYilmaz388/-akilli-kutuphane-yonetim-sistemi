from flask import Flask, render_template, redirect
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config

def create_app():
    # Flask app oluştur
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')
    
    app.config.from_object(Config)
    
    # Extensions
    JWTManager(app)
    Bcrypt(app)
    CORS(app)
    
    # Rate Limiter - IP bazlı istek sınırlama
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,  # IP adresine göre sınırla
        default_limits=["200 per day", "50 per hour"],  # Varsayılan limitler
        storage_uri="memory://",  # Bellekte sakla (küçük projeler için)
    )
    
    # Rate limiter'ı app'e ekle (blueprint'lerde kullanmak için)
    app.limiter = limiter
    
    # Blueprints (API)
    from app.controllers.auth_controller import auth_bp
    from app.controllers.book_controller import book_bp
    from app.controllers.loan_controller import loan_bp
    from app.controllers.author_controller import author_bp
    from app.controllers.category_controller import category_bp
    from app.controllers.penalty_controller import penalty_bp
    from app.controllers.page_controller import page_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(loan_bp)
    app.register_blueprint(author_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(penalty_bp)
    app.register_blueprint(page_bp)
    
    # Frontend Routes
    @app.route('/')
    def index():
        return redirect('/login')
    
    @app.route('/login')
    @limiter.limit("10 per minute")  # Login sayfası: Dakikada 10 erişim
    def login_page():
        return render_template('login.html')
    
    @app.route('/register')
    @limiter.limit("5 per hour")  # Kayıt sayfası: Saatte 5 erişim
    def register_page():
        return render_template('register.html')
    
    @app.route('/dashboard')
    def dashboard_page():
        return render_template('dashboard.html')
    
    @app.route('/profile')
    def profile_page():
        return render_template('profile.html')
    
    @app.route('/my-loans')
    def my_loans_page():
        return render_template('my_loans.html')
    
    @app.route('/penalties')
    def penalties_page():
        return render_template('penalties.html')
    
    @app.route('/admin/books')
    def books_admin_page():
        return render_template('books.html')
    
    @app.route('/admin')
    def admin_page():
        return render_template('admin.html')
    
    @app.route('/health')
    def health():
        return {'status': 'OK', 'message': 'Kütüphane Yönetim Sistemi çalışıyor!'}, 200
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'success': False, 'message': 'Sayfa bulunamadı!'}, 404
    
    @app.errorhandler(429)  # Rate limit aşıldığında
    def ratelimit_handler(e):
        return {
            'success': False, 
            'message': 'Çok fazla istek gönderdiniz! Lütfen bekleyip tekrar deneyin.'
        }, 429
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'success': False, 'message': 'Sunucu hatası!'}, 500
    
    return app