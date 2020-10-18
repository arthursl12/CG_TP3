from image import Image
from ray import Ray
from point import Point
from color import Color

class RenderEngine:
    """Renderiza os objetos no plano de renderização"""

    MAX_DEPTH = 5
    MIN_DISPLACE = 0.0001

    def render(self, scene):
        width = scene.width
        height = scene.height
        aspect_ratio = float(width) / height

        x0 = -1.0
        x1 = +1.0
        x_step = (x1 - x0) / (width - 1)

        y0 = -1.0 / aspect_ratio
        y1 = +1.0 / aspect_ratio
        y_step = (y1 - y0) / (height - 1)

        camera = scene.camera
        pixels = Image(width, height)

        for j in range(height):
            y = y0 + j * y_step
            for i in range(width):
                x = x0 + i * x_step
                ray = Ray(camera, Point(x,y) - camera)
                pixels.set_pixel(i,j,self.ray_trace(ray, scene))
            print(f"{float(j)/float(height) * 100:3.0f}%", end="\r")
        return pixels
    
    def ray_trace(self, ray, scene, depth=0):
        color = Color(0,0,0)

        # Encontra o objeto mais próximo que o raio intercepta
        dist_hit, obj_hit = self.find_nearest(ray, scene)
        if obj_hit is None:
            return color
        hit_pos = ray.origin + ray.direction * dist_hit
        hit_normal = obj_hit.normal(hit_pos)
        color += self.color_at(obj_hit, hit_pos, hit_normal, scene)

        if depth < self.MAX_DEPTH:
            new_ray_pos = hit_pos + hit_normal * self.MIN_DISPLACE
            new_ray_dir = ray.direction - 2 * ray.direction.dot_product(hit_normal) * hit_normal
            new_ray = Ray(new_ray_pos, new_ray_dir)

            # Atenuar o raio refletido pelo coeficiente de reflexão
            color += self.ray_trace(new_ray, scene, depth+1) * obj_hit.material.reflection


        return color

    def find_nearest(self, ray, scene):
        dist_min = None
        obj_hit = None

        for obj in scene.objects:
            dist = obj.intersects(ray)
            if dist is not None and (obj_hit is None or dist < dist_min):
                dist_min = dist
                obj_hit = obj
        return dist_min, obj_hit
    
    def color_at(self, obj_hit, hit_pos, normal, scene):
        material = obj_hit.material
        obj_color = material.color_at(hit_pos)
        to_cam = scene.camera - hit_pos
        color = material.ambient * Color.from_hex("#000000")
        specular_k = 50

        # Cálculos de iluminação
        for light in scene.lights:
            to_light = Ray(hit_pos, light.position - hit_pos)

            # Difusa
            color += (
                obj_color 
                * material.diffuse 
                * max(normal.dot_product(to_light.direction),0) 
            )
            # Specular (Blinn-Phong)
            half_vector = (to_light.direction + to_cam).normalize()
            color += (
                light.color 
                * material.specular 
                * max(normal.dot_product(half_vector), 0) ** specular_k
            )
        
        return color

