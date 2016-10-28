#include <math.h>
#include <stdio.h>
#include "vec3f.h"

const Vector3f ZERO_VEC3F = {0.0f, 0.0f, 0.0f};

void print_vec3f(Vector3f a)
{
    printf("%f %f %f\n", a.x, a.y, a.z);
}

inline float vec3fdot(Vector3f a, Vector3f b)
{
    return a.x*b.x + a.y*b.y + a.z*b.z;
}

inline Vector3f vec3fsub(Vector3f a, Vector3f b)
{
    Vector3f v;
    v.x = a.x - b.x;
    v.y = a.y - b.y;
    v.z = a.z - b.z;
    return v;
}

inline Vector3f vec3fsum2(Vector3f a, Vector3f b)
{
    Vector3f v;
    v.x = a.x + b.x;
    v.y = a.y + b.y;
    v.z = a.z + b.z;
    return v;
}

inline Vector3f vec3fprodf(Vector3f a, float b)
{
    Vector3f v;
    v.x = a.x*b;
    v.y = a.y*b;
    v.z = a.z*b;
    return v;
}

inline Vector3f vec3fsum3(Vector3f a, Vector3f b, Vector3f c)
{
    Vector3f v;
    v.x = a.x + b.x + c.x;
    v.y = a.y + b.y + c.y;
    v.z = a.z + b.z + c.z;
    return v;
}

inline Vector3f vec3fcross(Vector3f a, Vector3f b)
{
    Vector3f v;
    v.x = a.y*b.z - a.z*b.y;
    v.y = a.z*b.x - a.x*b.z;
    v.z = a.x*b.y - a.y*b.x;
    return v;
}

inline float vec3fabs(Vector3f a)
{
    return sqrt(a.x*a.x + a.y*a.y + a.z*a.z);
}

inline Vector3f vec3fnorm(Vector3f a)
{
    Vector3f v;
    float abs = vec3fabs(a);
    v.x = a.x/abs;
    v.y = a.y/abs;
    v.z = a.z/abs;
    return v;
}
