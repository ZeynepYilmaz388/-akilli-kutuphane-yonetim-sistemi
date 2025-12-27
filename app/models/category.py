class Category:
    def __init__(self, kategoriID=None, katagori_adi=None, aciklama=None):
        self.kategoriID = kategoriID
        self.katagori_adi = katagori_adi
        self.aciklama = aciklama
    
    def to_dict(self):
        return {
            'kategoriID': self.kategoriID,
            'katagori_adi': self.katagori_adi,
            'aciklama': self.aciklama
        }
    
    @staticmethod
    def from_db_row(row):
        #veritabanından gelen satırı alır ve Category nesnesine dönüştürür
        if row:
            return Category(
                kategoriID=row.get('kategoriid'),
                katagori_adi=row.get('katagori_adi'),
                aciklama=row.get('aciklama')
            )
        return None