#!/usr/bin/env python
"""
"""
from color import Color
from vector import Vector
from point import Point
from sphere import Sphere
from scene import Scene
from camera import Camera
from engine import RenderEngine
from light import Light
from material import Material
import argparse
import importlib
import os

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("scene", help="Caminho para cena")
    args = parser.parse_args()
    mod = importlib.import_module(args.scene)

    aspect_ratio = float(mod.WIDTH) / mod.HEIGHT
    camera = Camera(mod.CAMERA, Vector(0,0,0), Vector(0,1,0), 20, aspect_ratio)
    scene = Scene(camera, mod.OBJECTS, mod.LIGHTS, mod.WIDTH, mod.HEIGHT)
    engine = RenderEngine()
    qtd_samples = 2
    image = engine.render(scene, qtd_samples)

    os.chdir(os.path.dirname(os.path.abspath(mod.__file__)))
    with open(mod.RENDERED_IMG, "w") as img_file:
        image.write_ppm(img_file, qtd_samples)



if __name__ == "__main__":
    main()