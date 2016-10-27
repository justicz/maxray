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

    def set_group(self, group):
        objects = group.objects
        for obj in objects:
            if isinstance(obj, SceneObject):
                raylib.add_scene_object(byref(obj))
            elif isistnace(obj, Group):
                self.send_group(obj)

    def set_camera(self, camera):
        assert(isinstance(camera, Camera))
        raylib.add_camera(byref(camera))

    def set_lights(self, lights):
        for light in lights.lights:
            assert(isinstance(light, Light))
            raylib.add_light(byref(light))

    def set_materials(self, materials):
        for mat in materials.materials:
            assert(isinstance(mat, Material))
            raylib.add_material(byref(mat))

    def set_background(self, background):
        assert(isinstance(background, Background))
        raylib.add_background(byref(background))

    def set_size(self, w, h):
        raylib.set_size(w, h);

    def raytrace(self):
        raylib.raytrace.restype = POINTER(POINTER(Vector3f))
        return raylib.raytrace()

    def set_flags(self):
        if self.flags["-shadows"]:
            raylib.set_shadows()
        if self.flags["-bounces"]:
            raylib.set_bounces(self.flags["-bounces"])

    def run(self):
        scene = self.scene
        self.set_camera(scene.camera)
        self.set_group(scene.group)
        self.set_lights(scene.lights)
        self.set_materials(scene.materials)
        self.set_background(scene.background)
        self.set_size(self.args.size[0], self.args.size[1])
        # self.set_args(self.args)
        return self.raytrace()

