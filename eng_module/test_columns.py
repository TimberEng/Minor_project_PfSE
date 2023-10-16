import columns

def test_Column():
    Co = columns.Column(h=160, A=42.78, Ix=1710.59, IY=679.91, kx=2.0, ky=1.0, E=50.0)

    assert Co.h == 160
    assert Co.A == 42.78
    assert Co.Ix == 1710.59
    assert Co.kx == 2


