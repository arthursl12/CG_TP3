#!/usr/bin/env python
"""
"""
import argparse
import copy
import importlib
import os
import pathlib
import tempfile

from modules.camera import Camera
from modules.color import Color
from modules.engine import RenderEngine
from modules.image import read_ppm
from modules.light import Light
from modules.material import ChequeredMaterial, Material, Texture
from modules.plane import Plane
from modules.point import Point
from modules.scene import Scene
from modules.sphere import Sphere
from modules.vector import (Vector, list_from_string, vector_from_list,
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
    FPS = 5
    
    aspect_ratio = float(width) / height
    # Leitura do arquivo de entrada
    # Assumindo que não há comentários
    with open(args.arquivo_entrada) as in_file:
        first = list_from_string(in_file.readline())
        movimento = False
        if (len(first) < 3):
            # Câmera em movimento
            movimento = True
            qtd_posicoes = int(first[0])
            total_segs = int(first[1])
            total_frames = FPS * total_segs
            
            # Tempo das transições
            transicoes = list_from_string(in_file.readline())
            assert len(transicoes) == (qtd_posicoes-1)
            tempo_transicoes = []
            soma = 0
            for i in range(len(transicoes)):
                trans = (float)(transicoes[i])
                tempo_transicoes.append(trans)
                soma += trans
            print(tempo_transicoes)
            print(f"{soma} ?= {total_segs}")
            assert soma == total_segs

            # Posições da câmera
            posicoes = []
            for i in range(qtd_posicoes):
                _cam_pos = vector_from_string(in_file.readline())
                _look_at = vector_from_string(in_file.readline())
                _up = vector_from_string(in_file.readline())
                _fov = float(in_file.readline())
                pos = {
                    "cam_pos": _cam_pos,
                    "look_at": _look_at,
                    "up": _up,
                    "fov": _fov
                }
                posicoes.append(pos)
            
        else:
            # Câmera estática
            movimento = False
            # Câmera
            cam_pos = vector_from_list(first)
            look_at = vector_from_string(in_file.readline())
            up = vector_from_string(in_file.readline())
            fov = float(in_file.readline())
        
        # Luzes
        lights = []
        qtd_lights = int(in_file.readline())
        print(qtd_lights)
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
                lights.append(Light(lgt_pos, lgt_color, lgt_att, ambient=False))
        
        # Materiais
        # Pigmentos
        pigms = []
        qtd_pigms = int(in_file.readline())
        print(qtd_pigms)
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
                img = texture_mat.texture.map
                with open('test.ppm','w') as test:
                    img.write_ppm(test, 1)
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
                print(tam)
                check = ChequeredMaterial(color1=cor1, color2=cor2, tamanho=tam)
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
        print(qtd_acabs)
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
                # poly = Polyhedron(planos, new_material)
                plano = Plane(planos[0], new_material)
                objects.append(plano)

    # Montagem da cena
    if movimento:
        import shutil

        import imageio
        images = []
        filenames = []
        dirpath = tempfile.mkdtemp()
        frames_process = 0
        for j in range(len(tempo_transicoes)):
            frames_secao = (int)(tempo_transicoes[j] * FPS)
            for i in range(frames_secao):
                cam_passo = (posicoes[j+1]["cam_pos"] - posicoes[j]["cam_pos"]) / frames_secao
                look_at_passo = (posicoes[j+1]["look_at"] - posicoes[j]["look_at"]) / frames_secao
                up_passo = (posicoes[j+1]["up"] - posicoes[j]["up"]) / frames_secao
                fov_passo = (posicoes[j+1]["fov"] - posicoes[j]["fov"]) / frames_secao
                
                cam_pos = posicoes[j]["cam_pos"] + i * cam_passo
                look_at = posicoes[j]["look_at"] + i * look_at_passo
                up = posicoes[j]["up"] + i * up_passo
                fov = posicoes[j]["fov"] + i * fov_passo
                camera = Camera(cam_pos, look_at, up, fov, aspect_ratio)
                scene = Scene(camera, objects, lights, width, height)
                engine = RenderEngine()
                qtd_samples = 1

                # Raytracing & Render
                image = engine.render(scene, qtd_samples)
                file_name = dirpath + f"temp{i}-{j}.ppm"
                filenames.append(file_name)
                with open(file_name, "w") as img_file:
                    image.write_ppm(img_file, qtd_samples)
                    
                frames_process += 1
                print(f"{float(frames_process)/float(total_frames) * 100:3.0f}%") 
            
        print("Gerando GIF")      
        for filename in filenames:
            images.append(imageio.imread(filename))
        saida = args.arquivo_saida[0:-4]
        saida += ".gif"
        saida = os.path.abspath(saida) 
        print(saida)
        imageio.mimsave(saida, images, "GIF", fps=FPS)
        shutil.rmtree(dirpath)
    else:
        camera = Camera(cam_pos, look_at, up, fov, aspect_ratio)
        scene = Scene(camera, objects, lights, width, height)
        engine = RenderEngine()
        qtd_samples = 1

        # Raytracing & Render
        image = engine.render(scene, qtd_samples)
        saida = os.path.abspath(args.arquivo_saida) 
        print(saida)
        with open(saida, "w") as img_file:
            image.write_ppm(img_file, qtd_samples)


if __name__ == "__main__":
    main()
