from color import Color
from vector import Vector
from point import Point
from sphere import Sphere
from scene import Scene
from engine import RenderEngine
from light import Light
from material import Material, ChequeredMaterial

WIDTH = 1280
HEIGHT = 720

RENDERED_IMG = "2balls.ppm"
CAMERA = Vector(-5,3,-10)
OBJECTS = [
    # Plano chão
    Sphere(
        Point(0, -10000.5, 1), 
        10000.0, 
        ChequeredMaterial(
            color1=Color.from_hex("#420500"), 
            color2=Color.from_hex("#e6b87d"),
            ambient=0.2,
            reflection=0.1,
            specular=0.2,
            diffuse=1
        )),
    # Bola Prata
    Sphere(Point(0, 1, 0), 0.6, Material(Color.from_hex("#D3D3D3"), diffuse=0, specular=1, reflection=1)),
    Sphere(Point(0, 3, 0), 0.6, Material(Color.from_hex("#D3D3D3"), diffuse=0, specular=1, reflection=1)),
    Sphere(Point(0, 7, 0), 0.6, Material(Color.from_hex("#D3D3D3"), diffuse=0, specular=1, reflection=1)),
    
    # Bola Rosa
    Sphere(Point(1, 0, 0), 0.6, Material(Color.from_hex("#803980"))),
    Sphere(Point(3, 0, 0), 0.6, Material(Color.from_hex("#803980"))),
    Sphere(Point(7, 0, 0), 0.6, Material(Color.from_hex("#803980"))),
    
    # Bola Verde
    Sphere(Point(0, 0, 1), 0.6, Material(Color.from_hex("#228b22"))),
    Sphere(Point(0, 0, 3), 0.6, Material(Color.from_hex("#228b22"))),
    Sphere(Point(0, 0, 7), 0.6, Material(Color.from_hex("#228b22")))
]
LIGHTS = [
    # Light(Point(1.5,.5,-10), Color.from_hex("#FFFFFF")),
    Light(Point(10, 10, 10), Color.from_hex("#FFFFFF")),
    Light(Point(10, 10, -10), Color.from_hex("#FFFFFF"))
    # Light(Point(1.5,.5,-10), Color.from_hex("#FFFFFF"))
]