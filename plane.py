from vector import Vector
from sphere import Hit
from image import Image

class Plane:
    """Formato da Equação: ax + by + cz = d"""
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
            t = -(P0.dot_product(N) + (-plane[3])) / (V.dot_product(N))
            if (t >= 0 and t < dist):
                hit = True
                if (V.dot_product(N) > 0):
                    return t, Hit.HIT
                else:
                    return t, Hit.INSIDE
        return dist, Hit.MISS

    def above(self, point):
        plane = self.equacao
        norm_sqr = (plane[0] ** 2) + (plane[1] ** 2) + (plane[2] ** 2)
        # P0: um ponto no plano
        P0 = Vector(
            (plane[0] * plane[3]) / norm_sqr,
            (plane[1] * plane[3]) / norm_sqr,
            (plane[2] * plane[3]) / norm_sqr,
        )
        N = (Vector(plane[0], plane[1], plane[2])).normalize()
        PP0 = point - P0
        if (PP0.magnitude() == 0):
            return True

        PP0 = (point - P0).normalize()
        dot = N.dot_product(PP0)
        
        if (dot >= 0):
            return True
        else:
            return False
    
    def normal(self, surface_point, inside):
        Np = Vector(self.equacao[0], self.equacao[1], self.equacao[2]).normalize()
        if (inside == True):
            return Np
        else:
            return (-1) * Np
    
    def color_at(self, surf_point):
        if (self.material.texture is None):
            return self.material.color_at(surf_point)
        else:
            # Queremos achar e1 e e2 bases do plano
            Np = Vector(self.equacao[0], self.equacao[1], self.equacao[2]).normalize()
            e1 = (Np.cross_product(Vector(1, 0, 0))).normalize()
            if (e1 == Vector(0, 0, 0)):
                # Se Np e e1 forem paralelos
                e1 = (Np.cross_product(Vector(0, 0, 1))).normalize()
            
            e2 = (Np.cross_product(e1)).normalize()
            h = self.material.texture.height
            w = self.material.texture.width
            u = surf_point.dot_product(e1) * w
            v = surf_point.dot_product(e2) * h
            v_bound = round(v) % h
            u_bound = round(u) % w
            c = self.material.texture.get_pixel(u_bound,v_bound)

            return c

if __name__ == "__main__":
    from material import Material
    from color import  Color
    from ray import Ray
    material = Material(Color.from_hex("#D3D3D3"))
    eqn = [0, 1, 0, 60]
    P = Plane(eqn, material)
    
    # ray1 = Ray(Vector(0,-40,0), Vector(-1,-1,-1))
    # P.intersects(ray1, float('inf'))
    
    ray2 = Ray(Vector(0,-40,0), Vector(-1,-1,-1))
    P.above(ray2) == True