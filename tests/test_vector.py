import pytest
from vector import Vector

class TestVector:
    @classmethod
    def setup_class(cls):
        cls.v1 = Vector(1.0, -2.0, -2.0)
        cls.v2 = Vector(3.0, 6.0, 9.0)

    def test_magnitude(self):
        assert pytest.approx(3, abs=0.001) == self.v1.magnitude()
    
    def test_addition(self):
        sum = self.v1 + self.v2
        assert sum.x == 4.0
        assert sum.y == 4.0
        assert sum.z == 7.0
    
    def test_multiplication(self):
        p = self.v1 * 2 
        assert p.x ==  2.0
        assert p.y == -4.0
        assert p.z == -4.0
    
    def test_division(self):
        p = self.v1 / 2 
        assert p.x ==  0.5
        assert p.y == -1.0
        assert p.z == -1.0



