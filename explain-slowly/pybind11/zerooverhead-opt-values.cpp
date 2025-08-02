// optional.h
#pragma once

template <typename T> struct Optional {
  T value;
  bool has_value;
};

// Usage:
Optional<int> find(int *arr, size_t len, int target) {
  for (size_t i = 0; i < len; ++i) {
    if (arr[i] == target)
      return {arr[i], true};
  }
  return {{}, false};
}

void user() {
  int vals[] = {1, 2, 3};
  auto opt = find(vals, 3, 2);
  if (opt.has_value) {
    // Use opt.value
  }
}
