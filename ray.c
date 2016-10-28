#include <stdio.h>
#include <stdint.h>
#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include "math.h"
#include "load.h"
#include "ray.h"

void camera_ray(struct Camera *camera, float x, float y, struct Ray *camray)
{
    assert(camera->kind == PERSPECTIVE_CAM);
    struct Ray ray;
    Vector3f a = vec3fprodf(camera->direction, camera->dist);
    Vector3f b = vec3fprodf(camera->horizontal, x);
    Vector3f c = vec3fprodf(camera->up, y);
    ray.o = camera->center;
    ray.dir = vec3fnorm(vec3fsum3(a, b, c));
    *camray = ray;
}

void intersect_with_ray(struct SceneObject *scene_object, struct Ray ray, struct Hit *hit)
{
    // Default values in case we haven't implemented this scene_object yet
    hit->hit_coords = ZERO_VEC3F;
    hit->norm = ZERO_VEC3F;
    hit->dist = INFINITY;
    hit->scene_object = NULL;

    if (scene_object->kind == SPHERE) {
        float a = vec3fdot(ray.dir, ray.dir);
        float b = 2.0f * ray.dir.x * (ray.o.x - scene_object->center.x) +
                  2.0f * ray.dir.y * (ray.o.y - scene_object->center.y) +
                  2.0f * ray.dir.z * (ray.o.z - scene_object->center.z);
        float c = vec3fdot(scene_object->center, scene_object->center) +
                  vec3fdot(ray.o, ray.o) +
                  -2.0f * (scene_object->center.x * ray.o.x +
                           scene_object->center.y * ray.o.y +
                           scene_object->center.z * ray.o.z) -
                  scene_object->radius * scene_object->radius;
        float disc = b*b - 4.0f * a * c;
        // If the discriminant is less than zero, there was no hit
        if (disc < 0) {
            return;
        }
        float t = (-b - sqrt(disc))/(2.0f * a);
        hit->scene_object = scene_object;
        hit->hit_coords = vec3fsum2(ray.o, vec3fprodf(ray.dir, t));
        hit->norm = vec3fnorm(vec3fsub(hit->hit_coords, scene_object->center));
        hit->dist = t;
        return;
    }
    else if (scene_object->kind == PLANE)
    {
        float t = vec3fdot(scene_object->normal, ray.dir);
        t = (scene_object->offset - vec3fdot(ray.o, scene_object->normal)) / t;
        // Can't be behind the origin or too far
        if (t < 0.0f) {
            return;
        }
        hit->hit_coords = vec3fsum2(ray.o, vec3fprodf(ray.dir, t));
        hit->norm = scene_object->normal;
        hit->dist = t;
        return;
    }
}

void light_intensity_at_hit(struct Light *light, struct Hit *hit, struct Intensity *intensity)
{
    if (!isfinite(hit->dist))
    {
        intensity->intensity = scene.background.color;
        intensity->dir = ZERO_VEC3F;
        intensity->dist = INFINITY;
    }
    if (light->kind == POINT_LIGHT)
    {
        Vector3f diff = vec3fsub(light->position, hit->hit_coords);
        intensity->dir = vec3fnorm(diff);
        intensity->dist = vec3fabs(diff);
        float factor = 1.0f/(intensity->dist*intensity->dist*light->falloff);
        intensity->intensity = vec3fprodf(light->color, factor);
        return;
    }
    else if (light->kind == DIRECTIONAL_LIGHT)
    {
    }
}

void find_closest_intersection(struct SceneObject *root, struct Ray ray, struct Hit *hit)
{
    hit->dist = INFINITY;
    hit->norm = ZERO_VEC3F;
    hit->hit_coords = ZERO_VEC3F;

    // If we don't have any children, just check for an intersection
    if (root->num_children == 0)
    {
        intersect_with_ray(root, ray, hit);
        return;
    }

    // If we do have children, find the best of all of our children
    for (int32_t i = 0; i < root->num_children; i++)
    {
        struct Hit check;
        struct SceneObject *scene_object = root->children[i];
        find_closest_intersection(scene_object, ray, &check);
        if (check.dist < EPSILON)
        {
            continue;
        }
        if (check.dist < hit->dist)
        {
            *hit = check;
        }
   }
}

void normalize_framebuffer(Vector3f **framebuffer, int32_t w, int32_t h)
{
    float max = 0;
    for (int32_t j = 0; j < h; j++)
    {
        for (int32_t i = 0; i < w; i++)
        {
            float abs = vec3fabs(framebuffer[i][j]);
            if (abs > max)
            {
                max = abs;
            }
        }
    }

    // If the image is all black somehow we have bigger problems...
    if (max == 0)
    {
        return;
    }

    max = 255.0f / max;
    for (int32_t j = 0; j < h; j++)
    {
        for (int32_t i = 0; i < w; i++)
        {
            framebuffer[i][j] = vec3fprodf(framebuffer[i][j], max);
        }
    }
}

bool free_path(struct Ray shadow_ray)
{
    struct Hit hit;
    find_closest_intersection(&scene.group, shadow_ray, &hit);
    return !isfinite(hit.dist);
}

Vector3f solve_ray(struct Ray ray)
{
    Vector3f pixel = {0.0f, 0.0f, 0.0f};
    struct Hit hit;

    // Grab the root scene object
    assert(scene.group.num_children > 0);
    find_closest_intersection(&scene.group, ray, &hit);

    if (isfinite(hit.dist)) {
        for (int32_t l = 0; l < scene.lights.num_lights; l++)
        {
            struct Ray shadow_ray;
            shadow_ray.o = hit.hit_coords;

            shadow_ray.dir = vec3fnorm(vec3fsub((scene.lights.lights[0][l]).position, hit.hit_coords));
           
            if (!free_path(shadow_ray))
            {
                continue;
            }

            struct Intensity intensity;
            light_intensity_at_hit(&((*scene.lights.lights)[l]), &hit, &intensity);
            pixel = vec3fsum2(pixel, intensity.intensity);
        }
    }

    pixel = vec3fsum2(pixel, scene.background.ambient_light);

    return pixel;
}

Vector3f **raytrace()
{
    printf("C: In raytrace\n");

    int32_t horz_steps = size[0];
    float horz_increment = 2.0f / horz_steps;
    float horz_pos = -1.0f;

    int32_t vert_steps = size[1];
    float vert_decrement = 2.0f / vert_steps;
    float vert_pos = 1.0f;

    Vector3f **framebuffer = (Vector3f **)malloc(sizeof(Vector3f *) * size[0]);
    for (int32_t i = 0; i < size[0]; i++)
    {
        int32_t col_bytes = sizeof(Vector3f) * size[1];
        framebuffer[i] = (Vector3f *)malloc(col_bytes);
        memset(framebuffer[i], 0, col_bytes);
    }

    for (int32_t j = 0; j < vert_steps; j++)
    {
        for (int32_t i = 0; i < horz_steps; i++)
        {
            struct Ray camray;
            camera_ray(&scene.camera, horz_pos, vert_pos, &camray);
            framebuffer[i][j] = solve_ray(camray);
            horz_pos += horz_increment;
        }
        horz_pos = -1.0f;
        vert_pos -= vert_decrement;
    }

    normalize_framebuffer(framebuffer, horz_steps, vert_steps);

    printf("C: Finished raytrace\n");

    return framebuffer;

}

