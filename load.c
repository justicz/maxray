#include <stdio.h>
#include <stdint.h>
#include <assert.h>
#include <math.h>
#include "load.h"
#include "vec3f.h"

#define M_PI 3.14159265358979

size_t num_scene_objects = 0;
size_t num_lights = 0;
size_t num_materials = 0;

struct Light *lights[MAX_OBJ];
struct SceneObject *scene_objects[MAX_OBJ];
struct Material *materials[MAX_OBJ];
struct Background *background;
struct Camera *camera;
uint32_t size[2];

inline float to_rad(float degrees)
{
    return degrees * M_PI/180.0f;
}

void add_scene_object(struct SceneObject *scene_object)
{
    assert(num_scene_objects < MAX_OBJ - 1);
    scene_objects[num_scene_objects] = scene_object;
    num_scene_objects++;
}

void camera_init(struct Camera *cam)
{
    if (cam->kind == PERSPECTIVE_CAM)
    {
        cam->up = vec3fnorm(cam->up);
        cam->direction = vec3fnorm(cam->direction);
        cam->horizontal = vec3fnorm(vec3fcross(cam->direction, cam->up));
        cam->dist = 1.0f / tan(to_rad(cam->angle)/2.0f);
    }
}

void add_camera(struct Camera *cam)
{
    camera_init(cam);
    camera = cam;
}

void add_light(struct Light *light)
{
    assert(num_lights < MAX_OBJ - 1);
    lights[num_lights] = light;
    num_lights++;
}

void add_material(struct Material *material)
{
    assert(num_materials < MAX_OBJ - 1);
    materials[num_materials] = material;
    num_materials++;
}

void add_background(struct Background *bg)
{
    background = bg;
}

void set_size(uint32_t w, uint32_t h)
{
    size[0] = w;
    size[1] = h;
}
