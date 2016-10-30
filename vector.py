from ctypes import *

class Vector3f(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("z", c_float)]

    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

class Vector4f(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("z", c_float),
                ("w", c_float)]

    def __init__(self, x, y, z, w):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        self.w = float(w)

    def dot(self, other):
        return self.x * other.x + \
               self.y * other.y + \
               self.z * other.z + \
               self.w * other.w

