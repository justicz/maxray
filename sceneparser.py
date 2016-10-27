from scenetypes import *
from vector import *
import re
 
class SceneParser:
    def __init__(self, filename):
        self.filename = filename
        self.obj_stack = []
        self.group_stack = []
        self.lights_stack = []
        self.cur_material_index = None
        # Even though the parser supports multiple groups, multiple
        # "lights"es, and multiple "materials"es, the raytracer currently
        # only supports one of each of these.
        self.group = None
        self.lights = None
        self.materials = None
        self.camera = None
        self.background = None

    def parse_int(self):
        res = int(self.splits[self.index])
        self.index += 1
        return res

    def parse_float(self):
        res = float(self.splits[self.index])
        self.index += 1
        return res

    def parse_str(self):
        res = str(self.splits[self.index])
        self.index += 1
        return res

    def parse_vec3f(self):
        res = Vector3f(float(self.splits[self.index]),
                       float(self.splits[self.index + 1]),
                       float(self.splits[self.index + 2]))
        self.index += 3
        return res

    def parse_token(self):
        # Pull out the next token
        t = self.splits[self.index] 
        
        if t in OBJECT_PARSE:
            self.index += 1
            # The next character should always ben an opening curly brace
            assert(self.splits[self.index] == "{")

            # Skip the curly brace
            self.index += 1

            # Instantiate the object
            o = OBJECT_PARSE[t]()

            # Set the material if it's a scene object
            if isinstance(o, SceneObject):
                o.set_material_index(self.cur_material_index)

            # Add to the lights group if there is one
            if len(self.lights_stack) > 0:
                self.lights_stack[-1].add_light(o)

            # Add to group if there is one
            if len(self.group_stack) > 0:
                self.group_stack[-1].add_object(o)

            # Push onto the lights stack if we need to
            if isinstance(o, Lights):
                self.lights_stack.append(o)
                self.lights = o

            # Push onto the group stack if we need to
            if isinstance(o, Group):
                self.group_stack.append(o)
                self.group = o

            # We only support one root node each of the following objects
            if isinstance(o, Materials):
                assert(self.materials == None)
                self.materials = o

            if isinstance(o, Camera):
                assert(self.camera == None)
                self.camera = o

            if isinstance(o, Background):
                assert(self.background == None)
                self.background = o

            # Push this guy onto the object stack
            self.obj_stack.append(o)

        elif t in ATTRIBUTE_PARSE:
            # Grab the function we need to fetch the attribute
            fetch_attribute = ATTRIBUTE_PARSE[t]
            self.index += 1

            # Fetch the attribute (increments self.index)
            attribute = fetch_attribute(self)
            set_attribute_name = ATTRIBUTE_SET[t]

            # Grab the current object on the stack
            context = self.obj_stack[-1]
            setter = getattr(context, set_attribute_name)

            # Set the attribute
            setter(attribute)

        elif t == MATERIAL_INDEX:
            self.index += 1
            self.cur_material_index = self.parse_int()

        elif t == "}":
            # Pop the current object off of the object stack
            o = self.obj_stack.pop()
            # if it was a lights, pop it off of the lights stack
            if isinstance(o, Lights):
                self.lights_stack.pop()
            # if it was a group, pop it off of the group stack
            if isinstance(o, Group):
                self.group_stack.pop()
            self.index += 1

        else:
            print self.splits
            raise SyntaxError("Unexpected token: '{}' at index {}".format(t, self.index))


    # Parse the scene file and return a Scene object
    def parse(self):
        fins = open(self.filename).read()

        # Collapse everything into one line
        smush = fins.replace("\r", " ").replace("\n", " ")

        # Parse out each component; types, floats, ints
        splits = re.findall(r"[\w/\.\-]+|\{|\}", fins)

        # Begin tokenizing
        self.index = 0
        self.splits = splits

        while self.index < len(self.splits):
            self.parse_token()

        # Create a scene
        s = Scene()
        s.set_camera(self.camera)
        s.set_lights(self.lights)
        s.set_materials(self.materials)
        s.set_background(self.background)
        s.set_group(self.group)

        return s

# Maps object strings to object parsers
OBJECT_PARSE = {
    "PerspectiveCamera": PerspectiveCamera,
    "PointLight": PointLight,
    "DirectionalLight": DirectionalLight,
    "TriangleMesh": TriangleMesh,
    "Background": Background,
    "PhongMaterial": PhongMaterial,
    "Material": Material,
    "Sphere": Sphere,
    "Plane": Plane,
    "Group": Group,
    "Lights": Lights,
    "Materials": Materials,
    "Transform": Transform
}

# Maps attribute strings to attribute parsers
ATTRIBUTE_PARSE = {
    "numObjects": SceneParser.parse_int,
    "numMaterials": SceneParser.parse_int,
    "Translate": SceneParser.parse_vec3f,
    "Scale": SceneParser.parse_vec3f,
    "XRotate": SceneParser.parse_float,
    "YRotate": SceneParser.parse_float,
    "ZRotate": SceneParser.parse_float,
    "numLights": SceneParser.parse_int,
    "position": SceneParser.parse_vec3f,
    "direction": SceneParser.parse_vec3f,
    "color": SceneParser.parse_vec3f,
    "up": SceneParser.parse_vec3f,
    "angle": SceneParser.parse_float,
    "center": SceneParser.parse_vec3f,
    "obj_file": SceneParser.parse_str,
    "diffuseColor": SceneParser.parse_vec3f,
    "specularColor": SceneParser.parse_vec3f,
    "shininess": SceneParser.parse_float,
    "falloff": SceneParser.parse_float,
    "ambientLight": SceneParser.parse_vec3f,
    "radius": SceneParser.parse_float,
    "normal": SceneParser.parse_vec3f,
    "offset": SceneParser.parse_float,
    "cubeMap": SceneParser.parse_str
}

# Maps attribute strings to attribute setters names
ATTRIBUTE_SET = {
    "numObjects": "set_num_objects",
    "numMaterials": "set_num_materials",
    "Translate": "set_translate",
    "Scale": "set_scale",
    "XRotate": "set_x_rotate",
    "YRotate": "set_y_rotate",
    "ZRotate": "set_z_rotate",
    "numLights": "set_num_lights",
    "position": "set_position",
    "direction": "set_direction",
    "color": "set_color",
    "up": "set_up",
    "angle": "set_angle",
    "center": "set_center",
    "obj_file": "set_obj_file",
    "diffuseColor": "set_diffuse_color",
    "specularColor": "set_specular_color",
    "shininess": "set_shininess",
    "falloff": "set_falloff",
    "ambientLight": "set_ambient_light",
    "radius": "set_radius",
    "normal": "set_normal",
    "offset": "set_offset",
    "cubeMap": "set_cube_map"
}

# MaterialIndex is special because it sets the material of
# everything beneath it (until the next material index)
MATERIAL_INDEX = "MaterialIndex"
