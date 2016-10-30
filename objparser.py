from vector import *

class ObjectFile:
    def __init__(self, obj_file):
        self.obj_file = obj_file
        self.parse()

    def parse(self):
        vertices = []
        faces = []
        with open(self.obj_file) as fin:
            for line in fin.readlines():
                l = line.split(" ")
                if line[0] == "v":
                    x, y, z = l[1:]
                    vertices.append(Vector3f(x, y, z))
                if line[0] == "f":
                    i0, i1, i2 = l[1:]
                    i0, i1, i2 = int(i0), int(i1), int(i2)
                    faces.append([i0 - 1, i1 - 1, i2 - 1])

        self.vertices = vertices
        self.face_indices = faces
