from math import sqrt

class Sphere:
    """Uma esfera tridimensional. Possui centro, raio e material"""
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material
    
    def intersects(self, ray):
        """Verifica se ray intercepta a esfera. Retorna a distância até a 
        interseção ou None se não há interseção"""
        #a = 1
        sphere_to_ray = ray.origin - self.center
        b = 2 * ray.direction.dot_product(sphere_to_ray)
        c = sphere_to_ray.dot_product(sphere_to_ray) - self.radius * self.radius
        delta = b * b - 4 * c

        if delta >= 0:
            dist = (-b - sqrt(delta)) / 2 
            if dist > 0:
                return dist
        return None  