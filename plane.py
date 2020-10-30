from vector import Vector
from sphere import Hit

class Plane:
    """Formato da Equação: ax + by + cz + d = 0"""
    def __init__(self, equacao, material):
        self.equacao = equacao
        self.material = material
    
    def intersects(self, ray, dist):
        plane = self.equacao
        V = ray.direction.normalize()
        N = (Vector(plane[0], plane[1], plane[2])).normalize()
        P0 = ray.origin
        hit = False
        if (V.dot_product(N) != 0):
            t = -(P0.dot_product(N) + plane[3]) / (V.dot_product(N))
            if (t >= 0 and t < dist):
                hit = True
                if (V.dot_product(N) > 0):
                    return t, Hit.HIT
                else:
                    return t, Hit.INSIDE
        return dist, Hit.MISS

    def normal(self, surface_point, inside):
        Np = Vector(self.equacao[0], self.equacao[1], self.equacao[2]).normalize()
        if (inside == True):
            return Np
        else:
            return (-1) * Np

if __name__ == "__main__":
    from material import Material
    from color import  Color
    from ray import Ray
    material = Material(Color.from_hex("#D3D3D3"))
    eqn = [0, 1, 0, -60]
    P = Plane(eqn, material)
    
    ray1 = Ray(Vector(0,-40,0), Vector(-1,-1,-1))
    P.intersects(ray1, float('inf'))