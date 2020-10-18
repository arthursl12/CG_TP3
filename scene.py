class Scene:
    """Guarda todas as informações para o motor de Raytracing"""
    def __init__(self, camera, objects, width, height):
        self.camera = camera
        self.objects = objects
        self.width = width
        self.height = height