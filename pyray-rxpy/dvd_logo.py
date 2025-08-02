#!/usr/bin/env python3
"""
DVD Logo Bounce - Python Port
A bouncing DVD logo screensaver with color changes on wall hits.
"""

import pyray as rl

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
LOGO_WIDTH = 100
LOGO_HEIGHT = 50
SPEED = 2

# Variables
logo_x = SCREEN_WIDTH // 2 - LOGO_WIDTH // 2
logo_y = SCREEN_HEIGHT // 2 - LOGO_HEIGHT // 2
dx = SPEED
dy = SPEED

colors = [
    rl.RED, rl.GREEN, rl.BLUE, rl.YELLOW,
    rl.ORANGE, rl.PURPLE, rl.PINK, rl.SKYBLUE
]
current_color = 0

# Initialize window
rl.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "DVD Logo Bounce")
rl.set_target_fps(60)

# Main game loop
while not rl.window_should_close():
    # Update position
    logo_x += dx
    logo_y += dy
    
    # Check for wall collisions
    if logo_x <= 0 or logo_x + LOGO_WIDTH >= SCREEN_WIDTH:
        dx = -dx
        current_color = (current_color + 1) % len(colors)
    
    if logo_y <= 0 or logo_y + LOGO_HEIGHT >= SCREEN_HEIGHT:
        dy = -dy
        current_color = (current_color + 1) % len(colors)
    
    # Draw
    rl.begin_drawing()
    rl.clear_background(rl.BLACK)
    
    # Draw DVD-like rectangle
    rl.draw_rectangle(logo_x, logo_y, LOGO_WIDTH, LOGO_HEIGHT, colors[current_color])
    
    # Add some text to make it look more like the DVD logo
    rl.draw_text("DVD", logo_x + 10, logo_y + 10, 20, rl.WHITE)
    
    rl.end_drawing()

# Clean up
rl.close_window()
