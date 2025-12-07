-- 1. Kitap Ödünç Verme Function
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
        
        RAISE NOTICE 'Kitap başarıyla ödünç verildi.';
    ELSE
        RAISE EXCEPTION 'Kitap stokta mevcut değil!';
    END IF;
END;
$$ LANGUAGE plpgsql;

-- 2. Kitap İade Function
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