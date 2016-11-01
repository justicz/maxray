from PIL import Image

UP    = "up"
DOWN  = "down"
LEFT  = "left"
RIGHT = "right"
FRONT = "front"
BACK  = "back"
FACES = [UP, DOWN, LEFT, RIGHT, FRONT, BACK]

class Skybox:
    def __init__(self, faces):
        self.faces = faces

def load(prefix, cube_map, size):
    path = prefix + "/" + cube_map + "/"
    out = []
    for name in FACES:
        im = Image.open(path + name + ".png")
        im.thumbnail(size, Image.ANTIALIAS)
        im = im.convert('RGB')
        out.append(im)
    return out

