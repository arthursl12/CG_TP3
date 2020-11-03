import pytest
from modules.vector import (Vector, list_from_string, vector_from_list,
                            vector_from_string)


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

class TestFromString:
    def test_from_string_int(self):
        string = "1 0 0"
        assert Vector(1,0,0) == vector_from_string(string)
    
    def test_from_string_spaces(self):
        string = "   1   0     2    "
        assert Vector(1,0,2) == vector_from_string(string)
    
    def test_from_string_float(self):
        string = "1.0000 0.9998 0.2"
        assert Vector(1.0, 0.9998, 0.2) == vector_from_string(string)
    
    def test_from_string_spaces_int(self):
        string = "    1.0000         0.9998            0.2 "
        assert Vector(1.0, 0.9998, 0.2) == vector_from_string(string)

class TestFromList:
    def test_from_list_int(self):
        _list = ['1','0','0']
        assert Vector(1,0,0) == vector_from_list(_list)
    
    def test_from_list_float(self):
        _list = ['1.0000','0.9998','0.2']
        assert Vector(1.0, 0.9998, 0.2) == vector_from_list(_list)


