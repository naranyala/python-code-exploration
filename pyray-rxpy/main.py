#!/usr/bin/env python3
"""
Raylib Python Demo
Demonstrates basic raylib functionality using electronstudio/raylib-python-cffi
"""

import raylib as rl
from raylib import colors
import math


def main():
    # Window configuration
    screen_width = 800
    screen_height = 600
    window_title = "Raylib Python Demo"

    # Initialize window
    rl.InitWindow(screen_width, screen_height, window_title.encode('utf-8'))
    rl.SetTargetFPS(60)

    # Game state variables
    ball_x = screen_width / 2
    ball_y = screen_height / 2
    ball_speed_x = 5.0
    ball_speed_y = 4.0
    ball_radius = 20.0

    rectangle_x = screen_width / 2 - 50
    rectangle_y = screen_height / 2 - 50
    rectangle_width = 100
    rectangle_height = 100

    frame_counter = 0

    # Main game loop
    while not rl.WindowShouldClose():
        # Update
        frame_counter += 1

        # Update ball position
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # Ball collision with screen boundaries
        if ball_x >= (screen_width - ball_radius) or ball_x <= ball_radius:
            ball_speed_x *= -1

        if ball_y >= (screen_height - ball_radius) or ball_y <= ball_radius:
            ball_speed_y *= -1

        # Rectangle movement with arrow keys
        if rl.IsKeyDown(rl.KEY_RIGHT):
            rectangle_x += 5
        if rl.IsKeyDown(rl.KEY_LEFT):
            rectangle_x -= 5
        if rl.IsKeyDown(rl.KEY_UP):
            rectangle_y -= 5
        if rl.IsKeyDown(rl.KEY_DOWN):
            rectangle_y += 5

        # Keep rectangle within screen bounds
        if rectangle_x < 0:
            rectangle_x = 0
        if rectangle_x > screen_width - rectangle_width:
            rectangle_x = screen_width - rectangle_width
        if rectangle_y < 0:
            rectangle_y = 0
        if rectangle_y > screen_height - rectangle_height:
            rectangle_y = screen_height - rectangle_height

        # Draw
        rl.BeginDrawing()
        rl.ClearBackground(colors.RAYWHITE)

        # Draw bouncing ball
        rl.DrawCircle(int(ball_x), int(ball_y), ball_radius, colors.MAROON)

        # Draw controllable rectangle
        rl.DrawRectangle(int(rectangle_x), int(rectangle_y), int(rectangle_width), int(rectangle_height), colors.BLUE)
        rl.DrawRectangleLines(int(rectangle_x), int(rectangle_y), int(rectangle_width), int(rectangle_height), colors.DARKBLUE)

        # Draw sine wave
        wave_amplitude = 50
        wave_frequency = 0.02
        wave_y_offset = screen_height - 100

        for x in range(0, screen_width, 2):
            y = wave_y_offset + math.sin(x * wave_frequency + frame_counter * 0.1) * wave_amplitude
            rl.DrawPixel(x, int(y), colors.GREEN)

        # Draw grid
        grid_spacing = 50
        for i in range(0, screen_width, grid_spacing):
            rl.DrawLine(i, 0, i, screen_height, colors.LIGHTGRAY)
        for i in range(0, screen_height, grid_spacing):
            rl.DrawLine(0, i, screen_width, i, colors.LIGHTGRAY)

        # Draw text instructions
        instruction_text = "Use arrow keys to move the rectangle"
        text_width = rl.MeasureText(instruction_text.encode('utf-8'), 20)
        rl.DrawText(instruction_text.encode('utf-8'),
                    (screen_width - text_width) // 2,
                    10,
                    20,
                    colors.DARKGRAY)

        # Draw FPS counter
        rl.DrawFPS(10, 10)

        rl.EndDrawing()

    # Cleanup
    rl.CloseWindow()


if __name__ == "__main__":
    main()
