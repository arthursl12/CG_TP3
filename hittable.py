from abc import ABC, abstractmethod

class HitRecord:
    def __init__(self, ponto, t):
        self.point = ponto
        self.t = t

    def set_face_normal(self, ray, outward_normal):
        self.front_face = (ray.direction.dot_product(outward_normal) < 0)
        self.normal = outward_normal if front_face else -outward_normal
    


class Hittable(ABC):
    @abstractmethod
    def hit(self, ray, t_min, t_max, hit_record_list):
        pass
