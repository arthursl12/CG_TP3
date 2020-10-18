class Image:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pixels = [[None for _ in range(width)] for _ in range(height)]
    
    def set_pixel(self, x, y, col):
        self.pixels[y][x] = col
    
    def write_ppm(self, img_file):
        def to_byte(c):
            return round(max(min(c * 255, 255),0))
        img_file.write(f"P3 {self.width} {self.height}\n255\n")

        for row in self.pixels:
            for color in row:
                img_file.write(f"{to_byte(color.x)} {to_byte(color.y)} {to_byte(color.z)} ")
            img_file.write("\n")