import math
from vector import Vector
from ray import Ray

class Camera:
    def __init__(self, eye, vfov, aspect_ratio):
        theta = math.radians(vfov)
        self.h = math.tan(theta) / 2
        self.aspect_ratio = aspect_ratio

        self.view_height = 2.0 * self.h
        self.view_width = aspect_ratio * self.view_height

        self.horizontal = Vector(self.view_width, 0, 0)
        self.vertical = Vector(0, self.view_height, 0)
        self.canto_inf_esq =  eye - self.horizontal/2 - self.vertical/2 - Vector(0, 0, 1)
        self.eye = eye
    
    def get_ray(self, u, v):
        return Ray(
            self.eye, 
            (
                self.canto_inf_esq 
                + u * self.horizontal 
                + v * self.vertical 
                - self.eye
            )
        )