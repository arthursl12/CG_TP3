import pytest
from vector import Vector
from color import Color
from ray import Ray
from material import Material
from sphere import Hit
from plane import Plane

class TestPlane:
    @classmethod
    def setup_class(cls):
        material = Material(Color.from_hex("#D3D3D3"))
        cls.eqn = [0, 1, 0, -60]
        cls.P = Plane(cls.eqn, material)
    
    def test_normal(self):
        N = self.P.normal(Vector(0,60,0), False)
        assert N == Vector(0,-1,0)
        
        N = self.P.normal(Vector(0,60,0), True)
        assert N == Vector(0,1,0)

    def test_above(self):       
        assert self.P.above(Vector(0,-80,0)) == False
        assert self.P.above(Vector(0,-40,0)) == True
        assert self.P.above(Vector(0,-60,0)) == True
    
    def test_intersects(self):
        ray1 = Ray(Vector(0,-80,0), Vector(1,1,1))
        ray2 = Ray(Vector(0,-40,0), Vector(-1,-1,-1))
        ray3 = Ray(Vector(0,500,500), Vector(0,1,0))

        assert self.P.intersects(ray1, float('inf')) == (pytest.approx(34.641, abs=0.001), Hit.HIT)
        assert self.P.intersects(ray2, float('inf')) == (pytest.approx(34.641, abs=0.001), Hit.INSIDE)
        assert self.P.intersects(ray3, float('inf')) == (float('inf'), Hit.MISS)
        
