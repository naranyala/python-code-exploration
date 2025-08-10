import pyray as rl
import math

def main():
    # Initialize
    screen_width = 800
    screen_height = 600
    rl.init_window(screen_width, screen_height, "Circle with Raylib")
    rl.set_target_fps(60)
    
    # Circle properties
    center_x = screen_width // 2
    center_y = screen_height // 2
    radius = 100.0
    
    # Main game loop
    while not rl.window_should_close():
        # Update
        if rl.is_key_pressed(rl.KEY_ESCAPE):
            break
        
        # Draw
        rl.begin_drawing()
        rl.clear_background(rl.Color(25, 25, 25, 255))  # Dark gray
        
        # Draw circle
        rl.draw_circle(center_x, center_y, radius, rl.WHITE)
        
        # Optional: Draw circle outline
        rl.draw_circle_lines(center_x, center_y, radius + 5, rl.RED)
        
        rl.end_drawing()
    
    # Cleanup
    rl.close_window()

if __name__ == "__main__":
    main()
