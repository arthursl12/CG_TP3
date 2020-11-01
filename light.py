from color import Color

from enum import Enum
class LightType(Enum):
    POINT = 0

class Light:
    """Luz pontual com uma cor determinada"""
    def __init__(self, position, color=Color.from_hex("#FFFFFF"), attenuation=[1,0,0], ambient=False):
        self.position = position
        self.color = color
        self.type = LightType.POINT
        self.attenuation = attenuation
        self.ambient = ambient
    
    def get_attenuation(self, dist):
        fator  = self.attenuation[0]
        fator += self.attenuation[1] * dist
        fator += self.attenuation[2] * (dist ** 2)
        if fator == 0:
            return 1
        fator = min(1.0 / fator, 1)
        return fator
