from ctypes import *
from vector import *
from matrix import *

# We need to set these to inform the C program about
# what kind of thing we are

# Light types
POINT_LIGHT       = 0
DIRECTIONAL_LIGHT = 1

# SceneObject types
SPHERE            = 0
PLANE             = 1
TRIANGLE_MESH     = 2
GROUP             = 3
TRANSFORM         = 4

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

class Lights(Structure):
    _fields_ = [("num_lights", c_int),
                ("lights", POINTER(POINTER(Light)))]
    def __init__(self):
        self.p_lights = []

    def set_num_lights(self, num_lights):
        self.num_lights = num_lights

    def add_light(self, light):
        assert(isinstance(light, Light))
        self.p_lights.append(light)

    def set_lights_pointers(self):
        self.num_lights = len(self.p_lights)
        res = (POINTER(Light) * self.num_lights)()
        for i, child in enumerate(self.p_lights):
            res[i] = cast(pointer(child), POINTER(Light))
        self.lights = cast(res, POINTER(POINTER(Light)))

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
    def __init__(self):
        self.p_children = []
        self.transform = Matrix4f([1, 0, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, 1])

    def set_material_index(self, material_index):
        self.material_index = material_index

    def add_child_object(self, obj):
        assert(isinstance(obj, SceneObject))
        self.p_children.append(obj)

    def set_children_pointers(self):
        self.num_children = len(self.p_children)

        if self.num_children == 0:
            return

        res = (POINTER(SceneObject) * self.num_children)()
        for i, child in enumerate(self.p_children):
            res[i] = cast(pointer(child), POINTER(SceneObject))

        self.children = cast(pointer(res), POINTER(POINTER(SceneObject)))


# We have to put this after the class definition because of its
# recursive structure, which is unfortunate.
SceneObject._fields_ = [("kind", c_int),
                        ("obj_file", c_char_p),
                        ("center", Vector3f),
                        ("radius", c_float),
                        ("normal", Vector3f),
                        ("offset", c_float),
                        ("material_index", c_int),
                        ("children", POINTER(POINTER(SceneObject))),
                        ("num_children", c_int),
                        ("transform", Matrix4f)]

class Transform(SceneObject):
    def __init__(self):
        super(Transform, self).__init__()
        self.kind = TRANSFORM

    def apply_translation(self, translate):
        pass

    def apply_scale(self, scale):
        pass

    def apply_z_rotation(self, z_rotate):
        pass

    def apply_y_rotation(self, y_rotate):
        pass

    def apply_x_rotate(self, x_rotate):
        pass

class TriangleMesh(SceneObject):
    def __init__(self):
        super(TriangleMesh, self).__init__()
        self.kind = TRIANGLE_MESH

    def set_obj_file(self, obj_file):
        self.obj_file = obj_file.encode("utf-8")

class Sphere(SceneObject):
    def __init__(self):
        super(Sphere, self).__init__()
        self.kind = SPHERE

    def set_center(self, center):
        self.center = center

    def set_radius(self, radius):
        self.radius = radius

class Plane(SceneObject):
    def __init__(self):
        super(Plane, self).__init__()
        self.kind = PLANE

    def set_normal(self, normal):
        self.normal = normal

    def set_offset(self, offset):
        self.offset = offset

class Group(SceneObject):
    def __init__(self):
        super(Group, self).__init__()
        self.kind = GROUP

    def set_num_objects(self, num):
        self.num_objects = num

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

class Materials(Structure):
    _fields_ = [("num_materials", c_int),
                ("materials", POINTER(POINTER(Material)))]
    def __init__(self):
        self.p_materials = []

    def set_num_materials(self, num_materials):
        self.num_materials = num_materials

    def add_material(self, material):
        assert(isinstance(material, Material))
        self.p_materials.append(material)

    def set_materials_pointers(self):
        self.num_materials = len(self.p_materials)
        res = (POINTER(Material) * self.num_materials)()
        for i, child in enumerate(self.p_materials):
            res[i] = cast(pointer(child), POINTER(Material))
        self.materials = cast(res, POINTER(POINTER(Material)))

class PhongMaterial(Material):
    def __init__(self):
        self.kind = PHONG_MATERIAL

class Scene(Structure):
    _fields_ = [("camera", Camera),
                ("group", Group),
                ("lights", Lights),
                ("materials", Materials),
                ("background", Background)]

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

