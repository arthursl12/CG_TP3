import math
import random

from camera import Camera
from color import Color
from image import Image
from light import LightType
from point import Point
from ray import Ray
from sphere import Hit
from vector import Vector


class RenderEngine:
    """Renderiza os objetos no plano de renderização"""

    MAX_DEPTH = 10
    MIN_DISPLACE = 0.1

    def render(self, scene, qtd_samples):
        width = scene.width
        height = scene.height
        aspect_ratio = float(width) / height
        
        # camera = scene.camera
        camera = scene.camera
        ## TODO: tratamento do ângulo para (1) não poder ser 90° e (2) não ter tangente negativa
        pixels = Image(width, height)

        for j in reversed(range(height)):
            for i in reversed(range(width)):
                for s in range(qtd_samples):
                    u = (float(i) + random.random())/ (width-1)
                    v = (float(j) + random.random()) / (height-1)
                    ray = camera.get_ray(u, v)
                    color = Color(0,0,0)
                    dist = float('inf')
                    RIndex = 1.0
                    color, dist, RIndex = self.ray_trace(ray, scene, t=dist, aRIndex=RIndex, color=color, depth=0)
                    pixels.add_pixel(i, j, color)
            print(f"{float(height-j)/float(height) * 100:3.0f}%", end="\r")
        return pixels
    
    def ray_trace(self, ray, scene, aRIndex, t, color, depth=0):
        # Encontra o objeto mais próximo que o raio intercepta
        t, obj_hit, case = self.find_nearest(ray, scene)
        if obj_hit is None:
            return color, t, aRIndex
        hit_pos = ray.origin + ray.direction * t
        if (case == Hit.INSIDE):
            inside = True
        else:
            inside = False
        hit_normal = obj_hit.normal(hit_pos, inside)
        color += self.color_at(obj_hit, hit_pos, hit_normal, scene, ray)

        # Cálculo da Reflexão
        if (depth < self.MAX_DEPTH and obj_hit.material.reflection > 0):
            new_ray_pos = hit_pos + hit_normal * self.MIN_DISPLACE
            new_ray_dir = ray.direction - 2 * ray.direction.dot_product(hit_normal) * hit_normal
            new_ray = Ray(new_ray_pos, new_ray_dir)

            # Atenuar o raio refletido pelo coeficiente de reflexão
            rcol, rt, raRIndex = self.ray_trace(new_ray, scene, aRIndex=aRIndex, t=float('inf'), depth=depth+1, color=Color(0,0,0))
            color = Color(color.x, color.y, color.z)
            color += rcol * obj_hit.material.reflection
            color += obj_hit.material.reflection * obj_hit.material.color_at(hit_pos) * 0.03

        # Cálculo da Refração
        if (depth < self.MAX_DEPTH and obj_hit.material.refraction > 0):
            refr = obj_hit.material.refraction
            # rindex = obj_hit.material.refrIndex
            # n = aRIndex / rindex
            # rindex = obj_hit.material.ior
            # rindex = aRIndex / obj_hit.material.ior
            if (case == Hit.INSIDE):
                refr_ratio = obj_hit.material.ior
            else:
                refr_ratio = 1.0 / obj_hit.material.ior
            unit_direction = (ray.direction).normalize()
            N = hit_normal  
            cos_theta = ((-1) * unit_direction).dot_product(N)
            r_out_perp = refr_ratio * (unit_direction + cos_theta * N)
            magn = (r_out_perp.magnitude()) ** 2
            r_out_parallel = - math.sqrt(abs(1.0 - magn)) * N
            refr_direction = r_out_perp + r_out_parallel
            # N = hit_normal      # Normal depende se é interna ou externa
            # cosI  = -(N.dot_product(ray.direction))
            # cosT2 = 1.0 - n * n * (1.0 - cosI * cosI)
            # if (cosT2 > 0):
            #     T = (n * ray.direction) + (n * cosI - math.sqrt(cosT2)) * N
            #     r = Ray(hit_pos + T * self.MIN_DISPLACE, T)
            #     rcol, rt, raRIndex = self.ray_trace(r, scene, depth=depth+1, aRIndex=rindex, t=float('inf'), color=Color(0,0,0))
            #     absorb = self.color_at(obj_hit, hit_pos, hit_normal, scene, ray) * 0.15 * -t
            #     transp = Color(
            #         math.exp(absorb.x), 
            #         math.exp(absorb.y), 
            #         math.exp(absorb.z)
            #     )
            r = Ray(hit_pos - N * self.MIN_DISPLACE, refr_direction)
            rcol, rt, raRIndex = self.ray_trace(r, scene, depth=depth+1, aRIndex=aRIndex, t=float('inf'), color=Color(0,0,0))
            rcol = Color(rcol.x, rcol.y, rcol.z)
            color += rcol * refr

        return color, t, aRIndex

    def find_nearest(self, ray, scene):
        t_min = float('inf')
        obj_hit = None
        result = Hit.MISS

        for obj in scene.objects:
            new_t, case = obj.intersects(ray, t_min)
            if (case != Hit.MISS):
                result = case
                obj_hit = obj
                t_min = new_t

        return t_min, obj_hit, result
    
    def color_at(self, obj_hit, hit_pos, normal, scene, ray):
        material = obj_hit.material
        obj_color = obj_hit.color_at(hit_pos)
        to_cam = scene.camera.eye - hit_pos
        color = material.ambient * 0.1 * Color.from_hex("#FFFFFF")
        specular_k = material.exp_specular

        # Cálculos de iluminação
        for light in scene.lights:
            shade = 1.0
            
            # Sombras pontuais
            if (light.type == LightType.POINT and light.ambient == False):
                L = light.position - hit_pos
                dist = L.magnitude()
                L *= 1.0 / dist
                r = Ray(hit_pos + L * self.MIN_DISPLACE, L)
                
                for obj in scene.objects:
                    new_dist, case = obj.intersects(r, dist)
                    if (case != Hit.MISS):
                        shade = 0
                        break 

            if (shade > 0):
                inter_to_light = (light.position - hit_pos).normalize()
                # Difusa
                if (material.diffuse > 0):
                    light_dist = inter_to_light.magnitude()
                    light_attenuation = light.get_attenuation(light_dist)
                    diffuse_coeff = (
                        max(normal.dot_product(inter_to_light),0) 
                        * material.diffuse
                        * shade
                        * light_attenuation
                    )
                    color += (
                        diffuse_coeff
                        * obj_color.color_prod(light.color)
                    )
                
                
                
                # Specular (Blinn-Phong)
                # half_vector = (to_light.direction + to_cam).normalize()
                # color += (
                #     light.color 
                #     * material.specular 
                #     * max(normal.dot_product(half_vector), 0) ** specular_k
                # )
                
                if (material.specular > 0):
                    V = ray.direction
                    R = inter_to_light - 2.0 * inter_to_light.dot_product(normal) * normal
                    dot = V.dot_product(R)
                    if (dot > 0):
                        spec = (dot ** specular_k) * material.specular
                        color += (
                            light.color
                            * spec
                            * shade
                        )
        
        return color

