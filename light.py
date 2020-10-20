from color import Color

from enum import Enum
class LightType(Enum):
    POINT = 0

class Light:
    """Luz pontual com uma cor determinada"""
    def __init__(self, position, color=Color.from_hex("#FFFFFF")):
        self.position = position
        self.color = color
        self.type = LightType.POINT
