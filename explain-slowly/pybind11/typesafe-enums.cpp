// rgb.h
#pragma once

enum class RgbColor : uint8_t { // Fixed underlying type
  Red = 0xFF0000,
  Green = 0x00FF00,
  Blue = 0x0000FF
};

constexpr bool is_valid_rgb(RgbColor c) { // Compile-time check
  return c == RgbColor::Red || c == RgbColor::Green || c == RgbColor::Blue;
}

// Usage:
static_assert(is_valid_rgb(RgbColor::Red)); // Fails at compile-time if invalid
