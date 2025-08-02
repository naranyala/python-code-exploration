// arena.h – Manual memory management
#pragma once
#include <cstdlib>

struct Arena {
  char *data;
  size_t size;
  size_t used;
};

void arena_init(Arena *a, void *buffer, size_t size);
void *arena_alloc(Arena *a, size_t size); // Returns nullptr if OOM

// Usage:
Arena stack_arena;
char buffer[1024];
arena_init(&stack_arena, buffer, sizeof(buffer));

int *nums = (int *)arena_alloc(&stack_arena, 10 * sizeof(int));
