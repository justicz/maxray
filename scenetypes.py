from ctypes import *
from vector import *

# We need to set these to inform the C program about
# what kind of thing we are

# Light types
POINT_LIGHT       = 0
DIRECTIONAL_LIGHT = 1

# SceneObject types
SPHERE            = 0
PLANE             = 1
TRIANGLE_MESH     = 2

# Camera types
PERSPECTIVE_CAM   = 0

# Material types
MATERIAL          = 0
PHONG_MATERIAL    = 1

class Camera(Structure):
    _fields_ = [("kind", c_int),
                ("center", Vector3f),
                ("direction", Vector3f),
                ("up", Vector3f),
                ("angle", c_float),
                ("horizontal", Vector3f),
                ("dist", c_float)]
    def __init__(self):
        pass

class PerspectiveCamera(Camera):
    def __init__(self):
        self.kind = PERSPECTIVE_CAM

    def set_center(self, center):
        self.center = center

    def set_direction(self, direction):
        self.direction = direction

    def set_up(self, up):
        self.up = up

    def set_angle(self, angle):
        self.angle = angle

class Light(Structure):
    _fields_ = [("kind", c_int),
                ("position", Vector3f),
                ("color", Vector3f),
                ("falloff", c_float),
                ("direction", Vector3f)]
    def __init__(self):
        pass

class Lights:
    def __init__(self):
        self.lights = []

    def set_num_lights(self, num_lights):
        self.num_lights = num_lights

    def add_light(self, light):
        assert(isinstance(light, Light))
        self.lights.append(light)

class PointLight(Light):
    def __init__(self):
        self.kind = POINT_LIGHT

    def set_position(self, position):
        self.position = position

    def set_color(self, color):
        self.color = color

    def set_falloff(self, falloff):
        self.falloff = falloff

class DirectionalLight(Light):
    def __init__(self):
        self.kind = DIRECTIONAL_LIGHT

    def set_direction(self, direction):
        self.direction = direction

    def set_color(self, color):
        self.color = color

class Background(Structure):
    _fields_ = [("color", Vector3f),
                ("ambient_light", Vector3f),
                ("cube_map", c_char_p)]
    def __init__(self):
        pass

    def set_color(self, color):
        self.color = color

    def set_ambient_light(self, ambient_light):
        self.ambient_light = ambient_light

    def set_cube_map(self, cube_map):
        self.cube_map = cube_map

class SceneObject(Structure):
    _fields_ = [("kind", c_int),
                ("obj_file", c_char_p),
                ("center", Vector3f),
                ("radius", c_float),
                ("normal", Vector3f),
                ("offset", c_float),
                ("material_index", c_int)]

    def __init__(self):
        pass

    def set_material_index(self, material_index):
        self.material_index = material_index

# TODO: Implement Transform
class Transform(SceneObject):
#    _fields_ = [("translate", Vector3f),
#                ("scale", Vector3f),
#                ("material_index", c_int),
#                ("z_rotate", c_float),
#                ("y_rotate", c_float),
#                ("x_rotate", c_float)]
    def __init__(self):
        pass

    def set_translate(self, translate):
        self.translate = translate

    def set_scale(self, scale):
        self.scale = scale

    def set_material_index(self, material_index):
        self.material_index = material_index

    def set_z_rotate(self, z_rotate):
        self.z_rotate = z_rotate

    def set_y_rotate(self, y_rotate):
        self.y_rotate = y_rotate

    def set_x_rotate(self, x_rotate):
        self.x_rotate = x_rotate

class TriangleMesh(SceneObject):
    def __init__(self):
        self.kind = TRIANGLE_MESH

    def set_obj_file(self, obj_file):
        self.obj_file = obj_file.encode("utf-8")

class Sphere(SceneObject):
    def __init__(self):
        self.kind = SPHERE

    def set_center(self, center):
        self.center = center

    def set_radius(self, radius):
        self.radius = radius

class Plane(SceneObject):
    def __init__(self):
        self.kind = PLANE

    def set_normal(self, normal):
        self.normal = normal

    def set_offset(self, offset):
        self.offset = offset

class Materials:
    def __init__(self):
        self.materials = []

    def set_num_materials(self, num_materials):
        self.num_materials = num_materials

    def add_material(self, material):
        assert(isinstance(material, Material))
        self.materials.append(material)

class Group(Structure):
    def __init__(self):
        self.objects = []

    def set_num_objects(self, num):
        self.num_objects = num

    def add_object(self, obj):
        self.objects.append(obj)

class Material(Structure):
    _fields_ = [("kind", c_int),
                ("diffuse_color", Vector3f),
                ("specular_color", Vector3f),
                ("shininess", c_float)]
    def __init__(self):
        self.kind = MATERIAL

    def set_diffuse_color(self, color):
        self.diffuse_color = color

    def set_specular_color(self, color):
        self.specular_color = color

    def set_shininess(self, shininess):
        self.shininess = shininess

class PhongMaterial(Material):
    def __init__(self):
        self.kind = PHONG_MATERIAL

class Scene:
    def __init__(self):
        pass

    def set_camera(self, camera):
        self.camera = camera

    def set_group(self, group):
        self.group = group

    def set_lights(self, lights):
        self.lights = lights

    def set_materials(self, materials):
        self.materials = materials

    def set_background(self, background):
        self.background = background
