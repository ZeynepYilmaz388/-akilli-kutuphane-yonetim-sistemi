class User:
    def __init__(self, kullaniciID=None, kullanici_adsoyad=None, 
                 kullanici_sifre=None, kullanici_rol=None, 
                 kullanici_eposta=None, kayit_tarihi=None):
        self.kullaniciID = kullaniciID
        self.kullanici_adsoyad = kullanici_adsoyad
        self.kullanici_sifre = kullanici_sifre
        self.kullanici_rol = kullanici_rol
        self.kullanici_eposta = kullanici_eposta
        self.kayit_tarihi = kayit_tarihi
    
    def to_dict(self):
        return {
            'kullaniciID': self.kullaniciID,
            'kullanici_adsoyad': self.kullanici_adsoyad,
            'kullanici_rol': self.kullanici_rol,
            'kullanici_eposta': self.kullanici_eposta
        }
    
    @staticmethod
    def from_db_row(row):
        if row:
            return User(
                kullaniciID=row['kullaniciID'],
                kullanici_adsoyad=row['kullanici_adsoyad'],
                kullanici_sifre=row['kullanici_sifre'],
                kullanici_rol=row['kullanici_rol'],
                kullanici_eposta=row['kullanici_eposta'],
                kayit_tarihi=row.get('kayit_tarihi')
            )
        return None