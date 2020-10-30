"""
Classe Polyhedron
Região convexa definida por N planos. A computação desse poliedro é feita via
programação linear, logo ressalta-se a importância de que as normais dos planos 
estejam apontadas sempre para dentro da região, ou seja, para dentro do poliedro

Forma: Ax >= b  <=>  ax + by + cz >= d
Eq. Plano: ax + by + cz = d
"""
from vector import Vector
from sphere import Hit
class Polyhedron:
    def __init__(self, planos, material):
        self.planos = planos
        self.material = material
        
    def intersects(self, ray, dist):
        # Computa todas as interseções do raio com cada plano
        inters = []
        for plane in self.planos:
            norm_sqr = (plane[0] ** 2) + (plane[1] ** 2) + (plane[2] ** 2)
            # p0: um ponto no plano
            p0 = Vector(
                (plane[0] * plane[3]) / norm_sqr,
                (plane[1] * plane[3]) / norm_sqr,
                (plane[2] * plane[3]) / norm_sqr,
            )
            Np = (Vector(plane[0], plane[1], plane[2])).normalize()
            l = (ray.direction).normalize()
            denom = Np.dot_product(l) 
            if (abs(denom) > 1e-6):
                p0l0 = p0 - ray.origin
                t = p0l0.dot_product(Np) / denom
                if (t >= 0):
                    inters.append(t)
        
        # Testa se os pontos estão dentro da região ou na fronteira dela
        for t in inters:
            point = ray.origin + t * ray.direction
            for plane in self.planos:
                lhs = (
                    point.x * plane[0]
                    + point.y * plane[1]
                    + point.z * plane[2]
                )
                rhs = plane[3]
                if (lhs < rhs):
                    # Ponto fora da região
                    inters.remove(t)
                    
        if (len(inters) == 0):
            # Todos os pontos de interseção encontrados estão fora da região
            return float('inf'), Hit.MISS
        
        # Define se foi um hit dentro ou fora
        inters.sort()
        t_result = inters[0]
         
        # Acha o plano de interseção
        point = ray.origin + t_result * ray.direction
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
        
        Np = (Vector(plano_inters[0], plano_inters[1], plano_inters[2])).normalize()
        R = ((-1)*ray.direction).normalize()
        cos = Np.dot_product(R)
        if (cos > 0):
            return t_result, Hit.INSIDE
        else:
            return t_result, Hit.HIT
            
                
            
    
    def normal(self, surface_point, inside):
        pass
    
    def color_at(self, surf_point):
        pass

if __name__ == "__main__":
    from material import Material
    from color import  Color
    from ray import Ray
    material = Material(Color.from_hex("#D3D3D3"))
    planes = [
        [0, 1, 0, 60],
        [1, 0, 0, -300],
        [-1, 0, 0, -300],
        [0, 0, -1,-300],
        [0, 0, 1, -300]
    ]
    P = Polyhedron(planes, material)
    
    ray1 = Ray(Vector(0,0,0), Vector(1,1,1).normalize())
    P.intersects(ray1, float('inf'))