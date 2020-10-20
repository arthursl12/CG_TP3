from math import sqrt

from enum import Enum
class Hit(Enum):
    MISS = 0
    INSIDE = -1
    HIT = 1

class Sphere:
    """Uma esfera tridimensional. Possui centro, raio e material"""
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material
    
    def intersects(self, ray, dist):
        """Verifica se ray intercepta a esfera. Retorna a distância até a 
        interseção ou None se não há interseção"""
        #a = 1
        sphere_to_ray = ray.origin - self.center
        b = 2 * ray.direction.dot_product(sphere_to_ray)
        c = sphere_to_ray.dot_product(sphere_to_ray) - self.radius * self.radius
        delta = b * b - 4 * c

        if delta > 0:
            x1 = (-b - sqrt(delta)) / 2 
            x2 = (-b + sqrt(delta)) / 2
            if x2 > 0:
                if x1 < 0:
                    if x2 < dist:
                        return x2, Hit.INSIDE

                else:
                    if x1 < dist:
                        return x1, Hit.HIT
        return dist, Hit.MISS
    
    def normal(self, surface_point):
        """Retorna a normal no ponto da superfície da esfera"""
        return (surface_point - self.center).normalize()