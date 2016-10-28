from ctypes import *

class Matrix4f(Structure):
    _fields_ = [("m11", c_float), ("m12", c_float), ("m13", c_float), ("m14", c_float),
                ("m21", c_float), ("m22", c_float), ("m23", c_float), ("m24", c_float),
                ("m31", c_float), ("m32", c_float), ("m33", c_float), ("m34", c_float),
                ("m41", c_float), ("m42", c_float), ("m43", c_float), ("m44", c_float)]

    def __init__(self, row1, row2, row3, row4):
        m11, m12, m13, m14 = row1
        m21, m22, m23, m24 = row2
        m31, m32, m33, m34 = row3
        m41, m42, m43, m44 = row4

