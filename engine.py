import math
from image import Image
from camera import Camera
from vector import Vector
from ray import Ray
from point import Point
from color import Color
from sphere import Hit
from light import LightType

class RenderEngine:
    """Renderiza os objetos no plano de renderização"""

    MAX_DEPTH = 5
    MIN_DISPLACE = 0.0001

    def render(self, scene):
        width = scene.width
        height = scene.height
        aspect_ratio = float(width) / height

        # camera = scene.camera
        camera = scene.camera
        ## TODO: tratamento do ângulo para (1) não poder ser 90° e (2) não ter tangente negativa
        pixels = Image(width, height)

        for j in reversed(range(height)):
            for i in reversed(range(width)):
                u = float(i) / (width-1)
                v = float(j) / (height-1)
                ray = camera.get_ray(u, v)
                color, dist = self.ray_trace(ray, scene)
                pixels.set_pixel(i, j, color)
            print(f"{float(height-j)/float(height) * 100:3.0f}%", end="\r")
        return pixels
    
    def ray_trace(self, ray, scene, depth=0, aRIndex=1, dist=float('inf'), color=Color(0,0,0)):
        # Encontra o objeto mais próximo que o raio intercepta
        dist, obj_hit, case = self.find_nearest(ray, scene)
        if obj_hit is None:
            return color, dist
        hit_pos = ray.origin + ray.direction * dist
        hit_normal = obj_hit.normal(hit_pos)
        color += self.color_at(obj_hit, hit_pos, hit_normal, scene, ray)

        # Cálculo da Reflexão
        if (depth < self.MAX_DEPTH and obj_hit.material.reflection > 0):
            new_ray_pos = hit_pos + hit_normal * self.MIN_DISPLACE
            new_ray_dir = ray.direction - 2 * ray.direction.dot_product(hit_normal) * hit_normal
            new_ray = Ray(new_ray_pos, new_ray_dir)

            # Atenuar o raio refletido pelo coeficiente de reflexão
            rcol, dist = self.ray_trace(new_ray, scene, depth+1)
            color += rcol * obj_hit.material.reflection
            color += obj_hit.material.reflection * obj_hit.material.color_at(hit_pos) * 0.3

        # Cálculo da Refração
        if (depth < self.MAX_DEPTH and obj_hit.material.refraction > 0):
            refr = obj_hit.material.refraction
            rindex = obj_hit.material.refrIndex
            n = aRIndex / rindex
            N = hit_normal * (float)(case.value)      # Normal depende se é interna ou externa
            cosI  = -(N.dot_product(ray.direction))
            cosT2 = 1.0 - n * n * (1.0 - cosI * cosI)
            if (cosT2 > 0):
                T = (n * ray.direction) + (n * cosI - math.sqrt(cosT2)) * N
                r = Ray(hit_pos + T * self.MIN_DISPLACE, T)
                rcolor, dist = self.ray_trace(r, scene, depth+1, rindex)
                # absorb = self.color_at(obj_hit, hit_pos, hit_normal, scene, ray) * 0.0009 * -dist
                # transp = Color(
                #     math.exp(absorb.x), 
                #     math.exp(absorb.y), 
                #     math.exp(absorb.z)
                # )
                # color += rcolor * transp  
                # color += rcolor.cross_product(transp)
                color += rcolor
                # color += transp  
        return color, dist

    def find_nearest(self, ray, scene):
        dist_min = float('inf')
        obj_hit = None
        result = 0

        for obj in scene.objects:
            new_dist, case = obj.intersects(ray, dist_min)
            if (case != Hit.MISS):
                result = case
                obj_hit = obj
                dist_min = new_dist

        return dist_min, obj_hit, case
    
    def color_at(self, obj_hit, hit_pos, normal, scene, ray=Vector(0,0,0)):
        material = obj_hit.material
        obj_color = material.color_at(hit_pos)
        to_cam = scene.camera.eye - hit_pos
        color = material.ambient * Color.from_hex("#000000")
        specular_k = 50

        # Cálculos de iluminação
        for light in scene.lights:
            shade = 1.0
            
            # Sombras pontuais
            if (light.type == LightType.POINT):
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
                    diffuse_coeff = (
                        max(normal.dot_product(inter_to_light),0) 
                        * material.diffuse
                    )
                    color += (
                        diffuse_coeff
                        * obj_color
                        * shade
                    )
                    # color += (
                    #     diffuse_coeff
                    #     * light.color
                    #     * 0.1
                    # )
                
                
                
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
                        spec = (dot ** 20) * material.specular
                        color += (
                            light.color
                            * spec
                            * shade
                        )
        
        return color

