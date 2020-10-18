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
        assert sum == Vector(4.0, 4.0, 7.0)
    
    def test_multiplication(self):
        p = self.v1 * 2 
        assert p == Vector(2.0, -4.0, -4.0)
    
    def test_division(self):
        p = self.v1 / 2 
        assert p == Vector(0.5, -1.0, -1.0)
    
    def test_equality(self):
        assert self.v1 == self.v1



