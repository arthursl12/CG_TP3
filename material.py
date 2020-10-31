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
        u = abs(point.dot_product(self.u_vector)) * self.width
        v = abs(point.dot_product(self.v_vector)) * self.height
        v_bound = round(v) % self.height
        u_bound = round(u) % self.width
        return self.get_pixel(u_bound, v_bound)
    
    def get_pixel(self, u, v):
        return self.map.pixels[v][u]
        

class Material:
    """Cor e as propriedades de luz"""
    def __init__(
        self, 
        color=Color.from_hex("#FFFFFF"), 
        ambient=0.0005, 
        diffuse=1.0, 
        specular=1.0,
        exp_specular=20,
        reflection=0.9,
        refraction=0.0,
        ior=0,
        texture=None
    ):
        self.color = color
        self.ambient = ambient              # ka
        self.diffuse = diffuse              # kd
        self.specular = specular            # ks
        self.exp_specular = exp_specular    # alpha

        self.reflection = reflection        # kr
        self.refraction = refraction        # kt   
        self.ior = ior                      # ior
        self.texture = texture

    def color_at(self, position):
        return self.color

    def get_texel(self, point):
        return self.texture.get_texel(point)

    def set_acabamento(self, ka, kd, ks, alpha, kr, kt, ior):
        """
        Parâmetros:
        ka      - coeficiente de luz ambiente
        kd      - coeficiente de luz difusa
        ks      - coeficiente de luz especular
        alpha   - expoente da reflexão especular
        kr      - coeficiente de reflexão
        kt      - coeficiente de transmissão (refração)
        ior     - taxa entre índices de refração ambiente e material (n1/n2)
        """
        self.ambient = ka
        self.diffuse = kd
        self.specular = ks
        self.exp_specular = alpha
        self.reflection = kr
        self.refraction = kt
        self.ior = ior
            
    

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
        ior=0,
        exp_specular=20,
        tamanho=15
    ): 
        self.color1 = color1
        self.color2 = color2
        self.ambient = ambient              # ka
        self.diffuse = diffuse              # kd
        self.specular = specular            # ks
        self.exp_specular = exp_specular    # alpha

        self.reflection = reflection        # kr
        self.refraction = refraction        # kt
     
        self.ior = ior                      # ior
        self.texture = None
        self.tamanho = tamanho
        
    def set_acabamento(self, ka, kd, ks, alpha, kr, kt, ior):
        """
        Parâmetros:
        ka      - coeficiente de luz ambiente
        kd      - coeficiente de luz difusa
        ks      - coeficiente de luz especular
        alpha   - expoente da reflexão especular
        kr      - coeficiente de reflexão
        kt      - coeficiente de transmissão (refração)
        ior     - taxa entre índices de refração ambiente e material (n1/n2)
        """
        self.ambient = ka
        self.diffuse = kd
        self.specular = ks
        self.exp_specular = alpha
        self.reflection = kr
        self.refraction = kt
        self.ior = ior
        
    def color_at(self, position): 
        modX = int(position.x) % (self.tamanho * 2.5)
        modZ = int(position.z) % (self.tamanho * 2.5)
        
        def corX(modX):
            return (modX <= self.tamanho/4 or modX > self.tamanho * 1.5)
        def corZ(modZ):
            return (modZ <= self.tamanho/4 or modZ > self.tamanho * 1.5)
        
        if (corX(modX) != corZ(modZ)):
            return self.color1
        else:
            return self.color2
