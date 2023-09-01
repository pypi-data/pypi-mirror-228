from src.geometry import lingkaran, persegi, kubus
import pytest

nilai_uji_lingkaran = [
    (1, 3.14),
    (10, 314),
    (7, 153.86),
]

nilai_uji_persegi = [
    (1, 1),
    (10, 100),
    (7, 49),
]

nilai_uji_kubus = [
    (1, 1),
    (10, 1000),
    (3, 27),
]

@pytest.mark.parametrize("radius, expected_total", nilai_uji_lingkaran)
def test_hitung_luas_lingkaran(radius, expected_total):
    circle = lingkaran.Lingkaran(radius)
    assert circle.hitung_luas() == expected_total

@pytest.mark.parametrize("sisi, expected_total", nilai_uji_persegi)
def test_hitung_luas_persegi(sisi, expected_total):
    assert persegi.hitung_luas(sisi) == expected_total

@pytest.mark.parametrize("sisi, expected_total", nilai_uji_kubus)
def test_hitung_volume_kubus(sisi, expected_total):
    assert kubus.hitung_volume(sisi) == expected_total

if __name__ == "__main__":
    pytest.main()



