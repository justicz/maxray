from ctypes import *
import vector
import math

class Matrix4f(Structure):
    _fields_ = [("m11", c_float), ("m12", c_float), ("m13", c_float), ("m14", c_float),
                ("m21", c_float), ("m22", c_float), ("m23", c_float), ("m24", c_float),
                ("m31", c_float), ("m32", c_float), ("m33", c_float), ("m34", c_float),
                ("m41", c_float), ("m42", c_float), ("m43", c_float), ("m44", c_float)]

    def __init__(self, row1, row2, row3, row4):
        self.m11, self.m12, self.m13, self.m14 = row1
        self.m21, self.m22, self.m23, self.m24 = row2
        self.m31, self.m32, self.m33, self.m34 = row3
        self.m41, self.m42, self.m43, self.m44 = row4

    def get_rows(self):
        return [[self.m11, self.m12, self.m13, self.m14],
                [self.m21, self.m22, self.m23, self.m24],
                [self.m31, self.m32, self.m33, self.m34],
                [self.m41, self.m42, self.m43, self.m44]]

    def get_cols(self):
        return [[self.m11, self.m21, self.m31, self.m41],
                [self.m12, self.m22, self.m32, self.m42],
                [self.m13, self.m23, self.m33, self.m43],
                [self.m14, self.m24, self.m34, self.m44]]

    def apply_l(self, other):
        self.__init__(*(Matrix4fHelper.multiply(other, self).get_rows()))

    def apply_r(self, other):
        self.__init__(*(Matrix4fHelper.multiply(self, other).get_rows()))

class Matrix4fHelper(Structure):
    @staticmethod
    def x_rotation(deg):
        rad = math.radians(deg)
        row1 = [1, 0, 0, 0]
        row2 = [0, math.cos(rad), -math.sin(rad), 0]
        row3 = [0, math.sin(rad), math.cos(rad), 0]
        row4 = [0, 0, 0, 1]
        return Matrix4f(row1, row2, row3, row4)

    @staticmethod
    def y_rotation(deg):
        rad = math.radians(deg)
        row1 = [math.cos(rad), 0, math.sin(rad), 0]
        row2 = [0, 1, 0, 0]
        row3 = [-math.sin(rad), 0, math.cos(rad), 0]
        row4 = [0, 0, 0, 1]
        return Matrix4f(row1, row2, row3, row4)

    @staticmethod
    def z_rotation(deg):
        rad = math.radians(deg)
        row1 = [math.cos(rad), -math.sin(rad), 0, 0]
        row2 = [math.sin(rad), math.cos(rad), 0, 0]
        row3 = [0, 0, 1, 0]
        row4 = [0, 0, 0, 1]
        return Matrix4f(row1, row2, row3, row4)

    @staticmethod
    def translation(trans):
        row1 = [1, 0, 0, trans.x]
        row2 = [0, 1, 0, trans.y]
        row3 = [0, 0, 1, trans.z]
        row4 = [0, 0, 0, 1]
        return Matrix4f(row1, row2, row3, row4)

    @staticmethod
    def scale(scale):
        row1 = [scale.x, 0, 0, 0]
        row2 = [0, scale.y, 0, 0]
        row3 = [0, 0, scale.z, 0]
        row4 = [0, 0, 0, 1]
        return Matrix4f(row1, row2, row3, row4)

    @staticmethod
    def transpose(inm):
        return Matrix4f(*inm.get_cols())

    @staticmethod
    def multiply(left, right):
        myrows = [vector.Vector4f(*r) for r in left.get_rows()]
        otcols = [vector.Vector4f(*c) for c in right.get_cols()]
        out = [[0]*4 for i in range(4)]
        for i, row in enumerate(myrows):
            for j, col in enumerate(otcols):
                out[i][j] = row.dot(col)
        return Matrix4f(*out)

