import math

from modules.ray import Ray


class Camera:
    def __init__(self, eye, look_at, up, vfov, aspect_ratio):
        # Definição dos tamanhos do plano de projeção, com base no ângulo de fov
        # e no aspect_ratio
        vfov = min(75,vfov)
        theta = math.radians(vfov)
        self.h = math.tan(theta) / 2
        self.aspect_ratio = aspect_ratio
        self.view_height = 2.0 * self.h
        self.view_width = aspect_ratio * self.view_height
        
        
        w = (eye - look_at).normalize()     # Contrário da direção que estamos olhando
        u = (up.cross_product(w)).normalize()             # Direita, no plano de projeção
        v = u.cross_product(w)              # Cima, no plano de projeção
        
        
        self.eye = eye
        self.horizontal = self.view_width * u
        self.vertical = self.view_height * v
        self.canto_inf_esq = self.eye - self.horizontal/2 - self.vertical/2 - w
        
    
    def get_ray(self, s, t):
        return Ray(
            self.eye, 
            (
                self.canto_inf_esq 
                + s * self.horizontal 
                + t * self.vertical 
                - self.eye
            )
        )
