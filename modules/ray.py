class Ray:
    """Ray é uma semirreta, com origem e uma direção (normalizada)"""
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = direction.normalize()
    