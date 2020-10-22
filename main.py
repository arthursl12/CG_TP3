#!/usr/bin/env python
"""
"""
import argparse
import importlib
import os

from camera import Camera
from color import Color
from engine import RenderEngine
from image import read_ppm
from light import Light
from material import Material
from point import Point
from scene import Scene
from sphere import Sphere
from vector import Vector


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("scene", help="Caminho para cena")
    args = parser.parse_args()
    mod = importlib.import_module(args.scene)

    aspect_ratio = float(mod.WIDTH) / mod.HEIGHT
    camera = Camera(mod.CAMERA, Vector(0,0,0), Vector(0,1,0), 20, aspect_ratio)
    scene = Scene(camera, mod.OBJECTS, mod.LIGHTS, mod.WIDTH, mod.HEIGHT)
    engine = RenderEngine()
    qtd_samples = 1
    
    # Load image
    with open("2balls.ppm", "r") as img_file:
        im = read_ppm(img_file)

    # Raytracing & Render
    # image = engine.render(scene, qtd_samples)
    # os.chdir(os.path.dirname(os.path.abspath(mod.__file__)))
    # with open(mod.RENDERED_IMG, "w") as img_file:
    #     image.write_ppm(img_file, qtd_samples)

    with open('exit.ppm','w') as out:
        im.write_ppm(out, 1)


if __name__ == "__main__":
    main()
