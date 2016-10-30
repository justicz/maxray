CC = gcc
CFLAGS = -fPIC -Wall -Wextra -O2 -std=c99 -fopenmp
LDFLAGS = -shared -fopenmp
TARGET_LIB = ray.so

SRCS = ray.c load.c vec3f.c matrix4f.c
OBJS = $(SRCS:.c=.o)

$(TARGET_LIB): $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $^

$(SRCS:.c=.d):%.d:%.c
	$(CC) $(CFLAGS) -MM $< >$@

