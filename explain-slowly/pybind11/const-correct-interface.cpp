// string_utils.h
#pragma once

// Immutable string view
struct StrView {
  const char *data;
  size_t len;
};

// Pure function: no side effects, takes/returns by value
StrView trim_whitespace(StrView s);

// Usage:
void print_trimmed(const char *s) {
  StrView view = {s, strlen(s)};
  StrView trimmed = trim_whitespace(view);
  printf("%.*s\n", (int)trimmed.len, trimmed.data);
}
