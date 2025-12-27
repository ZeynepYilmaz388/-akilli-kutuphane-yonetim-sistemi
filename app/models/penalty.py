class Penalty:
    def __init__(self, cezaID=None, oduncID=None, kullaniciID=None,
                 ceza_tutari=0.00, gecikme_gun=0, odenme_durumu='odenmedi',
                 ceza_tarihi=None, odeme_tarihi=None):
        self.cezaID = cezaID
        self.oduncID = oduncID
        self.kullaniciID = kullaniciID
        self.ceza_tutari = ceza_tutari
        self.gecikme_gun = gecikme_gun
        self.odenme_durumu = odenme_durumu
        self.ceza_tarihi = ceza_tarihi
        self.odeme_tarihi = odeme_tarihi

    def to_dict(self):
        return {
            'cezaID': self.cezaID,
            'oduncID': self.oduncID,
            'kullaniciID': self.kullaniciID,
            'ceza_tutari': float(self.ceza_tutari) if self.ceza_tutari else 0.00,
            'gecikme_gun': self.gecikme_gun,
            'odenme_durumu': self.odenme_durumu,
            'ceza_tarihi': str(self.ceza_tarihi) if self.ceza_tarihi else None,
            'odeme_tarihi': str(self.odeme_tarihi) if self.odeme_tarihi else None
        }

    @staticmethod
    def from_db_row(row):
        #veritabanından gelen satırı alır ve Penalty nesnesine dönüştürür
        if row:
            return Penalty(
                cezaID=row.get('cezaid'),
                oduncID=row.get('oduncid'),
                kullaniciID=row.get('kullaniciid'),
                ceza_tutari=row.get('ceza_tutari'),
                gecikme_gun=row.get('gecikme_gun'),
                odenme_durumu=row.get('odenme_durumu', 'odenmedi'),
                ceza_tarihi=row.get('ceza_tarihi'),
                odeme_tarihi=row.get('odeme_tarihi')
            )
        return None