import math

class Vector:
    """Vetor de 3 elementos"""
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z
    
    def __str__(self):
        return f"({self.x} , {self.y} ,{self.z})"
    
    def dot_product(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross_product(self, other):
        res = Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x)
        return res
    
    def magnitude(self):
        return math.sqrt(self.dot_product(self))
    
    def normalize(self):
        return self / self.magnitude()
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        assert not isinstance(other, Vector)
        return Vector(self.x * other, self.y * other, self.z * other)
    
    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        assert not isinstance(other, Vector)
        return Vector(self.x / other, self.y / other, self.z / other)
    
    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

def from_string(string):
    """
    Dada uma string com três valores separados por espaço(s), retorna o vetor
    3D correspondente
    """
    coord_list = ' '.join(string.split())   # Elimina espaços consecutivos 
    coord_list = coord_list.split(' ')      # Separa por espaços
    assert len(coord_list) == 3
    return Vector(float(coord_list[0]), float(coord_list[1]), float(coord_list[2]))
    