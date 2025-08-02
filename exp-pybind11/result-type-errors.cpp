// result.h
#pragma once

template <typename T> struct Result {
  bool ok;
  union {
    T value;
    struct {
      int code;
      const char *msg;
    } error;
  };
};

// Usage:
Result<int> parse_number(const char *s) {
  if (!s)
    return {false, {.error = {1, "Null input"}}};
  // ... parsing logic ...
  return {true, {.value = 42}};
}

void user() {
  auto r = parse_number("123");
  if (!r.ok) {
    fprintf(stderr, "Error %d: %s\n", r.error.code, r.error.msg);
    return;
  }
  printf("Value: %d\n", r.value);
}
