#pragma once
#include "matrix4f.h"
#include "vec3f.h"
#include "load.h"

float minf(float a, float b);

float maxf(float a, float b);

int mini(int a, int b);

int maxi(int a, int b);

void transform_pos_by_matrix4f(Vector3f *pt, Matrix4f t);

void transform_vec_by_matrix4f(Vector3f *vec, Matrix4f t);

void transform_ray_by_matrix4f(struct Ray *ray, Matrix4f t);

void transform_hit_by_matrix4f(struct Hit *hit, struct Ray ray, Matrix4f t, Matrix4f ti);


