class Author:
   # def_init metodu constructor yapıcı metod
    def __init__(self, yazarID=None, yazar_ad=None, yazar_soyad=None, yazar_ulke=None):
        self.yazarID = yazarID
        self.yazar_ad = yazar_ad
        self.yazar_soyad = yazar_soyad
        self.yazar_ulke = yazar_ulke
    # gelen parametrleri nesnenin  içine kaydeder

    # to_dict metodu nesneyi sozluk yapısına çevirir
    #sebebi veritabanı işlemlerinde kolaylık sağlaması
    def to_dict(self):
        return {
            'yazarID': self.yazarID,
            'yazar_ad': self.yazar_ad,
            'yazar_soyad': self.yazar_soyad,
            'yazar_ulke': self.yazar_ulke
        }
    

    @staticmethod
    # bu fonsiyon  nesneye baglı değil self kullanılmaz
    def from_db_row(row):
        #veritabanından gelen satırı alır ve Author nesnesine dönüştürür
        if row:
            return Author(
                yazarID=row.get('yazarid'),
                yazar_ad=row.get('yazar_ad'),
                yazar_soyad=row.get('yazar_soyad'),
                yazar_ulke=row.get('yazar_ulke')
            )
        return None