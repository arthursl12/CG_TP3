from color import Color

class Light:
    """Luz pontual com uma cor determinada"""
    def __init__(self, position, color=Color.from_hex("#FFFFFF")):
        self.position = position
        self.color = color