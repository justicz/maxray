CC = gcc
CFLAGS = -fPIC -Wall -flto -Wextra -O3 -std=c99 -fopenmp
LDFLAGS = -shared -fopenmp -flto
TARGET_LIB = ray.so

SRCS = ray.c load.c vec3f.c matrix4f.c
OBJS = $(SRCS:.c=.o)

$(TARGET_LIB): $(OBJS)
	$(CC) $(LDFLAGS) -o $@ $^

$(SRCS:.c=.d):%.d:%.c
	$(CC) $(CFLAGS) -MM $< >$@

.PHONY: clean
clean:
	rm *.o

