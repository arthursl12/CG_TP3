"""
Classe Polyhedron
Região convexa definida por N planos. A computação desse poliedro é feita via
programação linear, logo ressalta-se a importância de que as normais dos planos 
estejam apontadas sempre para dentro da região, ou seja, para dentro do poliedro

Forma: Ax >= b  <=>  ax + by + cz + d >= 0
Eq. Plano: ax + by + cz + d = 0
"""
from plane import Plane
from sphere import Hit
from vector import Vector


class Polyhedron:
    def __init__(self, eqns_planos, material):
        self.planos = []
        for eqn in eqns_planos:
            plano = Plane(eqn, material)
            self.planos.append(plano)
        self.material = material
        
    def intersects(self, ray, dist):
        # Computa todas as interseções do raio com cada plano
        inters = []
        for plane in self.planos:
            new_dist, inter = plane.intersects(ray, dist)
            data = {
                "plano": plane,
                "new_dist": new_dist,
                "hit?": inter
            }
            inters.append(data)
        
        # Seleciona apenas as interseções HIT ou INSIDE
        hits = []
        for data in inters:
            if (data["hit?"] != Hit.MISS):
                hits.append(data)
        if (len(hits) == 0):
            return dist, Hit.MISS
        
        # Seleciona apenas as interseções na região válida
        in_the_region = []
        for data in hits:
            point = ray.origin + data["new_dist"] * ray.direction
            above_all = True
            for plane in self.planos:
                if (not plane.above(point)):
                    above_all = False
            if (above_all):
                in_the_region.append(data)
        if (len(in_the_region) == 0):
            return dist, Hit.MISS
            
        in_the_region = sorted(in_the_region, key=lambda k: k["new_dist"]) 
        result = in_the_region[0]["new_dist"]
        if (result < dist):
            plane = in_the_region[0]["plano"]
            if (not plane.above(ray.origin)):
                return result, Hit.HIT
            else:
                return result, Hit.INSIDE
        #     norm_sqr = (plane[0] ** 2) + (plane[1] ** 2) + (plane[2] ** 2)
        #     # p0: um ponto no plano
        #     p0 = Vector(
        #         (plane[0] * (-plane[3])) / norm_sqr,
        #         (plane[1] * (-plane[3])) / norm_sqr,
        #         (plane[2] * (-plane[3])) / norm_sqr,
        #     )
        #     Np = (Vector(plane[0], plane[1], plane[2])).normalize()
        #     l = (ray.direction).normalize()
        #     denom = Np.dot_product(l) 
        #     if (abs(denom) > 1e-6):
        #         p0l0 = p0 - ray.origin
        #         t = p0l0.dot_product(Np) / denom
        #         if (t >= 0):
        #             inters.append(t)
        
        # # Testa se os pontos estão dentro da região ou na fronteira dela
        # for t in inters:
        #     point = ray.origin + t * ray.direction
        #     for plane in self.planos:
        #         lhs = (
        #             point.x * plane[0]
        #             + point.y * plane[1]
        #             + point.z * plane[2]
        #         )
        #         rhs = plane[3]
        #         if ((lhs < rhs) and (t in inters)):
        #             # Ponto fora da região
        #             inters.remove(t)

                    
        # if (len(inters) == 0):
        #     # Todos os pontos de interseção encontrados estão fora da região
        #     return dist, Hit.MISS
        
        # # Define se foi um hit dentro ou fora
        # inters.sort()
        # t_result = inters[0]
        # if (t_result < dist):
        #     # Acha o plano de interseção
        #     point = ray.origin + t_result * ray.direction
        #     for plane in self.planos:
        #         lhs = (
        #             point.x * plane[0]
        #             + point.y * plane[1]
        #             + point.z * plane[2]
        #         )
        #         rhs = plane[3]
        #         if (abs(lhs-rhs) < 0.001):
        #             plano_inters = plane
        #             break
            
        #     Np = (Vector(plano_inters[0], plano_inters[1], plano_inters[2])).normalize()
        #     R = (ray.origin - point).normalize()
        #     cos = Np.dot_product(R)
        #     if (cos >= 0):
        #         return t_result, Hit.INSIDE
        #     else:
        #         return t_result, Hit.HIT
        # else:
        #     return dist, Hit.MISS
            
    def normal(self, surface_point, inside):
        # Acha o plano de interseção
        point = surface_point
        for plane in self.planos:
            lhs = (
                point.x * plane[0]
                + point.y * plane[1]
                + point.z * plane[2]
            )
            rhs = plane[3]
            if (abs(lhs-rhs) < 0.001):
                plano_inters = plane
                break
            
        assert (plano_inters is not None)      # Senão o ponto não está no plano
        if (inside):
            return (Vector(plano_inters[0],plano_inters[1],plano_inters[2])).normalize()
        else:
            N_dentro = (Vector(plano_inters[0],plano_inters[1],plano_inters[2])).normalize()
            return (-1) * N_dentro
        
    def color_at(self, surf_point):
        return self.material.color_at(surf_point)

if __name__ == "__main__":
    from color import Color
    from material import Material
    from ray import Ray
    material = Material(Color.from_hex("#D3D3D3"))
    planes = [
        [0, 1, 0, -60],
        [1, 0, 0, 300],
        [-1, 0, 0, 300],
        [0, 0, -1, 300],
        [0, 0, 1, 300]
    ]
    P = Polyhedron(planes, material)
    
    # ray1 = Ray(Vector(0,0,0), Vector(1,1,1).normalize())
    # P.intersects(ray1, float('inf'))
    
    ray1 = Ray(Vector(0,0,0), Vector(1,1,1).normalize())
    ray2 = Ray(Vector(0,500,500), Vector(0,0,-1))
    ray3 = Ray(Vector(0,500,500), Vector(1,0,0))
    
    P.intersects(ray1, float('inf'))
    P.intersects(ray2, float('inf'))
    P.intersects(ray3, float('inf'))
