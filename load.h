#pragma once
#include <stdint.h>
#include "vec3f.h"

#define MAX_OBJ 1024
#define EPSILON 0.05f

struct Camera {
    uint32_t kind;
    Vector3f center;
    Vector3f direction;
    Vector3f up;
    float angle;
    /* below here are not computed in python */
    Vector3f horizontal;
    float dist;
};

struct Ray {
    Vector3f dir;
    Vector3f o;
};

struct Hit {
    struct SceneObject *scene_object;
    Vector3f hit_coords;
    Vector3f norm;
    float dist;
};

struct SceneObject {
    uint32_t kind;
    char *obj_file;
    Vector3f center;
    float radius;
    Vector3f normal;
    float offset;
    uint32_t material_index;
};

struct Light {
    uint32_t kind;
    Vector3f position;
    Vector3f color;
    float falloff;
    Vector3f direction;
};

struct Material {
    uint32_t kind;
    Vector3f diffuse_color;
    Vector3f specular_color;
    float shininess;
};

struct Intensity {
    Vector3f dir;
    Vector3f intensity;
    float dist;
};

struct Background {
    Vector3f color;
    Vector3f ambient_light;
    char *cube_map;
};

enum LIGHT {
    POINT_LIGHT,
    DIRECTIONAL_LIGHT
};

enum SCENEOBJECT {
    SPHERE,
    PLANE,
    TRIANGLE_MESH
};

enum CAMERA {
    PERSPECTIVE_CAM
};

enum MAT {
    MATERIAL,
    PHONG_MAT
};

extern struct Light *lights[MAX_OBJ];
extern size_t num_lights;

extern struct SceneObject *scene_objects[MAX_OBJ];
extern size_t num_scene_objects;

extern struct Material *materials[MAX_OBJ];
extern size_t num_materials;

extern struct Background *background;
extern struct Camera *camera;

extern uint32_t size[2]; 

void add_scene_object(struct SceneObject *scene_object);
void camera_init(struct Camera *camera);
void add_camera(struct Camera *camera);
void add_light(struct Light *light);
void add_material(struct Material *material);
void add_background(struct Background *background);
void set_size(uint32_t w, uint32_t h);

