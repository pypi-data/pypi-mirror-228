from  ..src.geometry import lingkaran, persegi, segitiga
#from geometry import lingkaran, persegi, segitiga
import pytest

nilai_uji_lingkaran = [
    (1, 3.14),
    (10, 314),
    (7, 153.86)
]

nilai_uji_persegi = [
    (1, 1),
    (10, 100),
    (7, 49)
]

nilai_uji_segitiga = [
    (10, 20, 100),
    (5, 10, 25),
    (4, 3, 6)
]

@pytest.mark.parametrize("radius, expected_total", nilai_uji_lingkaran)
def test_hitung_luas_lingkaran (radius, expected_total):
    circle = lingkaran.Lingkaran(radius)
    assert circle.hitung_luas() == expected_total

@pytest.mark.parametrize("sisi, expected_total", nilai_uji_persegi)
def test_hitung_luas_persegi(sisi, expected_total):
    assert persegi.hitung_luas (sisi) == expected_total

@pytest.mark.parametrize("alas, tinggi, expected_total", nilai_uji_segitiga)
def test_hitung_luas_segitiga (alas, tinggi, expected_total):
    assert segitiga.hitung_luas (alas,tinggi) == expected_total

if __name__=="__main__":
    pytest.main()