#pragma once

typedef struct {
    float x;
    float y;
    float z;
} Vector3f;

extern const Vector3f ZERO_VEC3F;
float vec3fdot(Vector3f a, Vector3f b);
Vector3f vec3fcross(Vector3f a, Vector3f b);
Vector3f vec3fnorm(Vector3f a);
float vec3fabs(Vector3f a);
Vector3f vec3fprodf(Vector3f a, float b);
Vector3f vec3fsum2(Vector3f a, Vector3f b);
Vector3f vec3fsum3(Vector3f a, Vector3f b, Vector3f c);
Vector3f vec3fhad(Vector3f a, Vector3f b);
Vector3f vec3fsub(Vector3f a, Vector3f b);
void print_vec3f(Vector3f a);

