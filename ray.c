#include <stdio.h>
#include <stdint.h>
#include <assert.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include "math.h"
#include "load.h"
#include "ray.h"

Vector3f NORMS[6];
int FACES[6];
float PIXEL_SIDE;

float minf(float a, float b) {
    return a < b ? a : b;
}

float maxf(float a, float b) {
    return a > b ? a : b;
}

int mini(int a, int b) {
    return a < b ? a : b;
}

int maxi(int a, int b) {
    return a > b ? a : b;
}

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

void transform_pos_by_matrix4f(Vector3f *pt, Matrix4f t)
{
    Vector3f out;
    out.x = pt->x*t.m11 + pt->y*t.m12 + pt->z*t.m13 + t.m14;
    out.y = pt->x*t.m21 + pt->y*t.m22 + pt->z*t.m23 + t.m24;
    out.z = pt->x*t.m31 + pt->y*t.m32 + pt->z*t.m33 + t.m34;
    *pt = out;
}

void transform_vec_by_matrix4f(Vector3f *vec, Matrix4f t)
{
    Vector3f out;
    out.x = vec->x*t.m11 + vec->y*t.m12 + vec->z*t.m13;
    out.y = vec->x*t.m21 + vec->y*t.m22 + vec->z*t.m23;
    out.z = vec->x*t.m31 + vec->y*t.m32 + vec->z*t.m33;
    *vec = out;
}

void transform_ray_by_matrix4f(struct Ray *ray, Matrix4f t)
{
    transform_pos_by_matrix4f(&ray->o, t);
    transform_vec_by_matrix4f(&ray->dir, t);
    ray->dir = vec3fnorm(ray->dir);
}

void transform_hit_by_matrix4f(struct Hit *hit, struct Ray ray, Matrix4f t, Matrix4f ti)
{
    transform_pos_by_matrix4f(&hit->hit_coords, t);
    hit->dist = vec3fabs(vec3fsub(hit->hit_coords, ray.o));
    Matrix4f transposed = matrix4ftransposed(ti);
    transform_vec_by_matrix4f(&hit->norm, transposed);
    hit->norm = vec3fnorm(hit->norm);
}

bool has_skybox()
{
    return scene.background.skybox != NULL;
}

Vector3f sample_skybox_at_pos(float x, float y, int face)
{
    x += 0.5f;
    y += 0.5f;

    int x_low = mini(floor(x/PIXEL_SIDE), size[0] - 1);
    int x_high = x_low + 1;
    int y_low = mini(floor(y/PIXEL_SIDE), size[1] - 1);
    int y_high = y_low + 1;

    Vector3f **boxface = scene.background.skybox[face];

    float a = fmod(x, PIXEL_SIDE)/PIXEL_SIDE;
    float b = fmod(y, PIXEL_SIDE)/PIXEL_SIDE;
    Vector3f bl, br, tl, tr;

    // Bottom left
    bl = boxface[x_low][y_low];

    // Bottom right
    if (x_high < size[0])
    {
        br = boxface[x_high][y_low];
    }
    else
    {
        br = bl;
    }

    // Lerp it up
    Vector3f bhoriz = vec3fsum2(vec3fprodf(bl, (1 - a)), vec3fprodf(br, a));

    // Top left
    if (y_high < size[1])
        tl = boxface[x_low][y_high];
    else
        tl = bl;

    // Top right
    if (x_high < size[0] && y_high < size[1])
        tr = boxface[x_high][y_high];
    else
        tr = br;

    // Lerp it up
    Vector3f thoriz = vec3fsum2(vec3fprodf(tl, (1 - a)), vec3fprodf(tr, a));

    // One last lerp
    return vec3fsum2(vec3fprodf(bhoriz, (1 - b)), vec3fprodf(thoriz, b));
}

Vector3f solve_skybox_hit(struct Ray ray)
{
    int best_face;
    float lowest_dot = INFINITY;
    float t;
    for (int i = 0; i < 6; i++)
    {
        t = vec3fdot(NORMS[i], ray.dir);
        if (t < lowest_dot) {
            lowest_dot = t;
            best_face = FACES[i];
        }
    }
    t = 0.5f / lowest_dot;
    Vector3f hit_coords = vec3fprodf(ray.dir, t);
    float x, y;
    switch(best_face)
    {
        case UP:
            x = -hit_coords.x;
            y = hit_coords.z;
            break;
        case DOWN:
            x = -hit_coords.x;
            y = hit_coords.z;
            break;
        case LEFT:
            x = hit_coords.z;
            y = hit_coords.y;
            break;
        case RIGHT:
            x = -hit_coords.z;
            y = hit_coords.y;
            break;
        case FRONT:
            x = hit_coords.x;
            y = hit_coords.y;
            break;
        case BACK:
            x = hit_coords.x;
            y = hit_coords.y;
            break;
   }
    return sample_skybox_at_pos(x, y, best_face);
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
        if (disc < 0.0f) {
            return;
        }

        float t = (-b - sqrt(disc))/(2.0f * a);

        if (t < 0.0f) {
            return;
        }

        hit->scene_object = scene_object;
        hit->hit_coords = vec3fsum2(ray.o, vec3fprodf(ray.dir, t));
        hit->norm = vec3fnorm(vec3fsub(hit->hit_coords, scene_object->center));
        hit->dist = t;
        return;
    }
    else if (scene_object->kind == PLANE)
    {
        float t = vec3fdot(scene_object->normal, ray.dir);
        // No intersection if the ray is parallel to the plane
        if (t == 0.0f) {
            return;
        }
        t = (scene_object->offset - vec3fdot(ray.o, scene_object->normal)) / t;
        if (t < 0.0f) {
            return;
        }
        hit->scene_object = scene_object;
        hit->hit_coords = vec3fsum2(ray.o, vec3fprodf(ray.dir, t));
        hit->norm = scene_object->normal;
        hit->dist = t;
        return;
    }
    else if (scene_object->kind == TRIANGLE)
    {
        struct SceneObject *parent = scene_object->parent_mesh;
        assert(parent->kind == TRIANGLE_MESH);

        // First we compute the supporting plane
        Vector3f A = parent->mesh_vertices[scene_object->face[0]];
        Vector3f B = parent->mesh_vertices[scene_object->face[1]];
        Vector3f C = parent->mesh_vertices[scene_object->face[2]];

        Vector3f E0 = vec3fsub(B, A);
        Vector3f E1 = vec3fsub(C, A);
        Vector3f n = vec3fnorm(vec3fcross(E0, E1));
        float offset = vec3fdot(n, A);

        float t = vec3fdot(n, ray.dir);
        if (t == 0.0f) {
            return;
        }
        t = (offset - vec3fdot(ray.o, n)) / t;
        if (t < 0.0f) {
            return;
        }
        // Q is the intersection with the supporting plane
        Vector3f Q = vec3fsum2(ray.o, vec3fprodf(ray.dir, t));

        // Check if we're outside any of the edges
        float e0, e1, e2;

        Vector3f CMB = vec3fsub(C, B);
        Vector3f QMB = vec3fsub(Q, B);
        Vector3f CMB_QMB = vec3fcross(CMB, QMB);
        if ((e0 = vec3fdot(CMB_QMB, n)) < 0.0f) {
            return;
        }

        Vector3f AMC = vec3fsub(A, C);
        Vector3f QMC = vec3fsub(Q, C);
        Vector3f AMC_QMC = vec3fcross(AMC, QMC);
        if ((e1 = vec3fdot(AMC_QMC, n)) < 0.0f) {
            return;
        }

        Vector3f BMA = vec3fsub(B, A);
        Vector3f QMA = vec3fsub(Q, A);
        Vector3f BMA_QMA = vec3fcross(BMA, QMA);
        if ((e2 = vec3fdot(BMA_QMA, n)) < 0.0f) {
            return;
        }

        float BMA_CMA_n = vec3fdot(vec3fcross(BMA, vec3fprodf(AMC, -1.0f)), n);

        float alpha = e0 / BMA_CMA_n;
        float beta  = e1 / BMA_CMA_n;
        float gamma = e2 / BMA_CMA_n;

        Vector3f normA = parent->mesh_normals[scene_object->face[0]];
        Vector3f normB = parent->mesh_normals[scene_object->face[1]];
        Vector3f normC = parent->mesh_normals[scene_object->face[2]];

        Vector3f lerp = vec3fnorm(vec3fsum3(vec3fprodf(normA, alpha),
                                            vec3fprodf(normB, beta),
                                            vec3fprodf(normC, gamma)));

        // We're inside the triangle!
        hit->scene_object = scene_object;
        hit->hit_coords = Q;
        hit->norm = lerp;
        hit->dist = t;
    }
}


void sum_normals(struct SceneObject *root)
{
    if (root->kind == TRIANGLE_MESH)
    {
        for (int32_t i = 0; i < root->num_children; i++)
        {
            struct SceneObject *triangle = root->children[i];
            assert(triangle->kind == TRIANGLE);

            // Compute the normal of the supporting plane
            int *t = triangle->face;
            Vector3f A = root->mesh_vertices[t[0]];
            Vector3f B = root->mesh_vertices[t[1]];
            Vector3f C = root->mesh_vertices[t[2]];
            Vector3f E0 = vec3fsub(B, A);
            Vector3f E1 = vec3fsub(C, A);
            Vector3f n = vec3fnorm(vec3fcross(E0, E1));

            for (int32_t t = 0; t < 3; t++)
            {
                Vector3f old = root->mesh_normals[triangle->face[t]];
                root->mesh_normals[triangle->face[t]] = vec3fsum2(old, n);
                root->vertex_degrees[triangle->face[t]]++;
            }
        }
        return;
    }
    for (int32_t i = 0; i < root->num_children; i++)
    {
        struct SceneObject *scene_object = root->children[i];
        sum_normals(scene_object);
    }
}

void average_normals(struct SceneObject *root)
{
    if (root->kind == TRIANGLE_MESH)
    {
        for (int i = 0; i < root->num_mesh_vertices; i++)
        {
            root->mesh_normals[i] = vec3fprodf(root->mesh_normals[i], 1.0f/root->vertex_degrees[i]);
            root->mesh_normals[i] = vec3fnorm(root->mesh_normals[i]);
        }
        return;
    }

    for (int32_t i = 0; i < root->num_children; i++)
    {
        struct SceneObject *scene_object = root->children[i];
        average_normals(scene_object);
    }
}

void precompute_smooth_normals(struct SceneObject *root)
{
    sum_normals(root);
    average_normals(root);
}


void find_intersection(struct SceneObject *root, struct Ray ray, struct Hit *hit, bool closest)
{
    hit->dist = INFINITY;
    hit->norm = ZERO_VEC3F;
    hit->hit_coords = ZERO_VEC3F;

    // If we don't have any children, just check for an intersection
    if (root->num_children == 0)
    {
        // Transform the ray into object coordinates
        transform_ray_by_matrix4f(&ray, root->transform_inverse);

        // Intersect with the object
        intersect_with_ray(root, ray, hit);

        // Transform the ray back into world coordinates
        transform_ray_by_matrix4f(&ray, root->transform);

        // If there was a hit, transform its details back into world coordinates
        // (dealing with normals and distances)
        if (isfinite(hit->dist)) {
            transform_hit_by_matrix4f(hit, ray, root->transform, root->transform_inverse);
        }

        return;
    }

    // If we do have children, find the best of all of our children
    for (int32_t i = 0; i < root->num_children; i++)
    {
        struct Hit check;
        struct SceneObject *scene_object = root->children[i];
        find_intersection(scene_object, ray, &check, closest);
        if (check.dist < EPSILON)
        {
            continue;
        }
        if (check.dist < hit->dist)
        {
            *hit = check;
            if (!closest)
            {
                return;
            }
        }
    }
}

void find_closest_intersection(struct SceneObject *root, struct Ray ray, struct Hit *hit)
{
    find_intersection(root, ray, hit, true);
}

void find_any_intersection(struct SceneObject *root, struct Ray ray, struct Hit *hit)
{
    find_intersection(root, ray, hit, false);
}

bool free_shadow_path(struct Ray shadow_ray)
{
    // Check if shadows are enabled
    if (!scene.shadows)
    {
        return true;
    }
    struct Hit hit;
    find_any_intersection(&scene.group, shadow_ray, &hit);
    return !isfinite(hit.dist);
}

void light_intensity_at_hit(struct Light *light, struct Hit *hit, struct Intensity *intensity)
{
    struct Ray shadow_ray;
    bool in_shadow;

    intensity->intensity = ZERO_VEC3F;
    intensity->dir = ZERO_VEC3F;
    intensity->dist = INFINITY;

    if (!isfinite(hit->dist))
    {
        return;
    }

    if (light->kind == POINT_LIGHT)
    {
        shadow_ray.o = hit->hit_coords;
        shadow_ray.dir = vec3fnorm(vec3fsub(light->position, hit->hit_coords));
        in_shadow = !free_shadow_path(shadow_ray);
        if (!in_shadow)
        {
            Vector3f diff = vec3fsub(light->position, hit->hit_coords);
            intensity->dir = vec3fnorm(diff);
            intensity->dist = vec3fabs(diff);
            float factor = 1.0f/(intensity->dist*intensity->dist*light->falloff);
            intensity->intensity = vec3fprodf(light->color, factor);
        }
    }
    else if (light->kind == DIRECTIONAL_LIGHT)
    {
        Vector3f cam_to_light = vec3fnorm(vec3fprodf(light->direction, -1.0f));

        shadow_ray.o = hit->hit_coords;
        shadow_ray.dir = cam_to_light;
        in_shadow = !free_shadow_path(shadow_ray);

        if (!in_shadow)
        {
            intensity->dir = cam_to_light;
            intensity->dist = INFINITY;
            intensity->intensity = light->color;
        }
    }
}

void normalize_framebuffer(Vector3f **framebuffer, int32_t w, int32_t h)
{
    for (int32_t j = 0; j < h; j++)
    {
        for (int32_t i = 0; i < w; i++)
        {
            framebuffer[i][j]   = vec3fprodf(framebuffer[i][j], 255.0f);
            framebuffer[i][j].x = minf(framebuffer[i][j].x,      255.0f);
            framebuffer[i][j].y = minf(framebuffer[i][j].y,      255.0f);
            framebuffer[i][j].z = minf(framebuffer[i][j].z,      255.0f);
        }
    }
}

struct Material *get_material_from_scene_object(struct SceneObject *scene_object)
{
    int32_t material_index = scene_object->material_index;
    assert(material_index < scene.materials.num_materials);
    return scene.materials.materials[material_index];
}

Vector3f shade(struct Hit *hit, struct Intensity *intensity)
{
    struct Material *material = get_material_from_scene_object(hit->scene_object);

    Vector3f color = {0.0f, 0.0f, 0.0f};

    // Diffuse part
    float dot = vec3fdot(hit->norm, intensity->dir);
    dot = dot > 0.0f ? dot : 0.0f;

    Vector3f diffuse_color = vec3fprodf(material->diffuse_color, dot);
    diffuse_color = vec3fhad(diffuse_color, intensity->intensity);
    color = vec3fsum2(color, diffuse_color);

    // Specular part
    Vector3f eye_vec = vec3fnorm(vec3fsub(hit->hit_coords, scene.camera.center));
    Vector3f ref_eye = vec3fsub(eye_vec, vec3fprodf(hit->norm, 2.0f*vec3fdot(eye_vec, hit->norm)));
    dot = vec3fdot(ref_eye, intensity->dir);
    dot = dot > 0.0f ? dot : 0.0f;
    dot = pow(dot, material->shininess);

    Vector3f spec_color = vec3fprodf(material->specular_color, dot);
    spec_color = vec3fhad(spec_color, intensity->intensity);
    color = vec3fsum2(color, spec_color);

    return color;
}

Vector3f shade_ambient(struct Hit *hit)
{
    struct Material *material = get_material_from_scene_object(hit->scene_object);
    return vec3fhad(material->diffuse_color, scene.background.ambient_light);
}

Vector3f solve_ray(struct Ray ray, int bounces)
{
    Vector3f pixel = {0.0f, 0.0f, 0.0f};
    struct Hit hit;

    // Grab the root scene object
    assert(scene.group.num_children > 0);
    find_closest_intersection(&scene.group, ray, &hit);

    if (isfinite(hit.dist))
    {
        for (int32_t l = 0; l < scene.lights.num_lights; l++)
        {
            struct Intensity intensity;
            // Find the light intensity
            light_intensity_at_hit(scene.lights.lights[l], &hit, &intensity);
            // Shade the pixel with the light
            pixel = vec3fsum2(pixel, shade(&hit, &intensity));
        }
        // Add in the ambient component
        pixel = vec3fsum2(pixel, shade_ambient(&hit));
    }
    else
    {
        if (has_skybox())
        {
            return solve_skybox_hit(ray);
        }
        else
        {
            return scene.background.color;
        }
    }

    // If there are no more bounces left, just return the value
    if (bounces == 0)
    {
        return pixel;
    }

    struct Ray ref;
    ref.dir = vec3fsub(ray.dir, vec3fprodf(hit.norm, 2.0f*vec3fdot(ray.dir, hit.norm)));
    ref.o = hit.hit_coords;
    struct Material *material = get_material_from_scene_object(hit.scene_object);
    // Otherwise, recurse and incorporate the reflection
    Vector3f bounce = vec3fhad(solve_ray(ref, bounces - 1), material->specular_color);
    return vec3fsum2(bounce, pixel);
}

Vector3f **raytrace()
{
    // Define some constants (TODO: there's almost certainly a better way to do this)
    NORMS[0]=UP_NORM;       NORMS[1]=DOWN_NORM;
    NORMS[2]=LEFT_NORM;     NORMS[3]=RIGHT_NORM;
    NORMS[4]=FRONT_NORM;    NORMS[5]=BACK_NORM;
    FACES[0]=UP;            FACES[1]=DOWN;
    FACES[2]=LEFT;          FACES[3]=RIGHT;
    FACES[4]=FRONT;         FACES[5]=BACK;
    PIXEL_SIDE = 1.0f / size[0];

    printf("C: In raytrace\n");

    printf("C: Precomputing smooth normals...\n");
    precompute_smooth_normals(&scene.group);
    printf("C: ...done. Running raytrace... \n");

    Vector3f **framebuffer = (Vector3f **)malloc(sizeof(Vector3f *) * size[0]);
    for (int32_t i = 0; i < size[0]; i++)
    {
        int32_t col_bytes = sizeof(Vector3f) * size[1];
        framebuffer[i] = (Vector3f *)malloc(col_bytes);
        memset(framebuffer[i], 0, col_bytes);
    }

    int32_t horz_steps = size[0];
    float horz_increment = 2.0f / horz_steps;
    int32_t vert_steps = size[1];
    float vert_increment = 2.0f / vert_steps;

    #pragma omp parallel for
    for (int32_t j = 0; j < vert_steps; j++)
    {
        for (int32_t i = 0; i < horz_steps; i++)
        {
            struct Ray camray;
            float horz = -1.0f + i*horz_increment;
            float vert = 1.0f - j*vert_increment;
            camera_ray(&scene.camera, horz, vert, &camray);
            framebuffer[i][j] = solve_ray(camray, scene.bounces);
        }
    }

    normalize_framebuffer(framebuffer, horz_steps, vert_steps);

    printf("C: ...done\n");

    return framebuffer;

}

