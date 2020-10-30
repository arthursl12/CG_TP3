import pytest
from vector import Vector
from color import Color
from ray import Ray
from material import Material
from sphere import Hit
from polyhedron import Polyhedron

class TestPolyhedron:
    @classmethod
    def setup_class(cls):
        material = Material(Color.from_hex("#D3D3D3"))
        cls.planes = [
            [0, 1, 0, -60],
            [1, 0, 0, 300],
            [-1, 0, 0, 300],
            [0, 0, -1, 300],
            [0, 0, 1, 300]
        ]
        cls.P = Polyhedron(cls.planes, material)
    
    def test_normal(self):
        N = self.P.normal(Vector(0,60,0), False)
        assert N == Vector(0,-1,0)
        
        N = self.P.normal(Vector(0,60,0), True)
        assert N == Vector(0,1,0)

        
    
    def test_intersects(self):
        ray1 = Ray(Vector(0,0,0), Vector(1,1,1).normalize())
        ray2 = Ray(Vector(0,500,500), Vector(0,0,-1))
        ray3 = Ray(Vector(0,500,500), Vector(1,0,0))
        
        assert self.P.intersects(ray1, float('inf')) == (pytest.approx(103.9230, abs=0.001), Hit.HIT)
        assert self.P.intersects(ray2, float('inf')) == (pytest.approx(200, abs=0.001), Hit.HIT)
        assert self.P.intersects(ray3, float('inf')) == (float('inf'), Hit.MISS)
        
    def test_intersects_inside(self):
        ray4 = Ray(Vector(0,70,0), Vector(0,1,1))
        assert self.P.intersects(ray4, float('inf')) == (pytest.approx(424.2640, abs=0.001), Hit.INSIDE)
