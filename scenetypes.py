from ctypes import *
from vector import *
from matrix import *
import objparser
import skybox

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
TRIANGLE          = 5

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
                ("cube_map", c_char_p),
                ("skybox", POINTER(POINTER(POINTER(Vector3f))))]
    def __init__(self):
        # things we don't want to be garbage collected
        self.save = []
        self.cube_map =  ""

    def set_color(self, color):
        self.color = color

    def set_ambient_light(self, ambient_light):
        self.ambient_light = ambient_light

    def set_prefix(self, prefix):
        self.prefix = prefix

    def set_size(self, size):
        self.size = size

    def set_cube_map(self, cube_map):
        print "Python: Loading skybox..."
        self.cube_map = cube_map
        sbox = skybox.load(self.prefix, cube_map, self.size)
        faces = (POINTER(POINTER(Vector3f)) * 6)()
        for f in range(6):
            im = sbox[f]
            cols = (POINTER(Vector3f) * self.size[0])()
            for i in range(self.size[0]):
                col = (Vector3f * self.size[1])()
                cols[i] = cast(pointer(col), POINTER(Vector3f))
                for j in range(self.size[1]):
                    x, y, z = im.getpixel((i, j))
                    cols[i][j] = Vector3f(x/255.0, y/255.0, z/255.0)
                self.save.append(col)
            self.save.append(cols)
            faces[f] = cast(pointer(cols), POINTER(POINTER(Vector3f)))
        self.skybox = cast(pointer(faces), POINTER(POINTER(POINTER(Vector3f))))
        print "...done"

class SceneObject(Structure):
    def __init__(self):
        self.p_children = []
        self.transform = Matrix4f([1, 0, 0, 0],
                                  [0, 1, 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, 1])
        self.transform_inverse = Matrix4f([1, 0, 0, 0],
                                          [0, 1, 0, 0],
                                          [0, 0, 1, 0],
                                          [0, 0, 0, 1])

    def set_material_index(self, material_index):
        self.material_index = material_index

    def add_child_object(self, obj):
        assert(isinstance(obj, SceneObject))
        # Children inherit their parent's transform
        obj.transform = self.transform
        obj.transform_inverse = self.transform_inverse
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
                        ("face", c_int*3),
                        ("parent_mesh", POINTER(SceneObject)),
                        ("mesh_normals", POINTER(Vector3f)),
                        ("mesh_vertices", POINTER(Vector3f)),
                        ("vertex_degrees", POINTER(c_int)),
                        ("num_mesh_vertices", c_int),
                        ("transform", Matrix4f),
                        ("transform_inverse", Matrix4f)]

class Transform(SceneObject):
    def __init__(self):
        super(Transform, self).__init__()
        self.kind = TRANSFORM

    def apply_translation(self, translation):
        # object -> world
        self.transform.apply_r(Matrix4fHelper.translation(translation))
        # world -> object
        rt = Vector3f(-translation.x, -translation.y, -translation.z)
        self.transform_inverse.apply_l(Matrix4fHelper.translation(rt))

    def apply_scale(self, scale):
        # object -> world
        self.transform.apply_r(Matrix4fHelper.scale(scale))
        # world -> object
        rs = Vector3f(1.0/scale.x, 1.0/scale.y, 1.0/scale.z)
        self.transform_inverse.apply_l(Matrix4fHelper.scale(rs))

    def apply_x_rotation(self, x_rotation):
        # object -> world
        rot = Matrix4fHelper.x_rotation(x_rotation)
        self.transform.apply_r(rot)
        # world -> object
        self.transform_inverse.apply_l(Matrix4fHelper.transpose(rot))

    def apply_y_rotation(self, y_rotation):
        # object -> world
        rot = Matrix4fHelper.y_rotation(y_rotation)
        self.transform.apply_r(rot)
        # world -> object
        self.transform_inverse.apply_l(Matrix4fHelper.transpose(rot))

    def apply_z_rotation(self, z_rotation):
        # object -> world
        rot = Matrix4fHelper.z_rotation(z_rotation)
        self.transform.apply_r(rot)
        # world -> object
        self.transform_inverse.apply_l(Matrix4fHelper.transpose(rot))

class TriangleMesh(SceneObject):
    def __init__(self):
        super(TriangleMesh, self).__init__()
        self.kind = TRIANGLE_MESH

    def set_obj_file(self, obj_file):
        self.obj_file = obj_file.encode("utf-8")
        self.obj = objparser.ObjectFile(self.prefix + "/" + obj_file)
        for face in self.obj.face_indices:
            self.add_child_object(Triangle(face, self.material_index, self))

        self.num_mesh_vertices = len(self.obj.vertices)
        self.mv = (Vector3f * self.num_mesh_vertices)()
        self.mesh_vertices = cast(pointer(self.mv), POINTER(Vector3f))

        # Initialize the vertices
        for i in range(self.num_mesh_vertices):
            self.mesh_vertices[i] = self.obj.vertices[i]

        self.mn = (Vector3f * self.num_mesh_vertices)()
        self.mesh_normals = cast(pointer(self.mn), POINTER(Vector3f))

        # Zero out the mesh normals (to be computed in c)
        for i in range(self.num_mesh_vertices):
            self.mesh_normals[i] = Vector3f(0, 0, 0)

        self.dg = (c_int * self.num_mesh_vertices)()
        self.vertex_degrees = cast(pointer(self.dg), POINTER(c_int))
        for i in range(self.num_mesh_vertices):
            self.vertex_degrees[i] = 0

    def set_prefix(self, prefix):
        self.prefix = prefix

class Triangle(SceneObject):
    def __init__(self, face, material_index, parent):
        super(Triangle, self).__init__()
        self.kind = TRIANGLE
        self.material_index = material_index
        # We have to keep a pointer back to our parent so that we can grab
        # the value o feach vertex
        self.parent_mesh = cast(pointer(parent), POINTER(SceneObject))

        # Make sure face doesn't get garbage collected
        for i in range(3):
            self.face[i] = face[i]

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
                ("background", Background),
                ("shadows", c_bool),
                ("bounces", c_int)]

    def set_shadows(self, shadows):
        self.shadows = shadows

    def set_bounces(self, bounces):
        self.bounces = bounces

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

