#!/usr/bin/env python
"""
"""
import argparse
import copy
import importlib
import os

from camera import Camera
from color import Color
from engine import RenderEngine
from image import read_ppm
from light import Light
from material import ChequeredMaterial, Material, Texture
from point import Point
from polyhedron import Polyhedron
from scene import Scene
from sphere import Sphere
from vector import (Vector, list_from_string, vector_from_list,
                    vector_from_string)


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
        primeira = True
        for i in range(qtd_lights):
            lgt = list_from_string(in_file.readline())
            lgt_pos = vector_from_list(lgt[0:3])
            color_vec = vector_from_list((lgt[3:6]))
            lgt_color = Color(
                color_vec.x,
                color_vec.y,
                color_vec.z
            )
            att = vector_from_list(lgt[6:9])
            lgt_att = [att.x, att.y, att.z]
            if (primeira):
                lights.append(Light(lgt_pos, lgt_color, lgt_att, ambient=True))
                primeira = False
            else:
                lights.append(Light(lgt_pos, lgt_color, lgt_att, ambient=True))
        
        # Materiais
        # Pigmentos
        pigms = []
        qtd_pigms = int(in_file.readline())
        for i in range(qtd_pigms):
            pigm = list_from_string(in_file.readline())
            if (pigm[0] == "texmap"):
                text_file = pigm[1]
                p0 = list_from_string(in_file.readline())
                p0 = Vector(float(p0[0]), float(p0[1]), float(p0[2]))
                p1 = list_from_string(in_file.readline())
                p1 = Vector(float(p1[0]), float(p1[1]), float(p1[2]))
                text = Texture(text_file, u_vector=p0, v_vector=p1)
                texture_mat = Material(color=Color.from_hex("#000000"), texture=text)
                pigms.append(texture_mat)
            elif (pigm[0] == "checker"):
                cor1 = Color(
                    float(pigm[1]), 
                    float(pigm[2]),
                    float(pigm[3])
                )
                cor2 = Color(
                    float(pigm[4]), 
                    float(pigm[5]),
                    float(pigm[6])
                )
                tam = float(pigm[7])
                ## TODO: implementar tamanho no xadrez
                check = ChequeredMaterial(color1=cor1, color2=cor2)
                pigms.append(check)
            elif (pigm[0] == "solid"):
                color = Color(
                    float(pigm[1]), 
                    float(pigm[2]),
                    float(pigm[3])
                )
                solid = Material(color=color)
                pigms.append(solid)
        
        # Acabamentos
        acabs = []
        qtd_acabs = int(in_file.readline())
        for i in range(qtd_acabs):
            acab_list = list_from_string(in_file.readline())
            assert len(acab_list) == 7
            for j in range(len(acab_list)):
                acab_list[j] = float(acab_list[j])
            acabs.append(acab_list)
        
        # Objetos
        objects = []
        qtd_objs = int(in_file.readline())
        for i in range(qtd_objs):
            obj_descr = list_from_string(in_file.readline())
            if (obj_descr[2] == "sphere"):
                mat = int(obj_descr[0])
                acab = int(obj_descr[1])
                centro = Vector(
                    float(obj_descr[3]), 
                    float(obj_descr[4]), 
                    float(obj_descr[5])
                )
                raio = float(obj_descr[6])
                new_material = copy.deepcopy(pigms[mat])
                new_acab = copy.deepcopy(acabs[acab])
                new_material.set_acabamento(
                    new_acab[0],
                    new_acab[1],
                    new_acab[2],
                    new_acab[3],
                    new_acab[4],
                    new_acab[5],
                    new_acab[6]
                )
                # new_material.color = Color.from_hex("#FFF3F3")
                esfera = Sphere(centro, raio, new_material)
                objects.append(esfera)
            elif (obj_descr[2] == "polyhedron"):
                mat = int(obj_descr[0])
                acab = int(obj_descr[1])
                qtd_faces = int(obj_descr[3])
                
                planos = []
                for j in range(qtd_faces):
                    face_descr = list_from_string(in_file.readline())
                    assert len(face_descr) == 4
                    planos.append([
                        float(face_descr[0]),
                        float(face_descr[1]),
                        float(face_descr[2]),
                        -float(face_descr[3]),
                    ])
                new_material = copy.deepcopy(pigms[mat])
                new_acab = copy.deepcopy(acabs[acab])
                new_material.set_acabamento(
                    new_acab[0],
                    new_acab[1],
                    new_acab[2],
                    new_acab[3],
                    new_acab[4],
                    new_acab[5],
                    new_acab[6]
                )
                poly = Polyhedron(planos, new_material)
                objects.append(poly)
                

    # Montagem da cena
    camera = Camera(cam_pos, look_at, up, fov, aspect_ratio)
    scene = Scene(camera, objects, lights, width, height)
    engine = RenderEngine()
    qtd_samples = 1

    # Raytracing & Render
    image = engine.render(scene, qtd_samples)
    with open(args.arquivo_saida, "w") as img_file:
        image.write_ppm(img_file, qtd_samples)


if __name__ == "__main__":
    main()
