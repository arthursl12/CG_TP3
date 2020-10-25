from vector import Vector

class Color(Vector):
    """
    Guarda uma cor como uma tripla RGB. Armazenada como vetor 3D
    Entre 0 e 1
    """
    @classmethod
    def from_hex(cls, hexcolor="#000000"):
        x = int(hexcolor[1:3], 16) / 255.0
        y = int(hexcolor[3:5], 16) / 255.0
        z = int(hexcolor[5:7], 16) / 255.0
        return cls(x, y, z)

    def color_prod(self, other):
        r = self.x * other.x
        g = self.y * other.y
        b = self.z * other.z
        return Color(r,g,b)