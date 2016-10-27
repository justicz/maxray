from ctypes import *

class Vector3f(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("z", c_float)]

    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

