from color import Color
from vector import Vector
from image import read_ppm


class Texture:
    def __init__(self, texture_file, u_vector=Vector(0,0.1,0), v_vector=Vector(0,0,0)):
        self.map = read_ppm(texture_file)
        
        self.width = self.map.width
        self.height = self.map.height
        
        self.u_vector = u_vector
        self.v_vector = v_vector

    
    def get_texel(self, point):
        # print(self.map.pixels[round(v)][round(u)])
        u = point.dot_product(self.u_vector) * self.width
        v = point.dot_product(self.v_vector) * self.height
        v_bound = min(round(v), self.height-1)
        u_bound = min(round(u), self.width-1)
        return self.map.pixels[v_bound][u_bound]
        

class Material:
    """Cor e as propriedades de luz"""
    def __init__(
        self, 
        color=Color.from_hex("#FFFFFF"), 
        ambient=0.0005, 
        diffuse=1.0, 
        specular=1.0, 
        reflection=0.9,
        refraction=0.0,
        refrIndex=1,
        texture=None
    ):
        self.color = color
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection
        self.refraction = refraction
        self.refrIndex = refrIndex
        self.texture = texture
    def color_at(self, position):
        return self.color

    def get_texel(self, point):
        return self.texture.get_texel(point)
            
    

class ChequeredMaterial:
    """Material xadrezado"""
    def __init__(
        self, color1=Color.from_hex("#FFFFFF"),  
        color2=Color.from_hex("#FFFFFF"), 
        ambient=0.0005, 
        diffuse=1.0, 
        specular=1.0, 
        reflection=0.5,
        refraction=0.0,
        refrIndex=1
    ):
        self.color1 = color1
        self.color2 = color2
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.reflection = reflection
        self.refraction = refraction
        self.refrIndex = refrIndex
        self.texture = None
    
    def color_at(self, position):
        if (int((position.x + 5.0) * 3) % 2 == int((position.z * 3) % 2)):
            return self.color1
        else:
            return self.color2
