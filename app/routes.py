from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from app.models import User, Book, Loan
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from functools import wraps

# Login Required Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Bu sayfayı görüntülemek için giriş yapmalısınız!', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# 🏠 ANA SAYFA - Otomatik yönlendirme
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('books'))
    return redirect(url_for('login'))

# 🔐 GİRİŞ YAP
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            flash(f'Hoşgeldiniz {user.username}!', 'success')
            return redirect(url_for('books'))
        else:
            flash('❌ Kullanıcı adı veya şifre hatalı!', 'danger')
    
    return render_template('login.html')

# 📝 KAYIT OL
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone', '')
        
        # Kullanıcı adı kontrolü
        if User.query.filter_by(username=username).first():
            flash('❌ Bu kullanıcı adı zaten alınmış!', 'danger')
            return redirect(url_for('register'))
        
        # Email kontrolü
        if User.query.filter_by(email=email).first():
            flash('❌ Bu e-posta adresi zaten kayıtlı!', 'danger')
            return redirect(url_for('register'))
        
        # Yeni kullanıcı oluştur
        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            full_name=full_name,
            phone=phone
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('✅ Kayıt başarılı! Şimdi giriş yapabilirsiniz.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

# 📚 KİTAPLAR LİSTESİ (Ana Sayfa)
@app.route('/books')
@login_required
def books():
    all_books = Book.query.all()
    
    # Kullanıcının aktif ödünç sayısı
    user_loans_count = Loan.query.filter_by(
        user_id=session['user_id'], 
        returned=False
    ).count()
    
    return render_template('books.html', 
                         books=all_books, 
                         user_loans_count=user_loans_count)

# 📖 KİTAP ÖDÜNÇ AL
@app.route('/borrow/<int:book_id>', methods=['POST'])
@login_required
def borrow_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    # Kitap müsait mi?
    if not book.available:
        flash('❌ Bu kitap şu an müsait değil!', 'danger')
        return redirect(url_for('books'))
    
    # Kullanıcı bu kitabı zaten ödünç almış mı?
    existing_loan = Loan.query.filter_by(
        user_id=session['user_id'],
        book_id=book_id,
        returned=False
    ).first()
    
    if existing_loan:
        flash('⚠️ Bu kitabı zaten ödünç almışsınız!', 'warning')
        return redirect(url_for('books'))
    
    # Kullanıcının aktif ödünç sayısı kontrolü (Max 3)
    active_loans = Loan.query.filter_by(
        user_id=session['user_id'], 
        returned=False
    ).count()
    
    if active_loans >= 3:
        flash('⚠️ Aynı anda en fazla 3 kitap ödünç alabilirsiniz!', 'warning')
        return redirect(url_for('books'))
    
    # Ödünç kaydı oluştur
    new_loan = Loan(
        user_id=session['user_id'],
        book_id=book_id,
        borrow_date=datetime.now(),
        due_date=datetime.now() + timedelta(days=14)  # 14 gün süre
    )
    
    book.available = False
    
    db.session.add(new_loan)
    db.session.commit()
    
    flash(f'✅ "{book.title}" kitabı başarıyla ödünç alındı! İade tarihi: {new_loan.due_date.strftime("%d.%m.%Y")}', 'success')
    return redirect(url_for('books'))

# 📑 ÖDÜNÇ ALDIKLARIM
@app.route('/my-loans')
@login_required
def my_loans():
    # Kullanıcının tüm ödünç kayıtları (en yeni üstte)
    user_loans = Loan.query.filter_by(
        user_id=session['user_id']
    ).order_by(Loan.borrow_date.desc()).all()
    
    return render_template('my_loans.html', loans=user_loans)

# 🔄 KİTAP İADE ET
@app.route('/return/<int:loan_id>', methods=['POST'])
@login_required
def return_book(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    
    # Kullanıcı kontrolü
    if loan.user_id != session['user_id']:
        flash('❌ Bu işlem için yetkiniz yok!', 'danger')
        return redirect(url_for('my_loans'))
    
    # Zaten iade edilmiş mi?
    if loan.returned:
        flash('⚠️ Bu kitap zaten iade edilmiş!', 'warning')
        return redirect(url_for('my_loans'))
    
    # İade işlemi
    loan.returned = True
    loan.return_date = datetime.now()
    loan.book.available = True
    
    db.session.commit()
    
    flash(f'✅ "{loan.book.title}" kitabı başarıyla iade edildi!', 'success')
    return redirect(url_for('my_loans'))

# 🚪 ÇIKIŞ YAP
@app.route('/logout')
def logout():
    username = session.get('username', 'Kullanıcı')
    session.clear()
    flash(f'👋 Görüşürüz {username}!', 'info')
    return redirect(url_for('login'))

# 🔍 KİTAP ARAMA (Bonus)
@app.route('/search')
@login_required
def search():
    query = request.args.get('q', '')
    
    if query:
        books = Book.query.filter(
            (Book.title.ilike(f'%{query}%')) | 
            (Book.author.ilike(f'%{query}%')) |
            (Book.category.ilike(f'%{query}%'))
        ).all()
    else:
        books = Book.query.all()
    
    return render_template('books.html', books=books, search_query=query)