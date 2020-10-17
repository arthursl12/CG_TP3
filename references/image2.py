# -*- coding: utf-8 -*-
"""
pil_test.py

Esse programa ilustra alguns recursos do PIL
que podem lhe ser úteis no EP3.

"""

import Image

size = (400,300)
background = (255, 0, 0)

# cria uma imagem RGB de tamanho size e fundo background
imgRGB = Image.new("RGB", size, background)

# desenha um quadrado azul, pixel a pixel
for lin in range(50, 250):
    for col in range(100, 300):
        imgRGB.putpixel((col, lin), (0, 0, 255))

# salva e mostra o resultado
imgRGB.save("test_pil.ppm")
imgRGB.show()
