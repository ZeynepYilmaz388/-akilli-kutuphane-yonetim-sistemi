-- ================================================
-- AKILLI KÜTÜPHANE YÖNETİM SİSTEMİ
-- Tam Veritabanı Kurulum Scripti
-- ================================================
-- Yazar: Zeynep
-- Tarih: Aralık 2025
-- Veritabanı: PostgreSQL 18
-- ================================================

-- VeritabanÄ± zaten oluÅŸturuldu (pgAdmin'de)
-- TablolarÄ± oluÅŸturalÄ±m

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

-- Ã–rnek Veri Ekleme
-- Admin kullanÄ±cÄ± (ÅŸifre: admin123)
INSERT INTO KULLANICILAR (kullanici_adsoyad, kullanici_sifre, kullanici_rol, kullanici_eposta)
VALUES ('Admin User', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5ux7qRgVEpz7G', 'admin', 'admin@kutuphane.com')
ON CONFLICT (kullanici_eposta) DO NOTHING;

-- Ã–rnek Ã–ÄŸrenci (ÅŸifre: ogrenci123)
INSERT INTO KULLANICILAR (kullanici_adsoyad, kullanici_sifre, kullanici_rol, kullanici_eposta)
VALUES ('Zeynep YÄ±lmaz', '$2b$12$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'ogrenci', 'zeynep@ogrenci.com')
ON CONFLICT (kullanici_eposta) DO NOTHING;

-- Ã–rnek Yazarlar
INSERT INTO YAZARLAR (yazar_ad, yazar_soyad, yazar_ulke) VALUES
('Orhan', 'Pamuk', 'TÃ¼rkiye'),
('Elif', 'Åafak', 'TÃ¼rkiye'),
('Sabahattin', 'Ali', 'TÃ¼rkiye'),
('YaÅŸar', 'Kemal', 'TÃ¼rkiye');

-- Ã–rnek Kategoriler
INSERT INTO KATEGORILER (katagori_adi, aciklama) VALUES
('Roman', 'Roman tÃ¼rÃ¼ eserler'),
('Bilim Kurgu', 'Bilim kurgu tÃ¼rÃ¼ eserler'),
('Tarih', 'Tarih konulu kitaplar'),
('Åiir', 'Åiir kitaplarÄ±');

-- Ã–rnek Kitaplar
INSERT INTO KITAPLAR (baslik, yazarID, kategoriID, yayin_yili, stok_adedi, musait_adet) VALUES
('Kar', 1, 1, 2002, 5, 5),
('Masumiyet MÃ¼zesi', 1, 1, 2008, 3, 3),
('AÅŸk', 2, 1, 2009, 4, 4),
('KÃ¼rk Mantolu Madonna', 3, 1, 1943, 6, 6),
('Ä°nce Memed', 4, 1, 1955, 5, 5);

-- ================================================
-- STORED PROCEDURES
-- ================================================
-- 1. Kitap Ã–dÃ¼nÃ§ Verme Function
CREATE OR REPLACE FUNCTION sp_OduncVer(
    p_kitapID INTEGER,
    p_kullaniciID INTEGER,
    p_gun_sayisi INTEGER DEFAULT 14
)
RETURNS VOID AS $$
DECLARE
    v_musait_adet INTEGER;
    v_iade_tarihi TIMESTAMP;
BEGIN
    SELECT musait_adet INTO v_musait_adet FROM KITAPLAR WHERE kitapID = p_kitapID;
    
    IF v_musait_adet > 0 THEN
        v_iade_tarihi := CURRENT_TIMESTAMP + (p_gun_sayisi || ' days')::INTERVAL;
        
        INSERT INTO ODUNC (kitapID, kullaniciID, odunc_tarihi, iade_tarihi, durum)
        VALUES (p_kitapID, p_kullaniciID, CURRENT_TIMESTAMP, v_iade_tarihi, 'odunc');
        
        UPDATE KITAPLAR SET musait_adet = musait_adet - 1 WHERE kitapID = p_kitapID;
        
        RAISE NOTICE 'Kitap baÅŸarÄ±yla Ã¶dÃ¼nÃ§ verildi.';
    ELSE
        RAISE EXCEPTION 'Kitap stokta mevcut deÄŸil!';
    END IF;
END;
$$ LANGUAGE plpgsql;

-- 2. Kitap Ä°ade Function
CREATE OR REPLACE FUNCTION sp_KitapIade(p_oduncID INTEGER)
RETURNS VOID AS $$
DECLARE
    v_kitapID INTEGER;
    v_iade_tarihi TIMESTAMP;
    v_gercek_iade_tarihi TIMESTAMP := CURRENT_TIMESTAMP;
    v_gun_fark INTEGER;
    v_kullaniciID INTEGER;
BEGIN
    SELECT kitapID, iade_tarihi, kullaniciID 
    INTO v_kitapID, v_iade_tarihi, v_kullaniciID
    FROM ODUNC WHERE oduncID = p_oduncID;
    
    v_gun_fark := EXTRACT(DAY FROM (v_gercek_iade_tarihi - v_iade_tarihi));
    
    IF v_gun_fark > 0 THEN
        INSERT INTO CEZA (oduncID, kullaniciID, gun_sayisi, ceza_tutari, odenme_durumu)
        VALUES (p_oduncID, v_kullaniciID, v_gun_fark, v_gun_fark * 2.00, 'odenmedi');
        
        UPDATE ODUNC SET gercek_iade_tarihi = v_gercek_iade_tarihi, durum = 'gecikme'
        WHERE oduncID = p_oduncID;
    ELSE
        UPDATE ODUNC SET gercek_iade_tarihi = v_gercek_iade_tarihi, durum = 'iade'
        WHERE oduncID = p_oduncID;
    END IF;
    
    UPDATE KITAPLAR SET musait_adet = musait_adet + 1 WHERE kitapID = v_kitapID;
END;
$$ LANGUAGE plpgsql;
-- ================================================
-- TRIGGER: Otomatik Ceza Oluşturma
-- ================================================

-- Trigger Function: İade Edildiğinde Ceza Hesapla
CREATE OR REPLACE FUNCTION hesapla_ceza()
RETURNS TRIGGER AS $$
DECLARE
    v_gecikme_dakika INTEGER;
    v_ceza_tutari DECIMAL(10, 2);
    v_existing_ceza INTEGER;
BEGIN
    -- İade durumu güncellenmişse ve gecikmeli ise
    IF NEW.durum = 'iade' AND 
       NEW.gercek_iade_tarihi IS NOT NULL AND
       NEW.gercek_iade_tarihi > NEW.iade_tarihi THEN
        
        -- Gecikme süresini dakika olarak hesapla
        v_gecikme_dakika := EXTRACT(EPOCH FROM (NEW.gercek_iade_tarihi - NEW.iade_tarihi))::INTEGER / 60;
        
        -- Ceza tutarını hesapla (0.10 TL/dakika)
        v_ceza_tutari := v_gecikme_dakika * 0.10;
        
        -- Daha önce ceza var mı kontrol et
        SELECT COUNT(*) INTO v_existing_ceza
        FROM CEZALAR
        WHERE oduncID = NEW.oduncID;
        
        IF v_existing_ceza = 0 THEN
            -- Yeni ceza oluştur
            INSERT INTO CEZALAR (oduncID, kullaniciID, ceza_tutari, gecikme_gun, odenme_durumu)
            VALUES (NEW.oduncID, NEW.kullaniciID, v_ceza_tutari, v_gecikme_dakika, 'odenmedi');
            
            RAISE NOTICE 'Trigger: Ceza oluşturuldu! % TL (% dakika)', v_ceza_tutari, v_gecikme_dakika;
        END IF;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger Tanımı
DROP TRIGGER IF EXISTS trg_iade_edildiginde ON ODUNC;

CREATE TRIGGER trg_iade_edildiginde
AFTER UPDATE ON ODUNC
FOR EACH ROW
WHEN (NEW.durum = 'iade')
EXECUTE FUNCTION hesapla_ceza();

-- ================================================
-- KURULUM TAMAMLANDI!
-- ================================================