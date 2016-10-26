class Camera:
    def __init__(self):
        pass

class PerspectiveCamera(Camera):
    def __init__(self):
        pass

    def set_center(self, center):
        self.center = center

    def set_direction(self, direction):
        self.direction = direction

    def set_up(self, up):
        self.up = up

    def set_angle(self, angle):
        self.angle = angle

class Light:
    def __init__(self):
        pass

class TriangleMesh:
    def __init__(self):
        pass

    def set_obj_file(self, obj_file):
        self.obj_file = obj_file

class Lights:
    def __init__(self):
        self.lights = []
        self.index = 0

    def set_num_lights(self, num_lights):
        self.num_lights = num_lights

    def add_light(self, lights):
        self.lights.append(material)
        self.index += 1

    def get_light_by_index(self, index):
        return lights[index]


class PointLight(Light):
    def __init__(self):
        pass

    def set_position(self, position):
        self.position = position

    def set_color(self, color):
        self.color = color

    def set_falloff(self, falloff):
        self.falloff = falloff

class DirectionalLight(Light):
    def __init__(self):
        pass

    def set_direction(self, direction):
        self.direction = direction

    def set_color(self, color):
        self.color = color

class Background:
    def __init__(self):
        pass

    def set_color(self, color):
        self.color = color

    def set_ambient_light(self, ambient_light):
        self.ambient_light = ambient_light

    def set_cube_map(self, cube_map):
        self.cube_map = cube_map

class Transform:
    def __init__(self):
        pass

    def set_translate(self, translate):
        self.translate = translate

    def set_scale(self, scale):
        self.scale = scale

    def set_mesh(self, mesh):
        self.mesh = mesh

    def set_material_index(self, material_index):
        self.material_index = material_index

    def set_z_rotate(self, z_rotate):
        self.z_rotate = z_rotate

    def set_y_rotate(self, y_rotate):
        self.y_rotate = y_rotate

    def set_x_rotate(self, x_rotate):
        self.x_rotate = x_rotate

class SceneObject:
    def __init__(self):
        pass

    def set_material_index(self, material_index):
        self.material_index = material_index

class Sphere(SceneObject):
    def __init__(self):
        pass

    def set_center(self, center):
        self.center = center

    def set_radius(self, radius):
        self.radius = radius

class Plane(SceneObject):
    def __init__(self):
        pass

    def set_normal(self, normal):
        self.normal = normal

    def set_offset(self, offset):
        self.offset = offset

class Materials:
    def __init__(self):
        self.materials = []
        self.index = 0

    def set_num_materials(self, num_materials):
        self.num_materials = num_materials

    def add_material(self, material):
        self.materials.append(material)
        self.index += 1

    def get_material_by_index(self, index):
        return materials[index]

class Group:
    def __init__(self):
        self.objects = []
        self.index = 0

    def set_num_objects(self, num):
        self.num_objects = num

    def add_object(self, obj):
        self.objects.append(obj)
        self.index += 1

    def get_object_by_index(self, index):
        return self.objects[index]

class Material:
    def __init__(self):
        pass

    def set_diffuse_color(self, color):
        self.diffuse_color = color

    def set_specular_color(self, color):
        self.specular_color = color

    def set_shininess(self, shininess):
        self.shininess = shininess

class PhongMaterial(Material):
    def __init__(self):
        pass

class Scene:
    def __init__(self):
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)
