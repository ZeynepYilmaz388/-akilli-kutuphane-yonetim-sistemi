class Loan:
    def __init__(self, oduncID=None, kitapID=None, kullaniciID=None,
                 odunc_tarihi=None, iade_tarihi=None, 
                 gercek_iade_tarihi=None, durum='odunc'):
        self.oduncID = oduncID
        self.kitapID = kitapID
        self.kullaniciID = kullaniciID
        self.odunc_tarihi = odunc_tarihi
        self.iade_tarihi = iade_tarihi
        self.gercek_iade_tarihi = gercek_iade_tarihi
        self.durum = durum
    
    def to_dict(self):
        return {
            'oduncID': self.oduncID,
            'kitapID': self.kitapID,
            'kullaniciID': self.kullaniciID,
            'odunc_tarihi': str(self.odunc_tarihi) if self.odunc_tarihi else None,
            'iade_tarihi': str(self.iade_tarihi) if self.iade_tarihi else None,
            'gercek_iade_tarihi': str(self.gercek_iade_tarihi) if self.gercek_iade_tarihi else None,
            'durum': self.durum
        }
    
    @staticmethod
    def from_db_row(row):
        if row:
            return Loan(
                oduncID=row['oduncID'],
                kitapID=row['kitapID'],
                kullaniciID=row['kullaniciID'],
                odunc_tarihi=row.get('odunc_tarihi'),
                iade_tarihi=row.get('iade_tarihi'),
                gercek_iade_tarihi=row.get('gercek_iade_tarihi'),
                durum=row.get('durum', 'odunc')
            )
        return None