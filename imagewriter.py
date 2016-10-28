from PIL import Image

class ImageDrawer:
    def __init__(self, image_map, size):
        self.image_map = image_map
        self.size = size

    def draw(self, filename):
        print "Python: writing image"
        triple_map = []
        for j in range(self.size[1]):
            for i in range(self.size[0]):
                p = self.image_map[i][j]
                triple_map.append((int(p.x), int(p.y), int(p.z)))
        out = Image.new("RGB", self.size)
        out.putdata(triple_map)
        out.save(filename)
        print "Python: finished writing image"

