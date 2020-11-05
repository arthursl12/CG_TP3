from unittest.mock import Mock

import pytest
from modules.engine import RenderEngine
from modules.ray import Ray
from modules.scene import Scene
from modules.sphere import Hit, Sphere
from modules.vector import Vector


class TestFindNearest:
    @classmethod
    def setup_class(cls):
        material = Mock()
        S = Sphere(Vector(5,5,5), 1, material)
        cls.obj = [S]
        cls.scene = Scene(Mock(),cls.obj, Mock(), Mock(), Mock())
        cls.engine = RenderEngine()
    
    def test_simple(self):
        ray = Ray(Vector(0,0,0), Vector(1,1,1))
        t_min, obj_hit, result = self.engine.find_nearest(ray, self.scene)
        assert t_min == pytest.approx(7.66, abs=0.001)
        assert obj_hit.center == self.obj[0].center
        assert result == Hit.HIT
    
    def test_more_objects(self):
        ray = Ray(Vector(0,0,0), Vector(1,1,1))
        obj = self.obj + [Sphere(Vector(10,10,10), 1, Mock())]
        scene = Scene(Mock(),obj, Mock(), Mock(), Mock())
        t_min, obj_hit, result = self.engine.find_nearest(ray, scene)
        assert t_min == pytest.approx(7.66, abs=0.001)
        assert obj_hit.center == self.obj[0].center
        assert result == Hit.HIT
    
    def test_inside_ray(self):
        ray4 = Ray(Vector(5,5,5), Vector(1,1,1))
        obj = self.obj + [Sphere(Vector(10,10,10), 1, Mock())]
        scene = Scene(Mock(),obj, Mock(), Mock(), Mock())
        t_min, obj_hit, result = self.engine.find_nearest(ray4, scene)
        assert t_min == pytest.approx(1, abs=0.001)
        assert obj_hit.center == self.obj[0].center
        assert result == Hit.INSIDE
