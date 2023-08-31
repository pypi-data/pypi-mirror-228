from src.sanber_geometry import lingkaran, persegi
import pytest
import numpy as np

## PERSEGI TEST
@pytest.mark.parametrize("panjang, lebar, expected_luas", [
    (10, 5, 50),
    (20, 3, 60),
    (5, 10, 50)
])

def test_hitung_luas_persegi_dengan_panjang_lebar_beda(panjang, lebar, expected_luas):
    persegi1 = persegi.Persegi(panjang=panjang,lebar=lebar)
    assert persegi1.luas() == expected_luas

@pytest.mark.parametrize("panjang, lebar, expected_keliling", [
    (10, 5, 30),
    (20, 3, 46),
    (5, 10, 30)
])

def test_hitung_keliling_persegi_dengan_panjang_lebar_beda(panjang, lebar, expected_keliling):
    persegi1 = persegi.Persegi(panjang=panjang,lebar=lebar)
    assert persegi1.keliling() == expected_keliling
    
## LINGKARAN TEST
@pytest.mark.parametrize("radius, expected_luas", [
    (10, np.pi*10**2),
    (20, np.pi*20**2),
    (137, np.pi*137**2)
])

def test_hitung_luas_lingkaran_dengan_radius_beda(radius, expected_luas):
    lingkaran1 = lingkaran.Lingkaran(radius)
    assert lingkaran1.luas() == expected_luas
    
@pytest.mark.parametrize("radius, expected_keliling", [
    (10, np.pi*10*2),
    (20, np.pi*20*2),
    (137, np.pi*137*2)
])

def test_hitung_luas_lingkaran_dengan_radius_beda(radius, expected_keliling):
    lingkaran1 = lingkaran.Lingkaran(radius)
    assert lingkaran1.keliling() == expected_keliling
    
if __name__ == "__main__":
    pytest.main()