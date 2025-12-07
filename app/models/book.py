class Book:
    def __init__(self, kitapID=None, baslik=None, yazarID=None, 
                 kategoriID=None, yayin_yili=None, stok_adedi=0, musait_adet=0):
        self.kitapID = kitapID
        self.baslik = baslik
        self.yazarID = yazarID
        self.kategoriID = kategoriID
        self.yayin_yili = yayin_yili
        self.stok_adedi = stok_adedi
        self.musait_adet = musait_adet
    
    def to_dict(self):
        return {
            'kitapID': self.kitapID,
            'baslik': self.baslik,
            'yazarID': self.yazarID,
            'kategoriID': self.kategoriID,
            'yayin_yili': self.yayin_yili,
            'stok_adedi': self.stok_adedi,
            'musait_adet': self.musait_adet
        }
    
    @staticmethod
    def from_db_row(row):
        if row:
            return Book(
                kitapID=row['kitapID'],
                baslik=row['baslik'],
                yazarID=row.get('yazarID'),
                kategoriID=row.get('kategoriID'),
                yayin_yili=row.get('yayin_yili'),
                stok_adedi=row.get('stok_adedi', 0),
                musait_adet=row.get('musait_adet', 0)
            )
        return None