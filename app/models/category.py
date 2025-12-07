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
        if row:
            return Category(
                kategoriID=row['kategoriID'],
                katagori_adi=row['katagori_adi'],
                aciklama=row.get('aciklama')
            )
        return None