// shape.h
#pragma once
#include <cmath>

struct Circle {
  double radius;
};
struct Square {
  double side;
};

// Tagged union for type-safe dispatch
struct Shape {
  enum class Type { Circle, Square } tag;
  union {
    Circle circle;
    Square square;
  };
};

// Procedural "methods"
double area(const Shape &s) {
  switch (s.tag) {
  case Shape::Type::Circle:
    return M_PI * s.circle.radius * s.circle.radius;
  case Shape::Type::Square:
    return s.square.side * s.square.side;
  }
}
