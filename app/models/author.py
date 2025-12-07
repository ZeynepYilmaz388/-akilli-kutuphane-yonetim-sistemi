class Author:
    def __init__(self, yazarID=None, yazar_ad=None, yazar_soyad=None, yazar_ulke=None):
        self.yazarID = yazarID
        self.yazar_ad = yazar_ad
        self.yazar_soyad = yazar_soyad
        self.yazar_ulke = yazar_ulke
    
    def to_dict(self):
        return {
            'yazarID': self.yazarID,
            'yazar_ad': self.yazar_ad,
            'yazar_soyad': self.yazar_soyad,
            'yazar_ulke': self.yazar_ulke
        }
    
    @staticmethod
    def from_db_row(row):
        if row:
            return Author(
                yazarID=row['yazarID'],
                yazar_ad=row['yazar_ad'],
                yazar_soyad=row['yazar_soyad'],
                yazar_ulke=row.get('yazar_ulke')
            )
        return None