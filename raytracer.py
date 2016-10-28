from scenetypes import *
from ctypes import *
from vector import *
import os

SCRIPT_DIR = os.path.split(os.path.realpath(__file__))[0]
raylib = CDLL(SCRIPT_DIR + "/ray.so")

class RayTracer:
    def __init__(self, scene, args):
        self.scene = scene
        self.args = args

    def run(self):
        print "Python: setting scene size"
        raylib.set_size(self.args.size[0], self.args.size[1])
        print "Python: calling init_scene"
        raylib.init_scene(byref(self.scene))
        print "Python: calling raytrace"
        raylib.raytrace.restype = POINTER(POINTER(Vector3f))
        return raylib.raytrace()

