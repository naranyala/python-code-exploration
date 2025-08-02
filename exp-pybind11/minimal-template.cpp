// array_view.h – A minimal, bounds-checked view
#pragma once
#include <cassert>
#include <cstddef>

template <typename T> struct ArrayView {
  T *data;
  size_t size;

  T &operator[](size_t i) {
    assert(i < size); // Explicit bounds check
    return data[i];
  }
};

// Usage:
int sum(ArrayView<const int> view) {
  int total = 0;
  for (size_t i = 0; i < view.size; ++i) {
    total += view[i];
  }
  return total;
}
