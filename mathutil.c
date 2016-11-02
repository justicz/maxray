#include "mathutil.h"

inline float minf(float a, float b) {
    return a < b ? a : b;
}

inline float maxf(float a, float b) {
    return a > b ? a : b;
}

inline int mini(int a, int b) {
    return a < b ? a : b;
}

inline int maxi(int a, int b) {
    return a > b ? a : b;
}

inline void transform_pos_by_matrix4f(Vector3f *pt, Matrix4f t)
{
    Vector3f out;
    out.x = pt->x*t.m11 + pt->y*t.m12 + pt->z*t.m13 + t.m14;
    out.y = pt->x*t.m21 + pt->y*t.m22 + pt->z*t.m23 + t.m24;
    out.z = pt->x*t.m31 + pt->y*t.m32 + pt->z*t.m33 + t.m34;
    *pt = out;
}

inline void transform_vec_by_matrix4f(Vector3f *vec, Matrix4f t)
{
    Vector3f out;
    out.x = vec->x*t.m11 + vec->y*t.m12 + vec->z*t.m13;
    out.y = vec->x*t.m21 + vec->y*t.m22 + vec->z*t.m23;
    out.z = vec->x*t.m31 + vec->y*t.m32 + vec->z*t.m33;
    *vec = out;
}

inline void transform_ray_by_matrix4f(struct Ray *ray, Matrix4f t)
{
    transform_pos_by_matrix4f(&ray->o, t);
    transform_vec_by_matrix4f(&ray->dir, t);
    ray->dir = vec3fnorm(ray->dir);
}

inline void transform_hit_by_matrix4f(struct Hit *hit, struct Ray ray, Matrix4f t, Matrix4f ti)
{
    transform_pos_by_matrix4f(&hit->hit_coords, t);
    hit->dist = vec3fabs(vec3fsub(hit->hit_coords, ray.o));
    Matrix4f transposed = matrix4ftransposed(ti);
    transform_vec_by_matrix4f(&hit->norm, transposed);
    hit->norm = vec3fnorm(hit->norm);
}

