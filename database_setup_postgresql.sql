-- Veritabanı zaten oluşturuldu (pgAdmin'de)
-- Tabloları oluşturalım

-- KULLANICILAR Tablosu
CREATE TABLE IF NOT EXISTS KULLANICILAR (
    kullaniciID SERIAL PRIMARY KEY,
    kullanici_adsoyad VARCHAR(100) NOT NULL,
    kullanici_sifre VARCHAR(255) NOT NULL,
    kullanici_rol VARCHAR(20) CHECK (kullanici_rol IN ('admin', 'ogrenci', 'personel')) NOT NULL,
    kullanici_eposta VARCHAR(100) UNIQUE NOT NULL,
    kayit_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- YAZARLAR Tablosu
CREATE TABLE IF NOT EXISTS YAZARLAR (
    yazarID SERIAL PRIMARY KEY,
    yazar_ad VARCHAR(50) NOT NULL,
    yazar_soyad VARCHAR(50) NOT NULL,
    yazar_ulke VARCHAR(50)
);

-- KATEGORILER Tablosu
CREATE TABLE IF NOT EXISTS KATEGORILER (
    kategoriID SERIAL PRIMARY KEY,
    katagori_adi VARCHAR(50) NOT NULL,
    aciklama VARCHAR(255)
);

-- KITAPLAR Tablosu
CREATE TABLE IF NOT EXISTS KITAPLAR (
    kitapID SERIAL PRIMARY KEY,
    baslik VARCHAR(200) NOT NULL,
    yazarID INTEGER REFERENCES YAZARLAR(yazarID),
    kategoriID INTEGER REFERENCES KATEGORILER(kategoriID),
    yayin_yili INTEGER,
    stok_adedi INTEGER DEFAULT 0,
    musait_adet INTEGER DEFAULT 0
);

-- ODUNC Tablosu
CREATE TABLE IF NOT EXISTS ODUNC (
    oduncID SERIAL PRIMARY KEY,
    kitapID INTEGER REFERENCES KITAPLAR(kitapID),
    kullaniciID INTEGER REFERENCES KULLANICILAR(kullaniciID),
    odunc_tarihi TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    iade_tarihi TIMESTAMP,
    gercek_iade_tarihi TIMESTAMP,
    durum VARCHAR(20) CHECK (durum IN ('odunc', 'iade', 'gecikme')) DEFAULT 'odunc'
);

-- CEZA Tablosu
CREATE TABLE IF NOT EXISTS CEZA (
    cezaID SERIAL PRIMARY KEY,
    oduncID INTEGER REFERENCES ODUNC(oduncID),
    kullaniciID INTEGER REFERENCES KULLANICILAR(kullaniciID),
    gun_sayisi INTEGER,
    ceza_tutari DECIMAL(10,2),
    odenme_durumu VARCHAR(20) CHECK (odenme_durumu IN ('odenmedi', 'odendi')) DEFAULT 'odenmedi'
);

-- Örnek Veri Ekleme
-- Admin kullanıcı (şifre: admin123)
INSERT INTO KULLANICILAR (kullanici_adsoyad, kullanici_sifre, kullanici_rol, kullanici_eposta)
VALUES ('Admin User', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ux7qRgVEpz7G', 'admin', 'admin@kutuphane.com')
ON CONFLICT (kullanici_eposta) DO NOTHING;

-- Örnek Öğrenci (şifre: ogrenci123)
INSERT INTO KULLANICILAR (kullanici_adsoyad, kullanici_sifre, kullanici_rol, kullanici_eposta)
VALUES ('Zeynep Yılmaz', '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'ogrenci', 'zeynep@ogrenci.com')
ON CONFLICT (kullanici_eposta) DO NOTHING;

-- Örnek Yazarlar
INSERT INTO YAZARLAR (yazar_ad, yazar_soyad, yazar_ulke) VALUES
('Orhan', 'Pamuk', 'Türkiye'),
('Elif', 'Şafak', 'Türkiye'),
('Sabahattin', 'Ali', 'Türkiye'),
('Yaşar', 'Kemal', 'Türkiye');

-- Örnek Kategoriler
INSERT INTO KATEGORILER (katagori_adi, aciklama) VALUES
('Roman', 'Roman türü eserler'),
('Bilim Kurgu', 'Bilim kurgu türü eserler'),
('Tarih', 'Tarih konulu kitaplar'),
('Şiir', 'Şiir kitapları');

-- Örnek Kitaplar
INSERT INTO KITAPLAR (baslik, yazarID, kategoriID, yayin_yili, stok_adedi, musait_adet) VALUES
('Kar', 1, 1, 2002, 5, 5),
('Masumiyet Müzesi', 1, 1, 2008, 3, 3),
('Aşk', 2, 1, 2009, 4, 4),
('Kürk Mantolu Madonna', 3, 1, 1943, 6, 6),
('İnce Memed', 4, 1, 1955, 5, 5);