from modules.color import Color


class Image:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [[None for _ in range(width)] for _ in range(height)]
    
    def set_pixel(self, x, y, col):
        self.pixels[y][x] = col
    
    def add_pixel(self, x, y, col):
        if self.pixels[y][x] is None:
            self.set_pixel(x, y, col)
        else:
            self.pixels[y][x] += col
    
    def write_ppm(self, img_file, qtd_samples):
        def to_byte(c):
            return round(max(min(c * 255, 255),0))
        img_file.write(f"P3\n{self.width} {self.height}\n255\n")

        for row in self.pixels:
            for color in row:
                fator_media = 1.0 / qtd_samples
                color *= fator_media
                img_file.write(f"{to_byte(color.x)} {to_byte(color.y)} {to_byte(color.z)} ")
            img_file.write("\n")

def read_ppm(file_name):
    with open(file_name, "r", errors='ignore') as img_file:
        cabeca = False
        while not cabeca:
            line = img_file.readline()
            if line.strip()[0] == '#':
                continue
            else:
                cabecalho = line.strip()
                cabeca = True
    if (cabecalho == "P3"):
        with open(file_name, "r") as img_file:
            im = read_ppm_p3(img_file)
        return im
    elif (cabecalho == "P6"):
        with open(file_name, "rb") as img_file:
            im = read_ppm_p6(img_file)
        return im
    

def read_ppm_p3(img_file):
    lines = img_file.readlines()
    count = 0

    for line in lines:
        if line.strip()[0] == '#':
            continue

        if count == 0:
            cabecalho = line.strip()
            count += 1
        elif count == 1:
            size = line.strip()
            count += 1
        elif count == 2:
            max_color = line.strip()
            count += 1
        else:
            # print("Line{}: {}".format(count, line.strip())) 
            break

    assert cabecalho == "P3"

    size = ' '.join(size.split())
    size_list = size.split(' ')
    width = int(size_list[0])
    height = int(size_list[1])

    im = Image(width, height)

    count = 0
    curr_width = 0
    curr_height = 0
    for line in lines:
        if line.strip()[0] == '#':
            continue
        if count >= height + 3:
            break

        if count <= 2:
            count += 1
        else:
            curr_line = line.strip()
            curr_height = count - 3
            # print("Line {}, H = {}".format(count, curr_height))
            simple_spaces = ' '.join(curr_line.split())
            colors = simple_spaces.split(' ')

            for i in range(width):
                idx_r = 3*i
                r = float(colors[idx_r]  ) / float(max_color)
                g = float(colors[idx_r+1]) / float(max_color)
                b = float(colors[idx_r+2]) / float(max_color)

                im.set_pixel(i, curr_height, Color(r,g,b))
            count += 1
    return im 

def read_ppm_p6(img_file):
    lines = img_file.readlines()
    count = 0

    for line in lines:
        if line.decode(errors="ignore").strip()[0] == '#':
            continue
        
        if count == 0:
            cabecalho = line.strip()
            count += 1
        elif count == 1:
            size = line.strip()
            count += 1
        elif count == 2:
            max_color = line.strip()
            count += 1
        else:
            break
    
    
    cabecalho = cabecalho.decode()
    size = size.decode()
    max_color = int(max_color.decode())
    
    size = ' '.join(size.split())
    size_list = size.split(' ')
    width = int(size_list[0])
    height = int(size_list[1])
    
    im = Image(width, height)
    if (cabecalho == "P3"):
        raise("Formato inválido de ppm")
    elif(cabecalho == "P6"):
        byte_line = lines[count+1]
        for line in lines:
            if line.decode(errors="ignore").strip()[0] == '#':
                continue
            
            if count <= 2:
                count += 1
            else:
                curr_line = line.strip()
                byte_line = curr_line
        for j in range(height):
            for i in range(width):
                idx_r = 3*(i + width * j)
                r = float(byte_line[idx_r]  ) / float(max_color)
                g = float(byte_line[idx_r+1]) / float(max_color)
                b = float(byte_line[idx_r+2]) / float(max_color)
                im.set_pixel(i, j, Color(r,g,b))
        return im
    else:
        raise("Formato inválido de ppm")
