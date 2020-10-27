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
from vector import Vector, vector_from_string, list_from_string, vector_from_list


def main():
    # Parse dos argumentos
    parser = argparse.ArgumentParser()
    parser.add_argument("arquivo_entrada", help="Nome arquivo entrada")
    parser.add_argument("arquivo_saida", help="Nome arquivo saida")
    parser.add_argument(
        "-t",
        "--tamanho",
        action="store",
        nargs="+",
        type=int,
        dest="tamanho",
        help="(Opcional) Tamanho (largura x altura) da imagem de saída (padrão=800x600)",
        default=[800,600]
    )
    args = parser.parse_args()
    print(args.arquivo_entrada)
    print(args.arquivo_saida)
    print(args.tamanho)
    width = args.tamanho[0]
    height = args.tamanho[1]
    
    
    aspect_ratio = float(width) / height
    # Leitura do arquivo de entrada
    # Assumindo que não há comentários
    with open(args.arquivo_entrada) as in_file:
        # Câmera
        cam_pos = vector_from_string(in_file.readline())
        look_at = vector_from_string(in_file.readline())
        up = vector_from_string(in_file.readline())
        fov = float(in_file.readline())
        
        # Luzes
        lights = []
        qtd_lights = int(in_file.readline())
        for i in range(qtd_lights):
            lgt = list_from_string(in_file.readline())
            lgt_pos = vector_from_list(lgt[0:3])
            lgt_color = Color(vector_from_list((lgt[3:6])))
            att = vector_from_list(lgt[6:9])
            lgt_att = [att.x, att.y, att.z]
            lights.append(Light(lgt_pos, lgt_color, lgt_att))
        
        
            

    camera = Camera(cam_pos, look_at, up, fov, aspect_ratio)
    for light in lights:
        print(light.position)
    # parser = argparse.ArgumentParser()
    # parser.add_argument("scene", help="Caminho para cena")
    # args = parser.parse_args()
    # mod = importlib.import_module(args.scene)


    return

    scene = Scene(camera, mod.OBJECTS, mod.LIGHTS, mod.WIDTH, mod.HEIGHT)
    engine = RenderEngine()
    qtd_samples = 1

    # Raytracing & Render
    image = engine.render(scene, qtd_samples)
    os.chdir(os.path.dirname(os.path.abspath(mod.__file__)))
    with open(mod.RENDERED_IMG, "w") as img_file:
        image.write_ppm(img_file, qtd_samples)


if __name__ == "__main__":
    main()
