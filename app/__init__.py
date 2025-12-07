from flask import Flask, render_template, redirect
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Extensions
    JWTManager(app)
    Bcrypt(app)
    CORS(app)
    
    # Blueprints (API)
    from app.controllers.auth_controller import auth_bp
    from app.controllers.book_controller import book_bp
    from app.controllers.loan_controller import loan_bp
    from app.controllers.author_controller import author_bp
    from app.controllers.category_controller import category_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(book_bp)
    app.register_blueprint(loan_bp)
    app.register_blueprint(author_bp)
    app.register_blueprint(category_bp)
    
    # Frontend Routes
    @app.route('/')
    def index():
        return redirect('/login')
    
    @app.route('/login')
    def login_page():
        return render_template('login.html')
    
    @app.route('/dashboard')
    def dashboard_page():
        return render_template('dashboard.html')
    
    @app.route('/my-loans')
    def my_loans_page():
        return render_template('my_loans.html')
    
    @app.route('/admin/books')
    def books_admin_page():
        return render_template('books.html')
    
    @app.route('/health')
    def health():
        return {'status': 'OK'}, 200
    
    return app