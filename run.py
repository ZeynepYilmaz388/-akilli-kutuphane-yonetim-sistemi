from app import create_app
#uygulamanın giriş noktası flesk serverını baslatır
app = create_app()

if __name__ == '__main__':
    print("=" * 50)
    print(" Kütüphane Yönetim Sistemi")
    print("=" * 50)
    print("API: http://localhost:5000")
    print("\n Test Kullanıcıları:")
    print("   Admin: admin@kutuphane.com / admin123")
    print("   Öğrenci: zeynep@ogrenci.com / ogrenci123")
    print("=" * 50)
    
    app.run(debug=True, port=5000)