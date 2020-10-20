import pytest
from vector import Vector
from color import Color
from ray import Ray
from material import Material
from sphere import Sphere, Hit

class TestSphere:
    @classmethod
    def setup_class(cls):
        material = Material(Color.from_hex("#D3D3D3"))
        cls.S = Sphere(Vector(5,5,5), 1, material)

    def test_normal(self):
        N = self.S.normal(Vector(5,6,5))
        assert N == Vector(0,1,0)
    
    def test_intersects(self):
        ray1 = Ray(Vector(0,0,0), Vector(1,1,1))
        ray2 = Ray(Vector(4.87,4.16,5.53), Vector(-4.87,-4.16,-5.53))
        ray3 = Ray(Vector(0,0,0), Vector(1,0,0))
        
        assert self.S.intersects(ray1, float('inf')) == (pytest.approx(7.66, abs=0.001), Hit.HIT)
        assert self.S.intersects(ray2, float('inf')) == (float('inf'), Hit.MISS)
        assert self.S.intersects(ray3, float('inf')) == (float('inf'), Hit.MISS)
        
    def test_intersects_inside(self):
        ray4 = Ray(Vector(5,5,5), Vector(1,1,1))
        assert self.S.intersects(ray4, float('inf')) == (pytest.approx(1, abs=0.001), Hit.INSIDE)