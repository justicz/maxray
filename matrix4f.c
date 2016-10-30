#include <math.h>
#include <stdio.h>
#include "matrix4f.h"

void print_matrix4f(Matrix4f a)
{
    printf("Matrix4f[\n");
    printf("\t[%f %f %f %f]\n", a.m11, a.m12, a.m13, a.m14);
    printf("\t[%f %f %f %f]\n", a.m21, a.m22, a.m23, a.m24);
    printf("\t[%f %f %f %f]\n", a.m31, a.m32, a.m33, a.m34);
    printf("\t[%f %f %f %f]\n", a.m41, a.m42, a.m43, a.m44);
    printf("]\n");
}

Matrix4f matrix4ftransposed(Matrix4f a)
{
    Matrix4f out;
    out.m11 = a.m11; out.m12 = a.m21; out.m13 = a.m31; out.m14 = a.m41;
    out.m21 = a.m12; out.m22 = a.m22; out.m23 = a.m32; out.m24 = a.m42;
    out.m31 = a.m13; out.m32 = a.m23; out.m33 = a.m33; out.m34 = a.m43;
    out.m41 = a.m14; out.m42 = a.m24; out.m43 = a.m34; out.m44 = a.m44;
    return out;
}
