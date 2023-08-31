class Lingkaran:
    def __init__(self, radius): #dikerjakan di awal misal inisialisasi variabel
        self.radius = radius
    
    def hitung_luas(self):
        return 3.14*self.radius*self.radius
    
    def hitung_keliling(self):
        return 2*3.14*self.radius

def menghitung_luas():
    return "ini fungsi menghitung luas"