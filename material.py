from color import Color

class Texture:
    def __init__(self, _map, width, height):
        self.map = _map
        
        self.u_scale = width
        self.r_u_scale = 1.0 / width
        self.v_scale = height
        self.r_v_scale = 1.0 / height
    
    def get_texel(self, u, v):
        return map.pixels[v][u]
        

class Material:
    """Cor e as propriedades de luz"""
    def __init__(
        self, 
        color=Color.from_hex("#FFFFFF"), 
        ambient=0.05, 
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
        
        # with open(texture, "rb") as img_file:
        #     im = read_ppm(img_file)
        self.texture = texture
    
    def color_at(self, position):
        return self.color

    def get_texel(self, u, v):
        return texture.get_texel(u,v)
            
    

class ChequeredMaterial:
    """Material xadrezado"""
    def __init__(
        self, color1=Color.from_hex("#FFFFFF"),  
        color2=Color.from_hex("#FFFFFF"), 
        ambient=0.05, 
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
    
    def color_at(self, position):
        if (int((position.x + 5.0) * 3) % 2 == int((position.z * 3) % 2)):
            return self.color1
        else:
            return self.color2