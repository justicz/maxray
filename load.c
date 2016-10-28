#include <stdio.h>
#include <stdint.h>
#include <assert.h>
#include <math.h>
#include "load.h"
#include "vec3f.h"

#define M_PI 3.14159265358979

struct Scene scene;
int32_t size[2];

inline float to_rad(float degrees)
{
    return degrees * M_PI/180.0f;
}

void camera_init(struct Camera *cam)
{
    if (cam->kind == PERSPECTIVE_CAM)
    {
        //printf("Got perspective camera\n");
        cam->up = vec3fnorm(cam->up);
        cam->direction = vec3fnorm(cam->direction);
        cam->horizontal = vec3fnorm(vec3fcross(cam->direction, cam->up));
        cam->dist = 1.0f / tan(to_rad(cam->angle)/2.0f);
        //printf("\t up: \t"); print_vec3f(cam->up);
        //printf("\t dir: \t"); print_vec3f(cam->direction);
        //printf("\t hor: \t"); print_vec3f(cam->horizontal);
        //printf("\t dst: \t%f\n", cam->dist);
    }
}

void init_scene(struct Scene *sc)
{
    scene = *sc;
    camera_init(&scene.camera);
}

void set_size(int32_t w, int32_t h)
{
    printf("Got size %dpx x %dpx\n", w, h);
    size[0] = w;
    size[1] = h;
}
