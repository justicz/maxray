#pragma once
#include <stdint.h>
#include <stdbool.h>
#include "matrix4f.h"
#include "vec3f.h"

#define EPSILON 0.01f

struct Camera {
    int kind;
    Vector3f center;
    Vector3f direction;
    Vector3f up;
    float angle;
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
    int kind;
    char *obj_file;
    Vector3f center;
    float radius;
    Vector3f normal;
    float offset;
    int material_index;
    struct SceneObject **children;
    int num_children;
    int face[3];
    struct SceneObject *parent_mesh;
    Vector3f *mesh_normals;
    Vector3f *mesh_vertices;
    int *vertex_degrees;
    int num_mesh_vertices;
    Matrix4f transform;
    Matrix4f transform_inverse;
};

struct Lights {
    int num_lights;
    struct Light **lights;
};

struct Light {
    int kind;
    Vector3f position;
    Vector3f color;
    float falloff;
    Vector3f direction;
};

struct Materials {
    int num_materials;
    struct Material **materials;
};

struct Material {
    int kind;
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
    Vector3f ***skybox;
};

struct Scene {
    struct Camera camera;
    struct SceneObject group;
    struct Lights lights;
    struct Materials materials;
    struct Background background;
    bool shadows;
    int bounces;
};

enum LIGHT {
    POINT_LIGHT,
    DIRECTIONAL_LIGHT
};

enum SCENEOBJECT {
    SPHERE,
    PLANE,
    TRIANGLE_MESH,
    GROUP,
    TRANSFORM,
    TRIANGLE
};

enum CAMERA {
    PERSPECTIVE_CAM
};

enum MAT {
    MATERIAL,
    PHONG_MAT
};

enum SKYBOX {
    UP,
    DOWN,
    LEFT,
    RIGHT,
    FRONT,
    BACK
};

static const Vector3f UP_NORM    = {  0.0f, -1.0f,  0.0f };
static const Vector3f DOWN_NORM  = {  0.0f,  1.0f,  0.0f };
static const Vector3f RIGHT_NORM = { -1.0f,  0.0f,  0.0f };
static const Vector3f LEFT_NORM  = {  1.0f,  0.0f,  0.0f };
static const Vector3f FRONT_NORM = {  0.0f,  0.0f, -1.0f };
static const Vector3f BACK_NORM  = {  0.0f,  0.0f,  1.0f };
extern Vector3f NORMS[6];
extern int FACES[6];

extern struct Scene scene;
extern int size[2]; 

void init_scene(struct Scene *sc);
void set_size(int w, int h);

